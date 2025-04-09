from typing import Optional, Union, Dict, Any
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

from dglog import Logger

from dgkafka.producer import KafkaProducer


class AvroKafkaProducer(KafkaProducer):
    """Kafka producer with Avro schema support using Schema Registry."""

    def __init__(
            self,
            schema_registry_url: str,
            default_key_schema: Optional[Dict[str, Any]] = None,
            default_value_schema: Optional[Dict[str, Any]] = None,
            logger_: Optional[Logger] = None,
            **configs: Any
    ) -> None:
        """
        Initialize Avro producer.

        Args:
            schema_registry_url: URL of Schema Registry
            default_key_schema: Default Avro schema for message keys
            default_value_schema: Default Avro schema for message values
            logger_: Optional logger instance
            configs: Kafka producer configuration
        """
        self.schema_registry_url = schema_registry_url
        self.default_key_schema = default_key_schema
        self.default_value_schema = default_value_schema
        self.schema_registry_client = CachedSchemaRegistryClient({'url': schema_registry_url})
        super().__init__(logger_=logger_, **configs)

    def _init_producer(self, **configs: Any) -> None:
        """Initialize AvroProducer instance."""
        try:
            # AvroProducer requires schema registry in config
            configs['schema.registry.url'] = self.schema_registry_url
            self.producer = AvroProducer(
                config=configs,
                default_key_schema=self.default_key_schema,
                default_value_schema=self.default_value_schema
            )
            self.logger.info("Avro producer initialized successfully")
        except Exception as ex:
            self.logger.error(f"Failed to initialize Avro producer: {ex}")
            raise

    def produce(
            self,
            topic: str,
            value: Union[Dict[str, Any], Any],
            key: Optional[Union[Dict[str, Any], str]] = None,
            value_schema: Optional[Dict[str, Any]] = None,
            key_schema: Optional[Dict[str, Any]] = None,
            partition: Optional[int] = None,
            headers: Optional[Dict[str, bytes]] = None,
            flush: bool = True
    ) -> None:
        """
        Produce Avro-encoded message to Kafka.

        Args:
            topic: Target topic name
            value: Message value (must match Avro schema)
            key: Message key (optional)
            value_schema: Avro schema for message value (optional)
            key_schema: Avro schema for message key (optional)
            partition: Specific partition (optional)
            headers: Message headers (optional)
            flush: Immediately flush after producing (default: True)
        """
        producer = self._ensure_producer()
        producer.poll(0)

        # Prepare headers
        headers_list = None
        if headers:
            headers_list = [(k, v if isinstance(v, bytes) else str(v).encode('utf-8'))
                            for k, v in headers.items()]

        try:
            producer.produce(
                topic=topic,
                value=value,
                value_schema=value_schema,
                key=key,
                key_schema=key_schema,
                partition=partition,
                on_delivery=self.delivery_report,
                headers=headers_list
            )

            if flush:
                producer.flush()

        except SerializerError as ex:
            self.logger.error(f"Avro serialization failed: {ex}")
            raise
        except Exception as ex:
            self.logger.error(f"Failed to produce Avro message: {ex}")
            raise

    def get_schema(self, subject: str, version: int = 1) -> Dict[str, Any]:
        """Get Avro schema from Schema Registry."""
        return self.schema_registry_client.get_schema(subject, version)

    def get_latest_schema(self, subject: str) -> Dict[str, Any]:
        """Get latest version of schema for given subject."""
        return self.schema_registry_client.get_latest_schema(subject)[1]