import json
import logging
from abc import ABC, abstractmethod
from typing import Any

from .topics import Topics

logger = logging.getLogger(__name__)

class KafkaConsumer(ABC):
    def __init__(self, client):
        self.client = client

    @property
    @abstractmethod
    def topic(self) -> Topics:
        pass

    @property
    @abstractmethod
    def group_id(self) -> str:
        pass

    @abstractmethod
    def on_message(self, data: Any, message: Any) -> None:
        pass

    def consume(self):
        consumer = self.client.create_consumer(
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

        consumer.subscribe([self.topic.value])
        logger.info(f"Started consuming from topic {self.topic.value}")

        try:
            for message in consumer:
                logger.info(f"Received message on topic {self.topic.value} "
                            f"and partition {message.partition}")
                data = message.value
                self.on_message(data, message)

        except KeyboardInterrupt:
            logger.info("Stopping consumer due to keyboard interrupt")
        except Exception as e:
            logger.error(f"Error consuming message: {str(e)}")
        finally:
            consumer.close()
            logger.info("Consumer closed")
