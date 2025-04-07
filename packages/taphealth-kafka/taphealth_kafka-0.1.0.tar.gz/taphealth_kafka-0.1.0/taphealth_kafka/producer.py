import json
import logging
from abc import ABC, abstractmethod
from .topics import Topics

logger = logging.getLogger(__name__)

class KafkaProducer(ABC):
    def __init__(self, client):
        self.client = client
        self._producer = client.producer

    @property
    @abstractmethod
    def topic(self) -> Topics:
        pass

    def send(self, data):
        try:
            serialized_data = json.dumps(data, default=self._json_serializer)
            future = self._producer.send(
                self.topic.value,
                value=serialized_data
            )

            # Block until the message is sent (or timeout)
            future.get(timeout=10)
            logger.info(f"Data sent to Kafka topic {self.topic.value}")
        except Exception as e:
            logger.error(f"Error sending data to Kafka: {str(e)}")
            raise

    def _json_serializer(self, obj):
        """Custom JSON serializer for objects not serializable by default json module"""
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
