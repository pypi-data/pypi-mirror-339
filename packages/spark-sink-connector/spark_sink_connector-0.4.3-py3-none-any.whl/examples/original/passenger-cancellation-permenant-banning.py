import logging
import os
from pyspark.sql import SparkSession, DataFrame
from pyspark.conf import SparkConf
from pyspark.sql.functions import col, to_date
from pyspark.sql.protobuf.functions import from_protobuf

# ====== Logging Setup ======
logging.basicConfig(
    format="%(asctime)s | %(name)s - %(funcName)s - %(lineno)d | %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv
load_dotenv('/.env')

# ====== Configuration ======
KAFKA_BROKER = "redpanda:29092" # "kafka.de.data.snapp.tech:9092"
S3_ENDPOINT = "http://host.docker.internal:9000" # "http://s3.teh-1.snappcloud.io"
bucket_name = "snapp-raw-log-passenger-cancellation-permenant-banning-bucket"
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
kafka_user = os.getenv("KAFKA_USER")
kafka_password = os.getenv("KAFKA_PASSWORD")
kafka_request_timeout = os.getenv("KAFKA_REQUEST_TIMEOUT", "30000")
kafka_session_timeout = os.getenv("KAFKA_SESSION_TIMEOUT", "30000")
min_offset = os.getenv("MIN_OFFSET", "1")
max_offset = os.getenv("MAX_OFFSET", "2000000")
STARTING_OFFSET = os.getenv("STARTING_OFFSET", "earliest")


# ====== CREATE SPARK SESSION ======
def create_spark_session():
    """
    Initializes and returns a SparkSession. Assumes user has an existing `create_spark_session()` method.
    spark_conf.set("spark.jars.packages","org.apache.spark:spark-avro_2.12:3.5.1
                                        , org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,
                                          org.apache.kafka:kafka-clients:3.9.0,org.apache.spark:spark-protobuf_2.12:3.5.1")

    """
    try:
        spark_conf = SparkConf()
        spark_conf.set("spark.logLevel", "INFO")
        spark_conf.set("spark.sql.protobuf.debug", "true")
        spark_conf.set("spark.appName", "s3_sink_" + os.path.basename(__file__))
        spark_conf.set("spark.hadoop.fs.s3a.access.key", os.getenv("S3_ACCESS_KEY"))
        spark_conf.set("spark.hadoop.fs.s3a.secret.key", os.getenv("S3_SECRET_KEY"))
        spark_conf.set("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT)
        spark_conf.set("spark.hadoop.fs.s3a.path.style.access", "true")
        spark_conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        spark_conf.set("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        spark_conf.set("spark.sql.session.timeZone", "Asia/Tehran")
        spark_conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        spark_conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        spark_conf.set("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.5.1,"
                                              "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
                                              "org.apache.kafka:kafka-clients:3.9.0,"
                                              "org.apache.spark:spark-protobuf_2.12:3.5.1")
        spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()

        logger.info("✅ Spark session created successfully.")
        return spark
    except Exception as e:
        logger.error(f"❌ Failed to create Spark session: {e}")
    raise


# ====== READ DATA FROM KAFKA ======
def read_kafka_batch(spark):
    df = (spark.readStream.format("kafka") 
        .option("kafka.bootstrap.servers", KAFKA_BROKER)
          .option("mode", "PERMISSIVE")
          .option("subscribe", KAFKA_TOPIC)
        .option("minOffsetsPerTrigger", min_offset) 
        .option("maxOffsetsPerTrigger", max_offset)
          .option("failOnDataLoss", "false")
        # .option("kafka.sasl.mechanism", "SCRAM-SHA-512") 
        # .option("kafka.security.protocol", "SASL_PLAINTEXT") 
        # .option("kafka.sasl.jaas.config",
        #         f"org.apache.kafka.common.security.scram.ScramLoginModule required username='{kafka_user}' password='{kafka_password}';") 
        .option("startingOffsets", STARTING_OFFSET) 
        .option("kafkaConsumer.pollTimeoutMs", kafka_session_timeout) 
        .option("kafka.request.timeout.ms", kafka_request_timeout) 
        .option("kafka.session.timeout.ms", kafka_session_timeout) 
        .load())

    logger.info(f" ✅ Successfully read Kafka batch.")
    return df


# ====== TRANSOFRMATIONS ======
def transform(df: DataFrame) -> DataFrame:

    df = df.select(from_protobuf("value", "PassengerCancellationPermenantBanningEvent", "/schemas/schema.desc").alias("event"))
    df = df.select("event.*")
    df = df.withColumn("created_date", to_date(df["published_at"]))

    logger.info("✅ Transformations successfully handled on Spark batch.")
    return df


spark = create_spark_session()
df = read_kafka_batch(spark)
df = transform(df)

# df.printSchema()

df.writeStream \
    .format("delta") \
    .partitionBy("created_date") \
    .trigger(availableNow=True) \
    .outputMode("append") \
    .option("checkpointLocation", f"s3a://{bucket_name}/checkpoints5-refactored/{bucket_name.replace('-bucket', '')}") \
    .option("path", f"s3a://{bucket_name}/{bucket_name.replace('-bucket', '')}-refactored5") \
    .start().awaitTermination()

# df.writeStream.format("console").option("truncate","false").start().awaitTermination()

# For Run : helm install passenger-cancellation-permenant-banning-refactored ./sink/chart -n data-de-spark -f sink/passenger-cancellation-permenant-banning-refactored/values.yml
# For Stop : helm uninstall passenger-cancellation-permenant-banning-refactored
# For create proto descriptor file from proto: protoc --proto_path=./sink/passenger-cancellation-permenant-banning-refactored/ --include_imports --descriptor_set_out=sink/passenger-cancellation-permenant-banning-refactored/schema.desc sink/passenger-cancellation-permenant-banning-refactored/passenger_cancellation.proto
# proto path: https://gitlab.snapp.ir/backend/proto/-/tree/master/pb?ref_type=heads
