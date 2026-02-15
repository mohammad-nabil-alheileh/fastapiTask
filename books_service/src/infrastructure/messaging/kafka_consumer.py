# src/infrastructure/kafka/consumer.py
import json
import time
from uuid import UUID
from confluent_kafka import Consumer, KafkaException
from src.domain.library.entities.member import Member
from concurrent.futures import ThreadPoolExecutor
import asyncio


class KafkaConsumerService:
    """Simple, reliable Kafka consumer for member events."""

    def __init__(self, member_repo, bootstrap_servers: str = "kafka:9092"):
        self.member_repo = member_repo
        self.bootstrap_servers = bootstrap_servers
        self.topic = "member-created"
        self.group_id = "books-member-consumer-group"
        self.running = False
        self.consumer = None
        # Thread pool for handling async operations
        self.executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="AsyncHandler")
        
        print(f"✅ Consumer service initialized")
        print(f"   Bootstrap: {self.bootstrap_servers}")
        print(f"   Topic: {self.topic}")
        print(f"   Group: {self.group_id}")

    def _initialize_consumer(self):
        """Initialize Kafka consumer with minimal, reliable configuration."""
        config = {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": self.group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
            "auto.commit.interval.ms": 5000,
        }

        try:
            self.consumer = Consumer(config)
            print(f"✅ Kafka consumer initialized")
        except KafkaException as e:
            print(f"❌ Failed to initialize consumer: {e}")
            raise

    def _wait_for_topic(self, timeout: int = 60):
        """Wait for topic to be available."""
        from confluent_kafka.admin import AdminClient
        
        admin = AdminClient({"bootstrap.servers": self.bootstrap_servers})
        start = time.time()

        print(f"⏳ Waiting for topic '{self.topic}'...")
        
        while time.time() - start < timeout:
            try:
                metadata = admin.list_topics(timeout=5)
                if self.topic in metadata.topics:
                    print(f"✅ Topic '{self.topic}' is ready")
                    return True
            except:
                pass
            
            time.sleep(2)

        print(f"❌ Topic not available after {timeout}s")
        return False

    def _run_async_in_thread(self, member_id: UUID):
        """
        Run async operation in a separate thread with its own event loop.
        This is the worker function for the thread pool.
        """
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Run the async operation
            result = loop.run_until_complete(self._handle_member_async(member_id))
            return result
        finally:
            loop.close()

    async def _handle_member_async(self, member_id: UUID):
        """Handle member-created event - async version."""
        try:
            print(f"🔍 Checking if member exists: {member_id}")
            existing = await self.member_repo.get_by_id(member_id)

            if not existing:
                print(f"💾 Creating member: {member_id}")
                member = Member(id=member_id)
                await self.member_repo.create(member)
                print(f"✅ Member created: {member_id}")
            else:
                print(f"ℹ️  Member already exists: {member_id}")
                
        except Exception as e:
            print(f"❌ Error in async handler: {e}")
            import traceback
            traceback.print_exc()

    def start(self):
        """Start consuming messages."""
        print("🔥 Starting Kafka consumer...")
        self.running = True

        try:
            # Wait for topic
            if not self._wait_for_topic():
                return

            # Initialize consumer
            self._initialize_consumer()

            # Subscribe
            self.consumer.subscribe([self.topic])
            print(f"✅ Subscribed to '{self.topic}'")
            print("⏳ Waiting for messages...")

            messages_processed = 0

            while self.running:
                try:
                    msg = self.consumer.poll(timeout=1.0)

                    if msg is None:
                        continue

                    if msg.error():
                        print(f"❌ Kafka error: {msg.error()}")
                        continue

                    # Process message
                    print(f"\n📥 Message received")
                    print(f"   Partition: {msg.partition()}, Offset: {msg.offset()}")

                    try:
                        event = json.loads(msg.value().decode('utf-8'))
                        member_id = UUID(event["member_id"])
                        
                        print(f"   Member ID: {member_id}")
                        
                        # Submit to thread pool and wait for completion
                        future = self.executor.submit(self._run_async_in_thread, member_id)
                        # Wait for the result (blocking, but that's OK in consumer thread)
                        future.result(timeout=30)
                        
                        messages_processed += 1
                        print(f"✅ Processed (total: {messages_processed})\n")

                    except (json.JSONDecodeError, KeyError, ValueError) as e:
                        print(f"❌ Invalid message: {e}")
                    except Exception as e:
                        print(f"❌ Error processing message: {e}")
                        import traceback
                        traceback.print_exc()

                except KeyboardInterrupt:
                    print("\n⚠️  Interrupted")
                    break
                except Exception as e:
                    print(f"❌ Error in loop: {e}")
                    time.sleep(5)

        except Exception as e:
            print(f"❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()

    def stop(self):
        """Stop the consumer."""
        print("🔄 Stopping consumer...")
        self.running = False

        if self.consumer:
            try:
                self.consumer.close()
                print("✅ Consumer closed")
            except Exception as e:
                print(f"⚠️  Error closing: {e}")
        
        if self.executor:
            print("🔄 Shutting down thread pool...")
            self.executor.shutdown(wait=True, cancel_futures=False)
            print("✅ Thread pool closed")