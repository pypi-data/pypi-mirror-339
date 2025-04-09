from typing import Literal, Iterator, Any
from dgkafka.errors import ConsumerNotSetError
from dglog import Logger
from confluent_kafka import Consumer, KafkaError, KafkaException, Message, TopicPartition
from confluent_kafka import OFFSET_STORED, OFFSET_BEGINNING, OFFSET_END

OffsetType = Literal[OFFSET_STORED, OFFSET_BEGINNING, OFFSET_END] | int


class KafkaConsumer:
    def __init__(self, logger_: Logger | None = None, **configs: Any) -> None:
        self.consumer: Consumer | None = None
        self.logger = logger_ if logger_ else Logger()
        self.logger.auto_configure()
        self._init_consumer(**configs)

    def _init_consumer(self, **configs: Any) -> None:
        """Internal method to initialize consumer"""
        try:
            self.consumer = Consumer(configs)
        except KafkaException as ex:
            self.logger.error(f"[x] Failed to initialize Kafka consumer: {ex}")
            raise

    def close(self) -> None:
        """Safely close the consumer"""
        if self.consumer is not None:
            try:
                self.consumer.close()
                self.logger.info("[*] Kafka consumer closed successfully")
            except KafkaException as ex:
                self.logger.error(f"[x] Error closing consumer: {ex}")
                raise
            finally:
                self.consumer = None

    def __enter__(self):
        """Context manager entry point"""
        if self.consumer is None:
            self._init_consumer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.close()

    def _ensure_consumer(self) -> Consumer:
        """Ensure consumer is initialized"""
        if self.consumer is None:
            raise ConsumerNotSetError('[!] Consumer not initialized!')
        return self.consumer

    def subscribe(self, topics: str | list[str], partition: int | None = None,
                  offset: OffsetType = OFFSET_STORED) -> None:
        """Subscribe to topics"""
        consumer = self._ensure_consumer()

        if partition is not None and offset != OFFSET_STORED:
            topic_list = [topics] if isinstance(topics, str) else topics
            for topic in topic_list:
                self._assign_topic_partition(topic, partition, offset)
        else:
            topics_list = [topics] if isinstance(topics, str) else topics
            consumer.subscribe(topics_list)
            self.logger.info(f"[*] Subscribed to topics: {topics_list}")

    def _assign_topic_partition(self, topic: str, partition: int, offset: OffsetType) -> None:
        """Assign to specific partition"""
        consumer = self._ensure_consumer()
        topic_partition = TopicPartition(topic, partition, offset)
        consumer.assign([topic_partition])
        consumer.seek(topic_partition)
        self.logger.info(f"[*] Assigned to topic '{topic}' partition {partition} with offset {offset}")

    def consume(self, num_messages: int = 1, timeout: float = 10.0, decode_utf8: bool = False) -> Iterator[Message | str]:
        """Consume messages"""
        consumer = self._ensure_consumer()

        for _ in range(num_messages):
            if (msg := self._consume(consumer, timeout)) is None:
                continue
            yield msg.value().decode('utf-8') if decode_utf8 else msg

    def _consume(self, consumer: Consumer, timeout: float) -> Message | None:
        msg = consumer.poll(timeout)
        if msg is None:
            return
        if msg.error():
            self.logger.error(f"Consumer error: {msg.error()}")
            return
        self.logger.info(f"[<] Received message from {msg.topic()} [partition {msg.partition()}, offset {msg.offset()}]")
        self.logger.debug(f"[*] Message content: {msg.value()}")
        return msg

    def commit(self, message: Message | None = None, offsets: list[TopicPartition] | None = None,
               asynchronous: bool = True) -> list[TopicPartition] | None:
        """Commit offsets to Kafka."""
        consumer = self._ensure_consumer()
        if message:
            return consumer.commit(message=message, asynchronous=asynchronous)
        elif offsets:
            return consumer.commit(offsets=offsets, asynchronous=asynchronous)
        return consumer.commit(asynchronous=asynchronous)
