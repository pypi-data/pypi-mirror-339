import os
from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class SparkSinkConfig:
    """Configuration container for SparkSinkConnector with dynamic fields and default values support."""
    _dynamic_fields: Dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    _dynamic_defaults: Dict[str, Any] = field(default_factory=lambda: {
        "kafka_broker": "kafka.de.data.snapp.tech:9092",
        "kafka_topic": None,
        "kafka_user": None,
        "kafka_password": None,
        "kafka_request_timeout": "30000",
        "kafka_session_timeout": "30000",
        "min_offset": "1",
        "max_offset": "2000000",
        "starting_offsets": "earliest",
        "s3_endpoint": "http://s3.teh-1.snappcloud.io",
        "s3_access_key": None,
        "s3_secret_key": None,
        "s3_bucket_name": None,
        "table_path": None,
        "checkpoint_path": None,
        "hudi_options": "TODO",
        "schema_registry_url": "http://schema-registry.de.data.snapp.tech:8081",
        "logger_format": "%(asctime)s | %(name)s - %(funcName)s - %(lineno)d | %(levelname)s - %(message)s",
        "spark_jars":  "org.apache.spark:spark-avro_2.12:3.5.1,"
                                                              "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
                                                              "org.apache.kafka:kafka-clients:3.9.0,"
                                                              "org.apache.spark:spark-protobuf_2.12:3.5.1"
    }, init=False, repr=False)

    def __init__(self, **kwargs):
        """
        Custom __init__ method to allow dynamic fields to be passed as keyword arguments.
        """
        # Explicitly initialize _dynamic_fields
        self._dynamic_fields = {}

        predefined_fields = {f.name for f in self.__dataclass_fields__.values()}
        for key, value in kwargs.items():
            if key in predefined_fields:
                setattr(self, key, value)
            else:
                self._dynamic_fields[key] = value

        # Initialize defaults for predefined fields
        for field_name in predefined_fields:
            if not hasattr(self, field_name):
                default_value = self.__dataclass_fields__[field_name].default_factory()
                setattr(self, field_name, default_value)

        # Apply defaults for dynamic fields
        for key, default_value in self._dynamic_defaults.items():
            if key not in self._dynamic_fields:
                self._dynamic_fields[key] = os.getenv(key.upper(), default_value)

    def _get_config(self, key, arg_value):
        """
        Retrieves configuration, prioritizing existing attribute value (from constructor),
        then environment variables, then defaults.
        """
        if arg_value is not None:
            return arg_value

        env_key = key.upper()
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value

        # Default values for dynamic fields
        if key in self._dynamic_defaults:
            return self._dynamic_defaults[key]

        return None

    def __getattr__(self, key):
        """
        Override __getattr__ to retrieve dynamic fields from _dynamic_fields.
        """
        if key in self._dynamic_fields:
            return self._dynamic_fields[key]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def to_dict(self):
        """
        Convert the entire configuration (predefined and dynamic fields) to a dictionary.
        """
        config = {field: getattr(self, field) for field in self.__dataclass_fields__}
        config.update(self._dynamic_fields)
        return config
