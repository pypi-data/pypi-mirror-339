from dotenv import load_dotenv
from spark_sink_connector.spark_sink_connector import SparkSinkConnector
from spark_sink_connector.enums import SchemaKind, ConnectorOutputMode, ConnectorMode
from spark_sink_connector.spark_sink_config import SparkSinkConfig
from pyspark.sql.functions import to_date

if __name__ == "__main__":
    load_dotenv('/.env')  # For local test

    # Create configuration
    config = SparkSinkConfig(
        kafka_broker="redpanda:29092",
        s3_endpoint="http://host.docker.internal:9000",
        kafka_topic="mobser-passenger-cancellation-permanent-banning",
        kafka_user=None,
        kafka_password=None
    )

    # Create and use connector with method chaining
    connector = SparkSinkConnector(connector_mode=ConnectorMode.STREAM, config=config)

    # Execute the pipeline
    (connector
     .read_from_kafka()
     .apply_schema_from_file(
        kind=SchemaKind.PROTOBUF,
        file_name="/schemas/schema.desc",
        message_name="PassengerCancellationPermenantBanningEvent"
     )
     .transform(lambda df: df.withColumn("created_date", to_date(df["published_at"])))
     .write_delta_to_s3(
        partition_key="created_date",
        output_mode=ConnectorOutputMode.APPEND,
        bucket_name="snapp-raw-log-passenger-cancellation-permenant-banning-bucket"
     )
     .start())
