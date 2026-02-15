import json
import atexit
from confluent_kafka import Producer, KafkaException
from uuid import UUID


class KafkaProducer:
    """Simple, reliable Kafka producer for member events."""

    def __init__(self, bootstrap_servers: str = "kafka:9092"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = "member-created"
        self.producer = None
        self._initialize_producer()
        atexit.register(self.close)

    def _initialize_producer(self):
        """Initialize Kafka producer with minimal, reliable configuration."""
        config = {
            "bootstrap.servers": self.bootstrap_servers,
            "acks": "1",  # Wait for leader acknowledgment only
            "retries": 3,
            "retry.backoff.ms": 300,
        }

        try:
            self.producer = Producer(config)
            print(f"✅ Kafka producer initialized")
            print(f"   Bootstrap: {self.bootstrap_servers}")
            print(f"   Topic: {self.topic}")
        except KafkaException as e:
            print(f"❌ Failed to initialize producer: {e}")
            raise

    def _delivery_callback(self, err, msg):
        """Callback for delivery confirmation."""
        if err:
            print(f"❌ Delivery FAILED: {err}")
        else:
            print(f"✅ Delivered to {msg.topic()} [partition {msg.partition()}] at offset {msg.offset()}")

    def send_member_created(self, member_id: UUID) -> bool:
        """Send member-created event to Kafka."""
        if not self.producer:
            print("❌ Producer not initialized")
            return False

        event = {"member_id": str(member_id)}
        
        print(f"📤 Sending member-created event: {member_id}")

        try:
            self.producer.produce(
                topic=self.topic,
                key=str(member_id).encode('utf-8'),
                value=json.dumps(event).encode('utf-8'),
                callback=self._delivery_callback
            )

            # Trigger callbacks
            self.producer.poll(0)

            # Wait for delivery
            remaining = self.producer.flush(timeout=5)
            
            if remaining > 0:
                print(f"⚠️  {remaining} message(s) not delivered")
                return False
            
            return True

        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False

    def close(self):
        """Close the producer."""
        if self.producer:
            print("🔄 Closing Kafka producer...")
            self.producer.flush(timeout=10)
            self.producer = None
            print("✅ Producer closed")
