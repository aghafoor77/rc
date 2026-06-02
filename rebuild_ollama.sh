#!/bin/bash
set -e

echo "=========================================="
echo "Rebuilding Ollama Container"
echo "=========================================="

echo "Step 1: Stopping Ollama container..."
docker compose stop ollama

echo "Step 2: Removing old Ollama container..."
docker compose rm -f ollama

echo "Step 3: Rebuilding Ollama image with fixes..."
docker compose build ollama

echo "Step 4: Starting Ollama container..."
docker compose up -d ollama

echo ""
echo "=========================================="
echo "Ollama Rebuild Complete!"
echo "=========================================="
echo ""
echo "Checking status..."
sleep 5
docker compose logs ollama --tail=20

echo ""
echo "To monitor Ollama startup:"
echo "  docker compose logs -f ollama"
echo ""
echo "To test Ollama:"
echo "  curl http://localhost:11435/api/tags"

# Made with Bob
