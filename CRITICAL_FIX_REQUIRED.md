# 🚨 CRITICAL: Engines Not Initialized - Fix Required

## The Problem You're Seeing

```
Method: fallback heuristic
Classification based on heuristic rules (engines unavailable)
System operates in unknown sector
Primary purpose: unknown
```

This means:
- ❌ **Classification engines are NOT initialized**
- ❌ **RAG pipeline is NOT working**
- ❌ **LLM engine is NOT working**
- ❌ **Rule engine is NOT working**
- ⚠️ **System is using fallback mode** (simple heuristics only)

## Why This Happens

The backend code changes we made are **NOT being used** because:

1. **Docker containers not restarted** - Running old code
2. **Or Docker not running at all**
3. **Or services failed to start**

## The Fix

### Step 1: Check if Docker is Running

```bash
# Check Docker status
docker ps

# If you see containers listed, Docker is running
# If you see "Cannot connect to Docker daemon", Docker is not running
```

### Step 2: Restart Docker Services

```bash
cd /home/testbed/Desktop/eu-ai-act-compliance-system

# Stop all services
docker compose down
# or
docker-compose down

# Start services with new code
docker compose up -d
# or
docker-compose up -d

# Wait 60 seconds for services to fully start
sleep 60
```

### Step 3: Verify Services Started

```bash
# Check all services are running
docker compose ps
# or
docker-compose ps

# You should see:
# - backend (Up)
# - ollama (Up)
# - postgres (Up)
# - redis (Up)
# - nginx (Up)
```

### Step 4: Check Backend Logs

```bash
# View backend logs
docker compose logs backend --tail=50
# or
docker-compose logs backend --tail=50
```

**Look for these SUCCESS messages:**
```
INFO - Rule engine initialized
INFO - LLM engine initialized with Ollama at http://ollama:11434
INFO - RAG pipeline initialized with sentence-transformers embeddings
INFO - RAG collection: XXX documents
INFO - Hybrid classification engine initialized
```

**If you see ERROR messages:**
```
ERROR - Error initializing engines: ...
WARNING - Engines not initialized - will use fallback classification
```

This means something failed to start.

### Step 5: Test the API

```bash
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Credit Scoring System",
      "sector": "banking",
      "purpose": "creditworthiness_assessment"
    },
    "use_rag": true,
    "use_llm": true
  }'
```

**Expected Response (GOOD):**
```json
{
  "risk_category": "HIGH_RISK",
  "confidence": 0.85-0.95,
  "method": "hybrid_agreement" or "llm_based" or "rule_based",
  "rag_enabled": true,
  "retrieved_documents_count": 5
}
```

**Current Response (BAD):**
```json
{
  "risk_category": "MINIMAL_RISK",
  "confidence": 0.5,
  "method": "fallback_heuristic",
  "reasoning": {
    "steps": ["engines unavailable"]
  }
}
```

## Common Issues & Solutions

### Issue 1: Docker Not Installed

**Symptom**: `docker: command not found`

**Solution**: Install Docker
```bash
# Check if Docker is installed
docker --version

# If not installed, install Docker Desktop or Docker Engine
```

### Issue 2: Docker Not Running

**Symptom**: `Cannot connect to the Docker daemon`

**Solution**: Start Docker
```bash
# On Linux
sudo systemctl start docker

# On Mac/Windows
# Start Docker Desktop application
```

### Issue 3: Ollama Not Running

**Symptom**: Backend logs show `Connection refused to ollama:11434`

**Solution**: 
```bash
# Check Ollama container
docker compose ps ollama

# If not running, start it
docker compose up -d ollama

# Pull required model
docker compose exec ollama ollama pull llama3:8b
```

### Issue 4: ChromaDB Not Found

**Symptom**: Backend logs show `Collection not found` or `ChromaDB error`

**Solution**:
```bash
# Verify ChromaDB data exists
ls -la ./data/euaiact_chroma/

# Should show:
# chroma.sqlite3
# 8ed19602-7ffe-416c-acbb-6cfaa770c067/

# If missing, copy again
cp -r /home/testbed/Downloads/EUAIAct_Assistant/data/chroma ./data/euaiact_chroma
```

### Issue 5: Dependencies Not Installed

**Symptom**: Backend logs show `ModuleNotFoundError: No module named 'chromadb'`

**Solution**: Rebuild Docker image
```bash
docker compose build --no-cache backend
docker compose up -d
```

## Verification Checklist

After applying fixes, verify:

- [ ] Docker is running (`docker ps` works)
- [ ] All services are Up (`docker compose ps`)
- [ ] Backend logs show "Rule engine initialized"
- [ ] Backend logs show "LLM engine initialized"
- [ ] Backend logs show "RAG pipeline initialized"
- [ ] Backend logs show "RAG collection: XXX documents"
- [ ] No ERROR messages in logs
- [ ] CURL test returns `method: "hybrid_agreement"` or `"llm_based"`
- [ ] CURL test returns `rag_enabled: true`
- [ ] CURL test returns `confidence: 0.8+` (not 0.5)
- [ ] Frontend shows different responses for different inputs
- [ ] Frontend shows specific legal articles (not generic)

## Expected vs Actual Behavior

### ❌ Current (Fallback Mode):
```
Method: fallback heuristic
Confidence: 50.0%
System operates in unknown sector
Primary purpose: unknown
engines unavailable
```

### ✅ Expected (After Fix):
```
Method: hybrid_agreement
Confidence: 92.0%
System operates in banking sector
Purpose: creditworthiness_assessment
Retrieved 5 documents from RAG
Legal Basis: Article 6(2), Annex III(5)(b)
```

## Quick Diagnostic Command

```bash
# Run this to check everything
echo "=== Docker Status ===" && \
docker ps && \
echo -e "\n=== Backend Logs ===" && \
docker compose logs backend --tail=20 && \
echo -e "\n=== Test API ===" && \
curl -s -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{"ai_system_metadata":{"sector":"banking","purpose":"creditworthiness_assessment"},"use_rag":true,"use_llm":true}' \
  | jq '.method, .confidence, .rag_enabled'
```

**Expected Output:**
```
=== Docker Status ===
CONTAINER ID   IMAGE                  STATUS
xxx            backend                Up
xxx            ollama                 Up
...

=== Backend Logs ===
INFO - Rule engine initialized
INFO - LLM engine initialized
INFO - RAG pipeline initialized
INFO - RAG collection: 300+ documents

=== Test API ===
"hybrid_agreement"
0.92
true
```

## If Nothing Works - Nuclear Reset

```bash
# Complete reset
cd /home/testbed/Desktop/eu-ai-act-compliance-system

# Stop and remove everything
docker compose down -v

# Rebuild from scratch
docker compose build --no-cache

# Start services
docker compose up -d

# Wait for services to start
sleep 90

# Check logs
docker compose logs backend --tail=50

# Test API
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{"ai_system_metadata":{"sector":"banking","purpose":"creditworthiness_assessment"},"use_rag":true,"use_llm":true}'
```

## Summary

**Problem**: Engines not initialized → fallback mode → same response always

**Root Cause**: Docker not restarted after code changes

**Solution**: 
```bash
docker compose down
docker compose up -d
# Wait 60 seconds
# Test API with CURL
# Hard refresh browser
```

**Verification**: Response should show `method: "hybrid_agreement"` NOT `"fallback_heuristic"`

## Need Help?

If still not working after following this guide:

1. Run the diagnostic command above
2. Share the output
3. Check `docker compose logs backend` for errors
4. Verify ChromaDB data exists: `ls -la ./data/euaiact_chroma/`