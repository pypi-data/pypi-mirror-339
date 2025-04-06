import logging
import os
from dotenv import load_dotenv
import requests
import json
from pyspark.sql import SparkSession, DataFrame
from pyspark.conf import SparkConf
from pyspark.sql.functions import col, udf , to_timestamp, to_date, expr
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.types import IntegerType
from dataclasses import dataclass, field
import os
import sys

load_dotenv('/.env')  # For local test


def validate_write_mode(value: str):
    allowed_values = {"APPEND", "UPSERT"}
    if value not in allowed_values:
        raise ValueError(f"Invalid write mode: {value}. Only 'APPEND' and 'UPSERT' are allowed. But {value} provided")
    return value


@dataclass()
class Connections:
    url: str
    port: str
    user_env_name: str
    pass_env_name: str
    extra_configs: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if self.port:
            self.url_with_port = self.url + ":" + self.port
        else:
            self.url_with_port = self.url
        self.username = os.getenv(self.user_env_name, "")
        self.password = os.getenv(self.pass_env_name, "")


@dataclass
class appConfig:
    packages: list[str]
    partition_column: str
    key_column: str
    updating_column: str
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    write_mode: str = os.getenv("WRITE_MODE", "")
    full_table_name: str = os.path.basename(os.path.abspath(sys.argv[0])).strip(".py")

    def __post_init__(self):
        self.write_mode = validate_write_mode(self.write_mode)
        self.s3_bucket_name = f"{self.full_table_name}-bucket"
        self.hudi_path = f"s3a://{self.full_table_name}-bucket/{self.full_table_name}"
        self.hudi_checkpoint_path = f"s3a://{self.full_table_name}-bucket/checkpoints/{self.full_table_name}"
        self.hudi_table_name = f"{self.full_table_name}"
# ====== Configuration ======

sink_app_configs = appConfig(
    packages=[
        "org.apache.spark:spark-avro_2.12:3.5.1",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
        "org.apache.kafka:kafka-clients:3.9.0"
    ],
    partition_column="created_date",
    key_column="id",
    updating_column="updated_at"
)

s3_connection = Connections(
    url="http://host.docker.internal:9000",  # "http://s3.teh-1.snappcloud.io",
    port="9000",
    user_env_name="S3_ACCESS_KEY",
    pass_env_name="S3_SECRET_KEY"
)

kafka_connection = Connections(
    url="redpanda",  # "kafka.de.data.snapp.tech",
    port="29092",  # "9092",
    user_env_name="KAFKA_USER",
    pass_env_name="KAFKA_PASSWORD",
    extra_configs= {
        "schema_registry_url": "http://schema-registry.de.data.snapp.tech:8081",
        "request_timeout": os.getenv("KAFKA_REQUEST_TIMEOUT", ""),
        "session_timeout": os.getenv("KAFKA_SESSION_TIMEOUT", ""),
        "min_offset": os.getenv("MIN_OFFSET", ""),
        "max_offset": os.getenv("MAX_OFFSET", ""),
        "kafka_topic":"dbz.box_mysql_most_used.order_service_prod.orders",  # os.getenv("KAFKA_TOPIC",""),
        "starting_offset": os.getenv("STARTING_OFFSET","")
        }
)

# ====== Logging Setup ======
logging.basicConfig(
    format="%(asctime)s | %(name)s - %(funcName)s - %(lineno)d | %(levelname)s - %(message)s",
    level=sink_app_configs.log_level
)
logger = logging.getLogger(__name__)

# ====== UDF ======
def byte_array_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder="big")

schema_id_udf = udf(byte_array_to_int, IntegerType())

# ====== CREATE SPARK SESSION ======
def create_spark_session():
    try:
        spark_conf = SparkConf()
        spark_conf.set("spark.logLevel", "INFO")
        spark_conf.set("spark.appName", "s3_sink_" + os.path.basename(__file__))
        spark_conf.set("spark.hadoop.fs.s3a.access.key", s3_connection.username)
        spark_conf.set("spark.hadoop.fs.s3a.secret.key", s3_connection.password)
        spark_conf.set("spark.hadoop.fs.s3a.endpoint", s3_connection.url)
        spark_conf.set("spark.hadoop.fs.s3a.path.style.access", "true")
        spark_conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        spark_conf.set("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        spark_conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        spark_conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        spark_conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        spark_conf.set("spark.jars.packages",",".join(sink_app_configs.packages))
        spark_conf.set("spark.sql.session.timeZone", "Asia/Tehran")
        spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()
        # spark.sparkContext.setLogLevel("DEBUG")
        logger.info("✅ Spark session created successfully.")
        return spark
    except Exception as e:
        logger.error(f"❌ Failed to create Spark session: {e}")
    raise

# ====== FETCH SCHEMA VERSIONS FROM REGISTRY ======
def get_schemas_from_registry(schema_ids):
    schemas = {}

    for schema_id in schema_ids:
        schema_url = f"{kafka_connection.extra_configs['schema_registry_url']}/schemas/ids/{schema_id}"
        try:
            response = requests.get(schema_url)
            response.raise_for_status()
            schema_json = response.json()["schema"]
            schemas[schema_id] = json.loads(schema_json)

            logger.info(f"✅ Successfully fetched schema ID {schema_id}")
        except requests.RequestException as e:
            logger.error(f"❌ Failed to fetch schema ID {schema_id}: {e}")
            raise

    return schemas


# ====== READ DATA FROM KAFKA ======
def read_kafka_batch(spark: SparkSession) :
    df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", kafka_connection.url_with_port) \
        .option("subscribe", kafka_connection.extra_configs['kafka_topic']) \
        .option("minOffsetsPerTrigger", kafka_connection.extra_configs['min_offset']) \
        .option("maxOffsetsPerTrigger", kafka_connection.extra_configs['max_offset']) \
        .option("failOnDataLoss", "false") \
        .option("startingOffsets", kafka_connection.extra_configs['starting_offset']) \
        .option("kafkaConsumer.pollTimeoutMs", kafka_connection.extra_configs['session_timeout']) \
        .option("kafka.request.timeout.ms", kafka_connection.extra_configs['request_timeout']) \
        .option("kafka.session.timeout.ms", kafka_connection.extra_configs['session_timeout']) \
        .load()
    # .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
    # .option("kafka.security.protocol", "SASL_PLAINTEXT") \
    # .option("kafka.sasl.jaas.config",
    #         f"org.apache.kafka.common.security.scram.ScramLoginModule required username='{kafka_connection.username}' password='{kafka_connection.password}';") \

    df = df.withColumn("schema_id_bytes", expr("substring(value, 2, 4)"))
    df = df.withColumn("schema_id", schema_id_udf(col("schema_id_bytes")))
    df = df.withColumn("avro_payload", expr("substring(value, 6, length(value)-5)"))

    

    logger.info(
        f" ✅ Successfully read Kafka batch.")
    return df

# ====== APPLY SCHEMA EVOLUTION HANDLING ======
def process_data_with_schema_evolution(df, schemas):
    schema_dfs = []

    for schema_id, schema in schemas.items():
        try:
            # Filter records for this schema ID
            df_filtered = df.filter(col("schema_id") == schema_id)

            # Deserialize using `from_avro`
            df_schema = df_filtered.withColumn(
                "data",
                from_avro(col("avro_payload"), json.dumps(schema))
            ).select("data.*")

            schema_dfs.append(df_schema)
        except Exception as e:
            logger.warning(f"⚠️ Skipping schema {schema_id} due to error: {e}")

    if not schema_dfs:
        raise ValueError("No valid schema could be applied to the batch.")

    # Merge all schema variations dynamically
    merged_df = schema_dfs[0]
    for additional_df in schema_dfs[1:]:
        merged_df = merged_df.unionByName(additional_df, allowMissingColumns=True)

    logger.info("✅ Schema evolution successfully handled within batch.")
    return merged_df

# ====== TRANSOFRMATIONS ======
def transform(df: DataFrame) -> DataFrame:
    df = df.withColumn("created_at", to_timestamp(df["created_at"], "yyyy-MM-dd'T'HH:mm:ss"))
    df = df.withColumn("updated_at", to_timestamp(df["updated_at"], "yyyy-MM-dd'T'HH:mm:ss"))

    df = df.withColumn("created_date",to_date('created_at'))

    logger.info("✅ Transformations successfully handled on Spark batch.")
    return df


# ====== WRITE TO HUDI ======

hudi_options = {
    "hoodie.table.name": sink_app_configs.hudi_table_name,
    "hoodie.datasource.write.partitionpath.field": sink_app_configs.partition_column,
    "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
    "hoodie.datasource.write.recordkey.field": sink_app_configs.key_column,
    "hoodie.datasource.write.precombine.field": sink_app_configs.updating_column
}


# ====== WRITE TO DELTA ======
def write_to_delta(df: DataFrame, partition_col: str, bucket: str):
    df.coalesce(1).write \
        .format("delta") \
        .partitionBy(partition_col) \
        .mode("append") \
        .option("checkpointLocation", f"s3a://{bucket}/checkpoints/{bucket.replace('-bucket','')}") \
        .save(f"s3a://{bucket}/{bucket.replace('-bucket','')}")

    logger.info(f"✅ Data written to {bucket} Parquet.")


# ====== WRITE TO HUDI ======
def write_to_hudi(df: DataFrame, hudi_base_path: str, hudi_options: dict[str,str],hudi_partition_key:str):
    df.write \
            .format("hudi") \
            .partitionBy(hudi_partition_key) \
            .options(**hudi_options) \
            .mode("append") \
            .save(hudi_base_path)
    logger.info(f"✅ Data written to {hudi_base_path}  Hudi.")

# ====== MAIN BATCH PROCESSING ======
def run_batch(batch_df: DataFrame,batch_id: int):

    if batch_df.isEmpty():
        logger.error(f"The batch with batch_id = {batch_id} was empty. Continue to next batch ...")
        return None
    # Get Schemas
    unique_schema_ids = [row["schema_id"] for row in batch_df.select("schema_id").distinct().collect()]
    if not unique_schema_ids:
        logger.error("Can't extract any schema id from dataframe")
    schemas = get_schemas_from_registry(unique_schema_ids)
    # Transform 
    df_processed = process_data_with_schema_evolution(batch_df, schemas)
    df_transformed = transform(df_processed)


    # Load
    if sink_app_configs.write_mode == "APPEND":
        write_to_delta(df_transformed , partition_col="created_date", bucket=sink_app_configs.s3_bucket_name)
    elif sink_app_configs.write_mode == "UPSERT":
        write_to_hudi(df_transformed,sink_app_configs.hudi_path,hudi_options,sink_app_configs.partition_column)
    else:
        logger.critical("🚨 WRITE_MODE not defined, Data Won't write anywhere")

    logger.info("🎉 Batch processing completed.")


if __name__ == "__main__":
    spark = create_spark_session()
    df_kafka = read_kafka_batch(spark)  

    (df_kafka.writeStream
    .foreachBatch(run_batch)
    .option("checkpointLocation", sink_app_configs.hudi_checkpoint_path)
    .trigger(availableNow=True)
    .start().awaitTermination()
    )

# For Run : helm install snapp-backoffice-tags ./sink/chart -n data-de-spark -f sink/snapp-backoffice-tags/values.yml
# For Stop : helm uninstall snapp-backoffice-tags
