from fastapi import FastAPI
from src.presentation.routers import books
from src.infrastructure.db.init_db import init_db
from contextlib import asynccontextmanager
from src.infrastructure.messaging.kafka_consumer import KafkaConsumerService
from src.infrastructure.repositories.member_repo_sql import MemberRepositorySQL
import threading


consumer_service = None
consumer_thread = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting books service...")
    
    try:
        await init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database init failed: {e}")
        raise
    
    try:
        # Create repository - it creates its own sessions
        member_repo = MemberRepositorySQL()
        print(f"✅ Member repository created: {member_repo}")
        
        # Initialize consumer
        global consumer_service, consumer_thread
        consumer_service = KafkaConsumerService(member_repo, bootstrap_servers="kafka:9092")
        print(f"✅ Consumer service created: {consumer_service}")
        
        # Start consumer in thread (Kafka consumer is blocking)
        consumer_thread = threading.Thread(
            target=consumer_service.start,
            daemon=True,
            name="KafkaConsumerThread"
        )
        consumer_thread.start()
        print("✅ Kafka consumer thread started")
        
        # Give thread a moment to start
        import time
        time.sleep(1)
        
        if consumer_thread.is_alive():
            print("✅ Consumer thread is running")
        else:
            print("⚠️  WARNING: Consumer thread died immediately")
        
        print("✅ Books service ready\n")
        
    except Exception as e:
        print(f"❌ Consumer initialization failed: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    yield
    
    # Shutdown
    print("🔄 Shutting down books service...")
    if consumer_service:
        consumer_service.stop()
    print("✅ Books service stopped")


app = FastAPI(
    title="Books Service",
    lifespan=lifespan
)

app.include_router(books.router)
