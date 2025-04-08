import logging
from typing import List

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka import KafkaProducer, KafkaConsumer
from .topics import Topics

logger = logging.getLogger(__name__)

class KafkaClient:
    def __init__(self):
        self._admin = None
        self._producer = None
        self._consumer = None
        self._connected = False
        self._bootstrap_servers = []

    @property
    def bootstrap_servers(self):
        if not self._connected:
            raise ValueError("Cannot access bootstrap servers until connected")
        return self._bootstrap_servers

    @property
    def admin(self):
        if not self._connected:
            raise ValueError("Cannot access admin client until connected")
        return self._admin

    @property
    def producer(self):
        if not self._connected:
            self._producer = KafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda x: x.encode('utf-8')
            )
        return self._producer

    def create_consumer(self, group_id, **kwargs):
        if not self._connected:
            raise ValueError("Cannot create consumer until connected")
        self._consumer = KafkaConsumer(
            bootstrap_servers=self._bootstrap_servers,
            group_id=group_id,
            **kwargs
        )
        return self._consumer

    def connect(self, bootstrap_servers: List[str]):
        try:
            self._bootstrap_servers = bootstrap_servers
            self._admin = KafkaAdminClient(
                bootstrap_servers=bootstrap_servers,
                client_id="taphealth-kafka-admin"
            )
            self._connected = True

            topics = [topic.value for topic in Topics]
            self.create_topics(topics)

            logger.info(f"Connected to Kafka cluster at {bootstrap_servers}")
        except Exception as e:
            logger.error(f"Error connecting to Kafka cluster: {e}")
            raise

    def create_topics(self, topics: List[str]):
        if not self._connected or self._admin is None:
            raise ValueError("Cannot create topics: not connected to Kafka")

        try:
            existing_topics = self._admin.list_topics()
            topics_to_create = [topic for topic in topics if topic not in existing_topics]

            if not topics_to_create:
                logger.info("All topics already exist")
                return

            new_topics = [
            NewTopic(name=topic, num_partitions=1,
                replication_factor=1)
            for topic in topics_to_create
            ]

            self._admin.create_topics(new_topics)
            logger.info(f"Created topics: {topics_to_create}")
        except TopicAlreadyExistsError:
            logger.info("Topics already exist")
        except Exception as e:
            logger.error(f"Error creating topics: {e}")
            raise

    def disconnect(self):
        if self._producer:
            self._producer.close()
            self._producer = None

        if self._admin:
            self._admin.close()
            self._admin = None

        self._connected = False
        logger.info("Disconnected from Kafka")
