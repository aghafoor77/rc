#!/bin/bash

# EU AI Act Compliance System - Ollama Model Setup Script
# This script helps set up the required LLM model for the system

set -e

echo "=========================================="
echo "EU AI Act - Ollama Model Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running or you don't have permission to access it.${NC}"
    echo "Please start Docker or run: sudo usermod -aG docker \$USER"
    exit 1
fi

# Check if containers are running
if ! docker compose ps | grep -q "ollama"; then
    echo -e "${YELLOW}Warning: Ollama container is not running.${NC}"
    echo "Starting containers..."
    docker compose up -d ollama
    echo "Waiting for Ollama to be ready..."
    sleep 5
fi

echo "Checking available models in Ollama..."
echo ""

# List current models
echo -e "${GREEN}Currently installed models:${NC}"
docker compose exec ollama ollama list || {
    echo -e "${RED}Failed to list models. Is Ollama running?${NC}"
    exit 1
}
echo ""

# Ask user what to do
echo "What would you like to do?"
echo "1) Pull llama3:8b (recommended, ~4.7GB)"
echo "2) Pull llama3.1:8b (latest, ~4.7GB)"
echo "3) Pull llama3.2:8b (newest, ~4.7GB)"
echo "4) Pull mistral:7b (alternative, ~4.1GB)"
echo "5) Pull llama3:3b (smaller/faster, ~2GB)"
echo "6) Use rule-based classification only (no LLM)"
echo "7) Exit"
echo ""
read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        MODEL="llama3:8b"
        ;;
    2)
        MODEL="llama3.1:8b"
        ;;
    3)
        MODEL="llama3.2:8b"
        ;;
    4)
        MODEL="mistral:7b"
        ;;
    5)
        MODEL="llama3:3b"
        ;;
    6)
        echo ""
        echo -e "${GREEN}Configuring system for rule-based classification only...${NC}"
        echo "The system will automatically fall back to rule-based classification."
        echo "No model download needed."
        echo ""
        echo -e "${YELLOW}Note: Rule-based classification is less nuanced but still accurate for clear cases.${NC}"
        echo ""
        echo "Restarting backend service..."
        docker compose restart eu-ai-act-backend
        echo ""
        echo -e "${GREEN}Done! System is now using rule-based classification.${NC}"
        exit 0
        ;;
    7)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Pulling model: $MODEL${NC}"
echo "This may take several minutes depending on your internet connection..."
echo ""

# Pull the model
docker compose exec ollama ollama pull "$MODEL" || {
    echo -e "${RED}Failed to pull model. Check your internet connection.${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}Model pulled successfully!${NC}"
echo ""

# Update .env file if it exists
if [ -f .env ]; then
    echo "Updating .env file..."
    if grep -q "^LLM_MODEL=" .env; then
        sed -i "s/^LLM_MODEL=.*/LLM_MODEL=$MODEL/" .env
    else
        echo "LLM_MODEL=$MODEL" >> .env
    fi
    echo -e "${GREEN}.env file updated with LLM_MODEL=$MODEL${NC}"
else
    echo -e "${YELLOW}Warning: .env file not found. Creating from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        sed -i "s/^LLM_MODEL=.*/LLM_MODEL=$MODEL/" .env
        echo -e "${GREEN}.env file created with LLM_MODEL=$MODEL${NC}"
    else
        echo -e "${RED}Error: .env.example not found. Please create .env manually.${NC}"
    fi
fi

echo ""
echo "Restarting backend service to apply changes..."
docker compose restart eu-ai-act-backend

echo ""
echo -e "${GREEN}=========================================="
echo "Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "Model: $MODEL"
echo "Status: Ready"
echo ""
echo "Verifying setup..."
sleep 3

# Check logs
echo ""
echo "Recent backend logs:"
docker compose logs --tail=20 eu-ai-act-backend | grep -i "llm\|initialized" || true

echo ""
echo -e "${GREEN}All done! Your system is now ready to use LLM-based classification.${NC}"
echo ""
echo "To verify, check the logs with:"
echo "  docker compose logs -f eu-ai-act-backend"
echo ""

# Made with Bob
