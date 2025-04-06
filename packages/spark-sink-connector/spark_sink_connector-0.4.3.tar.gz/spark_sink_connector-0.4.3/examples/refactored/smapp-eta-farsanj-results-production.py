from dotenv import load_dotenv
from pyspark.sql.functions import to_timestamp
from spark_sink_connector.enums import SchemaKind, ConnectorOutputMode, ConnectorMode
from spark_sink_connector.spark_sink_config import SparkSinkConfig
from spark_sink_connector.spark_sink_connector import SparkSinkConnector

if __name__ == "__main__":
    load_dotenv('/.env')  # For local test

    # Create configuration
    config = SparkSinkConfig(
        kafka_broker="redpanda:29092",
        s3_endpoint="http://host.docker.internal:9000",
        schema_registry_url="http://schema-registry.de.data.snapp.tech:8081",
        kafka_topic="dbz.snapp_backoffice_mysql.backoffice.driver_documents"
    )

    # Create and use connector with method chaining
    connector = SparkSinkConnector(connector_mode=ConnectorMode.BATCH, config=config)


    # Define a custom transformation
    def transform_processing(df):
        df = df.withColumn("created_at", to_timestamp(df["created_at"], "yyyy-MM-dd'T'HH:mm:ss"))
        df = df.withColumn("updated_at", to_timestamp(df["updated_at"], "yyyy-MM-dd'T'HH:mm:ss"))
        return df


    # Execute the pipeline
    (connector
     .read_from_kafka()
     .apply_schema_from_registry(kind=SchemaKind.AVRO)
     .transform(transform_processing)
     .write_delta_to_s3(
        partition_key="created_at",
        output_mode=ConnectorOutputMode.APPEND,
        bucket_name="smapp-eta-farsanj-results-production-bucket"
     )
     .start())
