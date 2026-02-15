#!/bin/bash

set -e  # Exit on any error

echo "=========================================="
echo "COMPLETE REBUILD AND TEST"
echo "=========================================="
echo ""

echo "Step 1: Stop everything"
echo "------------------------------------------"
docker compose -f docker-compose.services.yml down
docker compose -f docker-compose.infra.yml down
echo "✅ Stopped all services"
echo ""

echo "Step 2: Remove old images"
echo "------------------------------------------"
docker rmi fastapiTask-books_service fastapiTask-members_service 2>/dev/null || echo "Images not found (OK)"
echo "✅ Removed old images"
echo ""

echo "Step 3: Start infrastructure"
echo "------------------------------------------"
docker compose -f docker-compose.infra.yml up -d
echo "Waiting 30 seconds for Kafka to be ready..."
sleep 30
echo "✅ Infrastructure started"
echo ""

echo "Step 4: Verify Kafka is ready"
echo "------------------------------------------"
docker exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
echo "✅ Kafka is responding"
echo ""

echo "Step 5: Build services with NO CACHE"
echo "------------------------------------------"
docker compose -f docker-compose.services.yml build --no-cache --progress=plain
echo "✅ Services built"
echo ""

echo "Step 6: Start services"
echo "------------------------------------------"
docker compose -f docker-compose.services.yml up -d
echo "Waiting 15 seconds for services to start..."
sleep 15
echo "✅ Services started"
echo ""

echo "Step 7: Check books_service logs"
echo "------------------------------------------"
echo "Looking for consumer initialization..."
docker logs books_service 2>&1 | head -50
echo ""

echo "Step 8: Verify consumer is running"
echo "------------------------------------------"
if docker logs books_service 2>&1 | grep -q "🔥 Starting Kafka consumer"; then
    echo "✅ CONSUMER IS STARTING!"
else
    echo "❌ CONSUMER NOT STARTING - checking for errors..."
    docker logs books_service 2>&1 | grep -E "(Error|error|Exception|Traceback|Failed)" | head -20
fi
echo ""

echo "Step 9: Create a test member"
echo "------------------------------------------"
RESPONSE=$(curl -s -X POST http://localhost:8002/members/ \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Test $(date +%s)\", \"email\": \"test$(date +%s)@example.com\"}")

echo "API Response:"
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo ""

echo "Step 10: Wait and check for message processing"
echo "------------------------------------------"
echo "Waiting 5 seconds for message to be processed..."
sleep 5

echo ""
echo "Members service producer logs:"
docker logs members_service 2>&1 | tail -10 | grep -E "(Sending|Delivered|member-created)" || echo "No producer activity"

echo ""
echo "Books service consumer logs:"
docker logs books_service 2>&1 | tail -20 | grep -E "(Message received|Member|Processed)" || echo "No consumer activity"
echo ""

echo "Step 11: Check Kafka directly"
echo "------------------------------------------"
echo "Messages in topic:"
docker exec kafka timeout 3 /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic member-created \
  --from-beginning 2>&1 | head -10 || echo "No messages or timeout"
echo ""

echo "Step 12: Final status"
echo "------------------------------------------"
echo "Container status:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "NAMES|members_service|books_service|kafka"
echo ""

echo "Books service health:"
curl -s http://localhost:8001/health | python3 -m json.tool 2>/dev/null || echo "Service not responding"
echo ""

echo "Members service health:"
curl -s http://localhost:8002/health | python3 -m json.tool 2>/dev/null || echo "Service not responding"
echo ""

echo "=========================================="
echo "REBUILD COMPLETE"
echo "=========================================="
echo ""
echo "If consumer is STILL not working, please share:"
echo "1. The output above"
echo "2. docker logs books_service (full)"
echo "3. docker exec books_service ls -la /app/src/"
