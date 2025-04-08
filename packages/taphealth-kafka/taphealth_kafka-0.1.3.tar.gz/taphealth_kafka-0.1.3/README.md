# TapHealth Kafka

A Python library for working with Kafka in TapHealth services. This library provides abstractions over kafka-python to simplify producing and consuming Kafka messages.

## Installation

```bash
pip install taphealth-kafka
```

## Usage

### Connecting to Kafka

```python
from taphealth_kafka import KafkaClient

# Initialize the client
kafka_client = KafkaClient()

# Connect to Kafka brokers
kafka_client.connect(["localhost:9092"])
```

### Producing Messages

```python
from taphealth_kafka import KafkaProducer, Topics
from taphealth_kafka.events import ActivityLoggedEvent
from taphealth_kafka.types import ActivityType
from datetime import datetime

# Create a producer class
class ActivityLoggedProducer(KafkaProducer):
    @property
    def topic(self):
        return Topics.ACTIVITY_LOGGED

# Initialize the producer
producer = ActivityLoggedProducer(kafka_client)

# Send a message
producer.send({
    "userId": "user123",
    "date": datetime.now().isoformat(),
    "activityType": ActivityType.MEAL_LOGGING,
    "loggedAt": datetime.now().isoformat(),
    "mealType": "lunch",
    "hadHealthy": True
})
```

### Consuming Messages

```python
from taphealth_kafka import KafkaConsumer, Topics

# Create a consumer class
class ActivityLoggedConsumer(KafkaConsumer):
    @property
    def topic(self):
        return Topics.ACTIVITY_LOGGED

    @property
    def group_id(self):
        return "activity-processor-group"

    def on_message(self, data, message):
        # Process the message
        print(f"Received activity log: {data}")
        # Implement your business logic here

# Initialize and start the consumer
consumer = ActivityLoggedConsumer(kafka_client)
consumer.consume()  # This will start listening in a blocking manner
```

## Example Service Integration

```python
import threading
from taphealth_kafka import KafkaClient, Topics
from taphealth_kafka.events import ActivityLoggedEvent

# Setup logging
logger = logging.getLogger(__name__)

# Initialize Kafka
kafka_client = KafkaClient()
kafka_client.connect(["kafka-broker:9092"])

# Producer example
class ActivityProducer(KafkaProducer):
    @property
    def topic(self):
        return Topics.ACTIVITY_LOGGED

# Consumer example
class ActivityConsumer(KafkaConsumer):
    @property
    def topic(self):
        return Topics.ACTIVITY_LOGGED

    @property
    def group_id(self):
        return "activity-service"

    def on_message(self, data, message):
        logger.info(f"Processing activity: {data}")
        # Your business logic here

# Start consumer in a separate thread
def start_consumer():
    consumer = ActivityConsumer(kafka_client)
    consumer.consume()

consumer_thread = threading.Thread(target=start_consumer)
consumer_thread.daemon = True
consumer_thread.start()

# Use producer in your API endpoints
producer = ActivityProducer(kafka_client)

def log_activity(user_id, activity_data):
    producer.send({
        "userId": user_id,
        **activity_data
    })
    return {"status": "activity logged"}
