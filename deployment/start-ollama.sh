#!/bin/bash
set -e

echo "=========================================="
echo "Starting Ollama with automatic model setup"
echo "=========================================="

# Start Ollama server in background
echo "[1/4] Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "[2/4] Waiting for Ollama to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "✓ Ollama is ready!"
    break
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "  Waiting... ($RETRY_COUNT/$MAX_RETRIES)"
  sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "✗ Failed to start Ollama after $MAX_RETRIES attempts"
  exit 1
fi

# Check if model exists
MODEL_NAME="${OLLAMA_MODEL:-llama3:8b}"
echo "[3/4] Checking for model: $MODEL_NAME"

if ollama list | grep -q "$MODEL_NAME"; then
  echo "✓ Model $MODEL_NAME already exists"
else
  echo "⚠ Model $MODEL_NAME not found. Pulling..."
  echo "  This may take 5-10 minutes (downloading ~4.7GB)"
  echo "  Please be patient..."
  
  if ollama pull "$MODEL_NAME"; then
    echo "✓ Model $MODEL_NAME pulled successfully!"
  else
    echo "✗ Failed to pull model $MODEL_NAME"
    echo "  You can manually pull it later with:"
    echo "  docker compose exec ollama ollama pull $MODEL_NAME"
    # Don't exit - let Ollama run without the model
  fi
fi

# Verify model is available
echo "[4/4] Verifying model availability..."
if ollama list | grep -q "$MODEL_NAME"; then
  echo "✓ Model $MODEL_NAME is ready to use"
else
  echo "⚠ Model $MODEL_NAME not available yet"
  echo "  System will use rule-based classification as fallback"
fi

echo "=========================================="
echo "Ollama is ready to serve requests"
echo "Model: $MODEL_NAME"
echo "Endpoint: http://localhost:11434"
echo "=========================================="

# Keep Ollama running in foreground
wait $OLLAMA_PID

# Made with Bob
