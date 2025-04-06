import os
import sys
from dotenv import load_dotenv
from spark_sink_connector.schema_helper import get_schemas_from_registry
from spark_sink_connector.schema_helper import process_data_with_schema_evolution, schema_id_udf
from spark_sink_connector.enums import ConnectorMode
from spark_sink_connector.spark_sink_config import SparkSinkConfig
from spark_sink_connector.spark_sink_connector import SparkSinkConnector
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_timestamp, to_date, expr

if __name__ == "__main__":
    load_dotenv('/.env')  # For local test

    config = SparkSinkConfig(
        kafka_broker="redpanda:29092",
        s3_endpoint="http://host.docker.internal:9000",
        schema_registry_url="http://schema-registry.de.data.snapp.tech:8081",
        kafka_topic="dbz.box_mysql_most_used.order_service_prod.orders",
        hudi_options={
            "hoodie.table.name": os.path.basename(os.path.abspath(sys.argv[0])).strip(".py"),
            "hoodie.datasource.write.partitionpath.field": "created_date",
            "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
            "hoodie.datasource.write.recordkey.field": "id",
            "hoodie.datasource.write.precombine.field": "updated_at"
        }
    )
    table_path = f"s3a://{config.hudi_options['hoodie.table.name']}-bucket2/{config.hudi_options['hoodie.table.name']}"
    checkpoint_path = f"s3a://{config.hudi_options['hoodie.table.name']}-bucket2/checkpoints/{config.hudi_options['hoodie.table.name']}"

    # Create and use connector with method chaining
    connector = SparkSinkConnector(connector_mode=ConnectorMode.STREAM, config=config, logging_level="INFO")


    def initial_transform(df: DataFrame) -> DataFrame:
        df = df.withColumn("schema_id_bytes", expr("substring(value, 2, 4)"))
        df = df.withColumn("schema_id", schema_id_udf(col("schema_id_bytes")))
        df = df.withColumn("avro_payload", expr("substring(value, 6, length(value)-5)"))
        return df


    def transform(df: DataFrame) -> DataFrame:
        df = df.withColumn("created_at", to_timestamp(df["created_at"], "yyyy-MM-dd'T'HH:mm:ss"))
        df = df.withColumn("updated_at", to_timestamp(df["updated_at"], "yyyy-MM-dd'T'HH:mm:ss"))
        df = df.withColumn("created_date", to_date('created_at'))
        connector.get_logger().info("✅ Transformations successfully handled on Spark batch.")
        return df


    def run_batch(batch_df: DataFrame, batch_id: int):
        if batch_df.isEmpty():
            connector.get_logger().error(f"The batch with batch_id = {batch_id} was empty. Continue to next batch ...")
            return None
        # Get Schemas
        unique_schema_ids = [row["schema_id"] for row in batch_df.select("schema_id").distinct().collect()]
        if not unique_schema_ids:
            connector.get_logger().error("Can't extract any schema id from dataframe")
        schemas = get_schemas_from_registry(unique_schema_ids,
                                            connector.config.schema_registry_url,
                                            connector.get_logger())
        df_processed = process_data_with_schema_evolution(batch_df, schemas, connector.get_logger())
        df_transformed = transform(df_processed)
        df_transformed.write \
            .format("hudi") \
            .partitionBy("created_date") \
            .options(**config.hudi_options) \
            .mode("append") \
            .save(table_path)
        connector.get_logger().info(f"✅ Data written to {table_path}  Hudi.")
        connector.get_logger().info("🎉 Batch processing completed.")


    # Execute the pipeline
    (connector
     .read_from_kafka()
     .transform(initial_transform)
     .get_dataframe()
     .writeStream
     .foreachBatch(run_batch)
     .option("checkpointLocation", checkpoint_path)
     .trigger(availableNow=True)
     .start()
     .awaitTermination())
