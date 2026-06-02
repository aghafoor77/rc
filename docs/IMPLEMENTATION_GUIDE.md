# EU AI Act Compliance System - Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing and deploying the EU AI Act Compliance Assessment System.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [RAG System Initialization](#rag-system-initialization)
6. [Running the System](#running-the-system)
7. [Testing](#testing)
8. [Production Deployment](#production-deployment)
9. [Monitoring](#monitoring)
10. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### System Requirements

- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **RAM**: 16GB minimum (32GB recommended)
- **Storage**: 50GB free space
- **CPU**: 4+ cores
- **GPU**: Optional (NVIDIA GPU for faster LLM inference)

### Software Requirements

- Python 3.11+
- Docker 20.10+
- Docker Compose 2.0+
- Conda (Anaconda or Miniconda)
- Git
- Ollama (for local LLM deployment)

---

## 2. Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/your-org/eu-ai-act-compliance-system.git
cd eu-ai-act-compliance-system
```

### Step 2: Create Conda Environment

```bash
# Create environment
conda create -n eu-ai-act python=3.11 -y

# Activate environment
conda activate eu-ai-act

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install Ollama

#### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### macOS
```bash
brew install ollama
```

#### Windows (WSL2)
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 4: Download Llama 3 Model

```bash
# Download Llama 3 8B (recommended)
ollama pull llama3:8b

# Or download Llama 3 70B (requires more resources)
# ollama pull llama3:70b
```

---

## 3. Configuration

### Step 1: Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env
```

### Step 2: Key Configuration Items

Update the following in `.env`:

```bash
# Database password
POSTGRES_PASSWORD=your_secure_password_here

# Secret key for JWT
SECRET_KEY=your_secret_key_here

# CORS origins (adjust for your frontend)
CORS_ORIGINS=http://localhost:3000,https://your-domain.com

# LLM model
LLM_MODEL=llama3:8b

# Ollama URL
OLLAMA_BASE_URL=http://localhost:11434
```

### Step 3: Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 4. Database Setup

### Option A: Using Docker Compose

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Wait for services to be ready
docker-compose ps
```

### Option B: Local Installation

#### PostgreSQL

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE eu_ai_act_db;
CREATE USER ai_compliance_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE eu_ai_act_db TO ai_compliance_user;
\q
```

#### Redis

```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
```

### Step 4: Run Database Migrations

```bash
# Initialize database schema
python backend/database/init_db.py
```

---

## 5. RAG System Initialization

### Step 1: Prepare Legal Corpus

```bash
# Create legal corpus directory
mkdir -p data/legal_corpus

# Add EU AI Act documents (PDF, TXT, or HTML)
# Place documents in data/legal_corpus/
```

### Step 2: Load Legal Documents into Vector Store

```bash
# Run corpus loader
python backend/rag/load_legal_corpus.py
```

This will:
- Parse legal documents
- Generate embeddings
- Store in ChromaDB
- Create searchable index

### Step 3: Verify RAG System

```bash
# Test RAG retrieval
python backend/rag/test_rag.py
```

---

## 6. Running the System

### Development Mode

#### Option A: Direct Python

```bash
# Activate conda environment
conda activate eu-ai-act

# Start Ollama (in separate terminal)
ollama serve

# Start FastAPI backend
cd backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option B: Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Production Mode

```bash
# Build and start all services
docker-compose -f docker-compose.yml up -d

# Scale backend workers
docker-compose up -d --scale backend=3

# View status
docker-compose ps
```

---

## 7. Testing

### Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_rule_engine.py
```

### Integration Tests

```bash
# Run integration tests
pytest tests/integration/

# Test API endpoints
pytest tests/integration/test_api.py
```

### Manual Testing

#### Test Classification Endpoint

```bash
curl -X POST "http://localhost:8000/api/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Credit Scoring System",
      "sector": "banking",
      "purpose": "creditworthiness_assessment",
      "deployer_type": "private_company",
      "autonomy_level": "fully_automated",
      "affects_individuals": true,
      "impacts_financial_access": true
    },
    "use_rag": true,
    "use_llm": true
  }'
```

#### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

---

## 8. Production Deployment

### Step 1: Security Hardening

```bash
# Update passwords
# Generate strong SECRET_KEY
# Configure HTTPS/TLS
# Set up firewall rules
# Enable rate limiting
```

### Step 2: SSL/TLS Configuration

```bash
# Install certbot
sudo apt-get install certbot

# Obtain SSL certificate
sudo certbot certonly --standalone -d your-domain.com

# Update nginx configuration
# Point to SSL certificates
```

### Step 3: Deploy with Docker Compose

```bash
# Pull latest images
docker-compose pull

# Build and start
docker-compose up -d

# Verify deployment
docker-compose ps
curl https://your-domain.com/health
```

### Step 4: Set Up Reverse Proxy (Nginx)

```nginx
# /etc/nginx/sites-available/eu-ai-act

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 5: Configure Systemd Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/eu-ai-act.service
```

```ini
[Unit]
Description=EU AI Act Compliance System
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/eu-ai-act-compliance-system
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable eu-ai-act
sudo systemctl start eu-ai-act
```

---

## 9. Monitoring

### Prometheus Metrics

Access Prometheus at: `http://localhost:9090`

Key metrics:
- API request rate
- Response times
- Error rates
- Classification accuracy
- LLM token usage
- Database query performance

### Grafana Dashboards

Access Grafana at: `http://localhost:3001`

Default credentials:
- Username: `admin`
- Password: Set in `.env` (GRAFANA_PASSWORD)

### Application Logs

```bash
# View backend logs
docker-compose logs -f backend

# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f ollama
```

### Health Checks

```bash
# Check all services
curl http://localhost:8000/health

# Check statistics
curl http://localhost:8000/api/v1/stats
```

---

## 10. Troubleshooting

### Common Issues

#### Issue: Ollama Connection Failed

**Solution:**
```bash
# Check Ollama status
ollama list

# Restart Ollama
sudo systemctl restart ollama

# Check logs
journalctl -u ollama -f
```

#### Issue: Database Connection Error

**Solution:**
```bash
# Check PostgreSQL status
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

#### Issue: ChromaDB Initialization Failed

**Solution:**
```bash
# Clear vector store
rm -rf data/vector_store/*

# Reinitialize
python backend/rag/load_legal_corpus.py
```

#### Issue: Out of Memory

**Solution:**
```bash
# Use smaller LLM model
ollama pull llama3:8b  # Instead of 70b

# Reduce batch size in configuration
# Increase Docker memory limit
```

#### Issue: Slow Classification

**Solution:**
```bash
# Enable GPU acceleration (if available)
# Reduce LLM max_tokens
# Enable response caching
# Scale backend workers
docker-compose up -d --scale backend=3
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
uvicorn backend.api.main:app --reload --log-level debug
```

### Performance Tuning

```bash
# Optimize PostgreSQL
# Increase connection pool size
# Enable query caching
# Add database indexes

# Optimize Redis
# Increase memory limit
# Enable persistence

# Optimize LLM
# Use quantized models
# Enable batch processing
# Implement prompt caching
```

---

## Additional Resources

- [EU AI Act Official Text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52021PC0206)
- [Ollama Documentation](https://ollama.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Meta Llama 3 Documentation](https://llama.meta.com/)

---

## Support

For issues and questions:
- GitHub Issues: [Project Issues](https://github.com/your-org/eu-ai-act-compliance/issues)
- Email: support@your-org.com
- Documentation: [Full Documentation](https://docs.your-org.com)

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-11  
**Maintained by**: Implementation Team