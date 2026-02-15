from fastapi import FastAPI
from src.presentation.routers import members
from src.infrastructure.db.init_db import init_db
from src.infrastructure.messaging.kafka_producer import KafkaProducer
from contextlib import asynccontextmanager
from src.presentation.dependencies import set_kafka_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting members service...")
    
    await init_db()
    print("✅ Database initialized")
    
    # Create producer
    kafka_producer = KafkaProducer(bootstrap_servers="kafka:9092")
    
    # Set it in dependencies so routes can access it
    set_kafka_producer(kafka_producer)
    
    print("✅ Members service ready\n")
    
    yield
    
    # Shutdown
    if kafka_producer:
        kafka_producer.close()
    print("✅ Members service stopped")


app = FastAPI(
    title="Members Service",
    lifespan=lifespan
)

app.include_router(members.router)
