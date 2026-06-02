#!/bin/bash
set -e

echo "=========================================="
echo "Starting Ollama (Simple Mode)"
echo "=========================================="

MODEL_NAME="${OLLAMA_MODEL:-llama3:8b}"
echo "Model: $MODEL_NAME"
echo "Starting Ollama server..."

# Just start Ollama and let it run
# Health checks will be handled by Docker
exec ollama serve

# Made with Bob
