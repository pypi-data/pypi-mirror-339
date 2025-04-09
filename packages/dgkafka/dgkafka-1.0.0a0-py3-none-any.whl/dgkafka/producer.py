import uuid
from typing import Optional, Any
from dglog import Logger
from confluent_kafka import Producer, Message
from dgkafka.errors import ProducerNotSetError


class KafkaProducer:
    def __init__(self, logger_: Logger | None = None, **configs: Any) -> None:
        """Initialize Kafka producer.

        Args:
            logger_: Optional logger instance
            configs: Kafka producer configuration
        """
        self.producer: Producer | None = None
        self.logger = logger_ if logger_ else Logger()
        self.logger.auto_configure()
        self._init_producer(**configs)

    def _init_producer(self, **configs: Any) -> None:
        """Internal method to initialize producer."""
        try:
            self.producer = Producer(configs)
            self.logger.info("[*] Kafka producer initialized successfully")
        except Exception as ex:
            self.logger.error(f"[x] Failed to initialize producer: {ex}")
            raise

    def close(self) -> None:
        """Close the producer connection."""
        if self.producer is not None:
            try:
                self.producer.flush()
                self.logger.info("[*] Producer closed successfully")
            except Exception as ex:
                self.logger.error(f"[x] Error closing producer: {ex}")
                raise
            finally:
                self.producer = None

    def __enter__(self):
        """Context manager entry point."""
        if self.producer is None:
            self._init_producer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.close()

    def _ensure_producer(self) -> Producer:
        """Ensure producer is initialized."""
        if self.producer is None:
            raise ProducerNotSetError('[!] Producer not initialized!')
        return self.producer

    def delivery_report(self, err: Optional[Any], msg: Message) -> None:
        """Delivery callback for produced messages.

        Args:
            err: Error object if delivery failed
            msg: Delivered message object
        """
        if err is not None:
            self.logger.error(f"[x] Message delivery failed: {err}")
            self.logger.debug(f"[~] Failed message details: {msg}")
        else:
            self.logger.info(f"[>] Message delivered to {msg.topic()} [partition {msg.partition()}, offset {msg.offset()}]")

    def produce(
            self,
            topic: str,
            message: str | bytes | dict[str, Any],
            key: str | None = None,
            partition: int | None = None,
            headers: dict[str, bytes] | None = None,
            flush: bool = True
    ) -> None:
        """Produce a message to Kafka.

        Args:
            topic: Target topic name
            message: Message content (str, bytes or dict)
            key: Message key (optional)
            partition: Specific partition (optional)
            headers: Message headers (optional)
            flush: Immediately flush after producing (default: True)
        """
        producer = self._ensure_producer()
        producer.poll(0)

        # Generate key if not provided
        key = key if key is not None else str(uuid.uuid4())
        key_bytes = key.encode('utf-8')

        # Prepare message value
        if isinstance(message, str):
            value = message.encode('utf-8')
        elif isinstance(message, bytes):
            value = message
        else:  # Assume dict-like object
            try:
                import json
                value = json.dumps(message).encode('utf-8')
            except Exception as ex:
                self.logger.error(f"[x] Failed to serialize message: {ex}")
                raise

        # Prepare message headers
        headers_list = None
        if headers:
            headers_list = [(k, v if isinstance(v, bytes) else str(v).encode('utf-8'))
                            for k, v in headers.items()]

        # Produce message
        try:
            producer.produce(
                topic=topic,
                value=value,
                key=key_bytes,
                partition=partition,
                on_delivery=self.delivery_report,
                headers=headers_list
            )

            if flush:
                producer.flush()

        except Exception as ex:
            self.logger.error(f"[x] Failed to produce message: {ex}")
            raise

    def flush(self, timeout: float = 10.0) -> None:
        """Wait for all messages to be delivered.

        Args:
            timeout: Maximum time to wait (seconds)
        """
        producer = self._ensure_producer()
        try:
            remaining = producer.flush(timeout)
            if remaining > 0:
                self.logger.warning(f"[!] {remaining} messages remain undelivered after flush timeout")
        except Exception as ex:
            self.logger.error(f"[x] Flush failed: {ex}")
            raise