#!/bin/bash
set -e

echo "=========================================="
echo "Starting Ollama (Model Pre-loaded)"
echo "=========================================="

# Check if model is present
MODEL_NAME="${OLLAMA_MODEL:-llama3:8b}"
echo "Expected model: $MODEL_NAME"

# Start Ollama server in background
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready using ollama list command
echo "Waiting for Ollama to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  # Check if Ollama is responding by trying to list models
  if ollama list >/dev/null 2>&1; then
    echo "✓ Ollama is ready!"
    break
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "  Waiting... ($RETRY_COUNT/$MAX_RETRIES)"
  sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "⚠ Ollama took longer than expected to start"
  echo "  Continuing anyway - Ollama may still be initializing"
fi

# Verify model is available
echo "Verifying model availability..."
if ollama list 2>/dev/null | grep -q "$MODEL_NAME"; then
  echo "✓ Model $MODEL_NAME is ready (pre-loaded in image)"
else
  echo "⚠ Model $MODEL_NAME not found in image"
  echo "  Pulling model now (this should only happen once)..."
  if ollama pull "$MODEL_NAME" 2>/dev/null; then
    echo "✓ Model $MODEL_NAME pulled successfully!"
  else
    echo "⚠ Could not pull model $MODEL_NAME"
    echo "  System will continue - model may load on first use"
  fi
fi

echo "=========================================="
echo "Ollama is ready to serve requests"
echo "Model: $MODEL_NAME"
echo "Endpoint: http://localhost:11434"
echo "Process ID: $OLLAMA_PID"
echo "=========================================="

# Keep Ollama running in foreground
wait $OLLAMA_PID

# Made with Bob
