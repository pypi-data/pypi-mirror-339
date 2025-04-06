import logging
import os
import requests
import json
from pyspark.sql import SparkSession, DataFrame
from pyspark.conf import SparkConf
from pyspark.sql.functions import col, udf, to_timestamp, date_format, window, expr
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.types import IntegerType


import os
from dotenv import load_dotenv
load_dotenv('/.env')

# ====== Logging Setup ======
logging.basicConfig(
    format="%(asctime)s | %(name)s - %(funcName)s - %(lineno)d | %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====== Configuration ======
KAFKA_BROKER = "redpanda:29092" # "kafka.de.data.snapp.tech:9092"
S3_ENDPOINT = "http://host.docker.internal:9000" # "http://s3.teh-1.snappcloud.io"
SCHEMA_REGISTRY_URL = "http://schema-registry.de.data.snapp.tech:8081"
# KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "dbz.snapp_backoffice_mysql.backoffice.driver_documents")
KAFKA_TOPIC = "dbz.snapp_backoffice_mysql.backoffice.driver_documents"
kafka_user = os.getenv("KAFKA_USER")
kafka_password = os.getenv("KAFKA_PASSWORD")
kafka_request_timeout = os.getenv("KAFKA_REQUEST_TIMEOUT", "30000")
kafka_session_timeout = os.getenv("KAFKA_SESSION_TIMEOUT", "30000")
min_offset = os.getenv("MIN_OFFSET", "1")
max_offset = os.getenv("MAX_OFFSET", "2000000")
WRITE_MODE = os.getenv("WRITE_MODE", "APPEND")
STARTING_OFFSET = os.getenv("STARTING_OFFSET", "earliest")
Bucket_name = "smapp-eta-farsanj-results-production-bucket"

# ====== UDF ======
def byte_array_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder="big")


schema_id_udf = udf(byte_array_to_int, IntegerType())

# ====== CREATE SPARK SESSION ======
def create_spark_session():
    """
    Initializes and returns a SparkSession. Assumes user has an existing `create_spark_session()` method.
    spark_conf.set("spark.jars.packages","org.apache.spark:spark-avro_2.12:3.5.1
                                        , org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,
                                          org.apache.kafka:kafka-clients:3.9.0")

    """
    try:
        spark_conf = SparkConf()
        spark_conf.set("spark.logLevel", "INFO")
        spark_conf.set("spark.appName", "s3_sink_"+os.path.basename(__file__))
        spark_conf.set("spark.hadoop.fs.s3a.access.key", os.getenv("S3_ACCESS_KEY"))
        spark_conf.set("spark.hadoop.fs.s3a.secret.key", os.getenv("S3_SECRET_KEY"))
        spark_conf.set("spark.hadoop.fs.s3a.endpoint", "http://host.docker.internal:9000")
        spark_conf.set("spark.hadoop.fs.s3a.path.style.access", "true")
        spark_conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        spark_conf.set("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        spark_conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        spark_conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        spark_conf.set("spark.jars.packages","org.apache.spark:spark-avro_2.12:3.5.1,"
                                             "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
                                             "org.apache.kafka:kafka-clients:3.9.0")
        spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()

        logger.info("✅ Spark session created successfully.")
        return spark
    except Exception as e:
        logger.error(f"❌ Failed to create Spark session: {e}")
    raise

# ====== FETCH SCHEMA VERSIONS FROM REGISTRY ======
def get_schemas_from_registry(schema_ids):
    schemas = {}

    for schema_id in schema_ids:
        schema_url = f"{SCHEMA_REGISTRY_URL}/schemas/ids/{schema_id}"
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
def read_kafka_batch(spark):
    df = spark.read.format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("minOffsetsPerTrigger", min_offset) \
        .option("maxOffsetsPerTrigger", max_offset) \
        .option("failOnDataLoss", "false") \
        .option("startingOffsets", STARTING_OFFSET) \
        .option("kafkaConsumer.pollTimeoutMs", kafka_session_timeout) \
        .option("kafka.request.timeout.ms", kafka_request_timeout) \
        .option("kafka.session.timeout.ms", kafka_session_timeout) \
        .load()
    # .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
    # .option("kafka.security.protocol", "SASL_PLAINTEXT") \
    # .option("kafka.sasl.jaas.config",
    #         f"org.apache.kafka.common.security.scram.ScramLoginModule required username='{kafka_user}' password='{kafka_password}';") \

    df = df.withColumn("schema_id_bytes", expr("substring(value, 2, 4)"))
    df = df.withColumn("schema_id", schema_id_udf(col("schema_id_bytes")))
    df = df.withColumn("avro_payload", expr("substring(value, 6, length(value)-5)"))


    unique_schema_ids = [row["schema_id"] for row in df.select("schema_id").distinct().collect()]
    logger.info(f" ✅ Successfully read Kafka batch. Loaded {df.count()} records from Kafka with {len(unique_schema_ids)} unique schema IDs")
    return df, unique_schema_ids

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
    df = df.withColumn("accept_event_timestamp", to_timestamp(df["accept_event_timestamp"], "yyyy-MM-dd'T'HH:mm:ss"))
    df = df.withColumn("board_event_timestamp", to_timestamp(df["board_event_timestamp"], "yyyy-MM-dd'T'HH:mm:ss"))
    df = df.withColumn("finish_event_timestamp", to_timestamp(df["finish_event_timestamp"], "yyyy-MM-dd'T'HH:mm:ss"))
    df = df.withColumn("insert_timestamp", to_timestamp(df["insert_timestamp"], "yyyy-MM-dd'T'HH:mm:ss"))

    df = df.withColumn("created_date",
                       date_format(window(df["accept_event_timestamp"], "1 day").start, "yyyy-MM-dd"))
    logger.info("✅ Transformations successfully handled on Spark batch.")
    return df

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
def write_to_hudi(df: DataFrame, partition_col: str, bucket: str):
    print(df.show())
    logger.info(f"✅ Data written to {bucket}  Hudi.")

# ====== MAIN BATCH PROCESSING ======
def run_batch(bucket: str):
    # Extract
    spark = create_spark_session()
    df_kafka, schema_ids = read_kafka_batch(spark)
    schemas = get_schemas_from_registry(schema_ids)
    df_processed = process_data_with_schema_evolution(df_kafka, schemas)
    del df_kafka

    # Transform
    df_transformed = transform(df_processed)
    del df_processed

    # Load
    if WRITE_MODE == "APPEND":
        write_to_delta(df_transformed , partition_col="created_at", bucket=bucket)
    elif WRITE_MODE == "OVERWRITE":
        write_to_hudi(df_transformed, partition_col="created_at", bucket=bucket)

    logger.info("🎉 Batch processing completed.")


if __name__ == "__main__":
    try:
        run_batch(Bucket_name)
    except KeyboardInterrupt:
        logger.info("🛑 Streaming stopped by user.")
    except Exception as e:
        logger.critical(f"🚨 Critical error in the application: {e}")

# For Run : helm install smapp-eta-farsanj-results-production ./sink/chart -n data-de-spark -f sink/smapp-eta-farsanj-results-production/values.yml
# For Stop : helm uninstall smapp-eta-farsanj-results-production

