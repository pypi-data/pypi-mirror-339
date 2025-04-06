import os
from dataclasses import dataclass, field


@dataclass
class SparkSinkConfig:
    """Configuration container for SparkSinkConnector."""

    kafka_broker: str = field(default_factory=lambda: os.getenv("KAFKA_BROKER", "kafka.de.data.snapp.tech:9092"))
    kafka_topic: str = field(default_factory=lambda: os.getenv("KAFKA_TOPIC", None))
    kafka_user: str = field(default_factory=lambda: os.getenv("KAFKA_USER", None))
    kafka_password: str = field(default_factory=lambda: os.getenv("KAFKA_PASSWORD", None))
    kafka_request_timeout: str = field(default_factory=lambda: os.getenv("KAFKA_REQUEST_TIMEOUT", "30000"))
    kafka_session_timeout: str = field(default_factory=lambda: os.getenv("KAFKA_SESSION_TIMEOUT", "30000"))
    min_offset: str = field(default_factory=lambda: os.getenv("MIN_OFFSET", "1"))
    max_offset: str = field(default_factory=lambda: os.getenv("MAX_OFFSET", "2000000"))
    starting_offsets: str = field(default_factory=lambda: os.getenv("STARTING_OFFSET", "earliest"))
    s3_endpoint: str = field(default_factory=lambda: os.getenv("S3_ENDPOINT", "http://s3.teh-1.snappcloud.io"))
    s3_access_key: str = field(default_factory=lambda: os.getenv("S3_ACCESS_KEY", None))
    s3_secret_key: str = field(default_factory=lambda: os.getenv("S3_SECRET_KEY", None))
    s3_bucket_name: str = field(default_factory=lambda: os.getenv("S3_BUCKET_NAME", None))
    schema_registry_url: str = field(
        default_factory=lambda: os.getenv("SCHEMA_REGISTRY_URL", "http://schema-registry.de.data.snapp.tech:8081"))
    spark_jars: str = field(default_factory=lambda: os.getenv("SPARK_JARS",
                                                              "org.apache.spark:spark-avro_2.12:3.5.1,"
                                                              "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
                                                              "org.apache.kafka:kafka-clients:3.9.0,"
                                                              "org.apache.spark:spark-protobuf_2.12:3.5.1"))
    logger_format: str = field(default_factory=lambda: os.getenv("LOGGER_FORMAT",
                                                                 "%(asctime)s | %(name)s - %(funcName)s - %(lineno)d | %(levelname)s - %(message)s"))

    def __post_init__(self):
        """
        Post-initialization to prioritize constructor arguments over environment variables and defaults.
        """
        # Re-assign attributes here to prioritize constructor arguments
        # If an argument was passed during initialization, it will already be set by dataclass __init__
        # We only need to override with environment variables if no argument was given.
        self.kafka_broker = self._get_config('kafka_broker', self.kafka_broker)
        self.kafka_topic = self._get_config('kafka_topic', self.kafka_topic)
        self.kafka_user = self._get_config('kafka_user', self.kafka_user)
        self.kafka_password = self._get_config('kafka_password', self.kafka_password)
        self.kafka_request_timeout = self._get_config('kafka_request_timeout', self.kafka_request_timeout)
        self.kafka_session_timeout = self._get_config('kafka_session_timeout', self.kafka_session_timeout)
        self.min_offset = self._get_config('min_offset', self.min_offset)
        self.max_offset = self._get_config('max_offset', self.max_offset)
        self.starting_offsets = self._get_config('starting_offsets', self.starting_offsets)
        self.s3_endpoint = self._get_config('s3_endpoint', self.s3_endpoint)
        self.s3_access_key = self._get_config('s3_access_key', self.s3_access_key)
        self.s3_secret_key = self._get_config('s3_secret_key', self.s3_secret_key)
        self.s3_bucket_name = self._get_config('s3_bucket_name', self.s3_bucket_name)
        self.schema_registry_url = self._get_config('schema_registry_url', self.schema_registry_url)
        self.spark_jars = self._get_config('spark_jars', self.spark_jars)
        self.logger_format = self._get_config('logger_format', self.logger_format)

    def _get_config(self, key, arg_value):
        """
        Retrieves configuration, prioritizing existing attribute value (from constructor),
        then environment variables, then defaults (defined in field default_factory).
        """
        if arg_value is not None:
            return arg_value

        env_key = key.upper()
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value

        default_value = getattr(SparkSinkConfig, key).default_factory() if hasattr(SparkSinkConfig, key) and hasattr(
            getattr(SparkSinkConfig, key), 'default_factory') else None
        return default_value
