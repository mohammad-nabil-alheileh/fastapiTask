from src.application.library.member_service import MemberService
from src.infrastructure.repositories.member_repo_sql import MemberRepositorySQL
from fastapi import Depends


# Global producer instance - set by main.py during startup
_kafka_producer = None


def set_kafka_producer(producer):
    """Called by main.py to set the global producer instance."""
    global _kafka_producer
    _kafka_producer = producer
    print(f"✅ Kafka producer set in dependencies: {producer}")


def get_kafka_producer():
    """Dependency to inject Kafka producer into routes."""
    if _kafka_producer is None:
        raise RuntimeError("Kafka producer not initialized. Check startup logs.")
    return _kafka_producer


def get_kafka_producer_status():
    """Check if producer is initialized (for health checks)."""
    return "connected" if _kafka_producer else "disconnected"


def get_member_service(
    kafka_producer = Depends(get_kafka_producer)
) -> MemberService:
    """Dependency to get member service with all dependencies injected."""
    member_repo = MemberRepositorySQL()
    return MemberService(member_repo, kafka_producer)