# EU AI Act Compliance System - Architecture Documentation

## 1. System Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Web UI     │  │  Dashboard   │  │   Reports    │              │
│  │  (React/Vue) │  │   (Admin)    │  │   Viewer     │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         API Gateway Layer                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              FastAPI REST API (OpenAPI/Swagger)              │  │
│  │  • Authentication & Authorization (JWT)                      │  │
│  │  • Rate Limiting & Throttling                                │  │
│  │  • Request Validation & Sanitization                         │  │
│  │  • API Versioning (v1, v2)                                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Orchestration Layer                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Classification Orchestrator                  │  │
│  │  • Workflow Management (LangGraph)                           │  │
│  │  • State Management                                          │  │
│  │  • Error Handling & Retry Logic                             │  │
│  │  • Async Task Queue (Celery)                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│   Rule-Based Engine       │   │   LLM-Based Engine        │
│  ┌─────────────────────┐  │   │  ┌─────────────────────┐  │
│  │  Deterministic      │  │   │  │  Semantic Reasoning │  │
│  │  Classification     │  │   │  │  (Llama 3)          │  │
│  │  • Prohibited AI    │  │   │  │  • Nuanced Cases    │  │
│  │  • High-Risk Rules  │  │   │  │  • Explainability   │  │
│  │  • Annex III Match  │  │   │  │  • Confidence Score │  │
│  └─────────────────────┘  │   │  └─────────────────────┘  │
└───────────────────────────┘   └───────────────────────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      RAG Pipeline Layer                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Retrieval-Augmented Generation                   │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐             │  │
│  │  │  Document  │  │  Vector    │  │  Context   │             │  │
│  │  │  Retrieval │→ │  Search    │→ │  Injection │             │  │
│  │  └────────────┘  └────────────┘  └────────────┘             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Compliance Mapping Engine                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  • Legal Article Mapping                                     │  │
│  │  • Obligation Extraction                                     │  │
│  │  • Gap Analysis                                              │  │
│  │  • Remediation Recommendations                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Security & Guardrails Layer                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  • Prompt Injection Detection                                │  │
│  │  • Input Validation & Sanitization                           │  │
│  │  • Output Filtering                                          │  │
│  │  • AI Firewall (Policy Enforcement)                          │  │
│  │  • Anomaly Detection                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Data & Storage Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  PostgreSQL  │  │   ChromaDB   │  │    Redis     │             │
│  │  (Metadata)  │  │   (Vectors)  │  │   (Cache)    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐                                │
│  │  Audit Logs  │  │  Legal Corpus│                                │
│  │  (Immutable) │  │  (Documents) │                                │
│  └──────────────┘  └──────────────┘                                │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Interaction Flow

```
User Request → API Gateway → Authentication → Input Validation
                                                      │
                                                      ▼
                                            Orchestrator
                                                      │
                                    ┌─────────────────┴─────────────────┐
                                    ▼                                   ▼
                            Rule Engine                          LLM Engine
                                    │                                   │
                                    │         ┌─────────────────────────┤
                                    │         ▼                         │
                                    │    RAG Pipeline                   │
                                    │         │                         │
                                    └─────────┴─────────────────────────┘
                                                      │
                                                      ▼
                                          Compliance Mapper
                                                      │
                                                      ▼
                                            Security Filter
                                                      │
                                                      ▼
                                          Result Aggregation
                                                      │
                                                      ▼
                                            Audit Logging
                                                      │
                                                      ▼
                                          Response to User
```

## 2. Core Components

### 2.1 Rule-Based Classification Engine

**Purpose**: Deterministic classification for clear-cut cases

**Components**:
- **Rule Parser**: Loads and validates classification rules
- **Rule Matcher**: Matches AI system metadata against rules
- **Confidence Calculator**: Assigns confidence scores to rule matches
- **Conflict Resolver**: Handles overlapping or conflicting rules

**Rule Structure**:
```python
{
    "rule_id": "R-PROHIBITED-001",
    "category": "PROHIBITED",
    "name": "Social Scoring by Public Authority",
    "conditions": {
        "operator": "AND",
        "criteria": [
            {"field": "deployer_type", "operator": "==", "value": "public_authority"},
            {"field": "purpose", "operator": "in", "value": ["social_scoring", "trustworthiness_evaluation"]},
            {"field": "scope", "operator": "==", "value": "general_population"}
        ]
    },
    "legal_basis": "Article 5(1)(c)",
    "confidence": 1.0,
    "priority": 1
}
```

**Decision Logic**:
1. Load all active rules from rule database
2. Parse AI system metadata
3. Evaluate each rule's conditions
4. Collect matching rules
5. Apply priority and conflict resolution
6. Return classification with confidence score

### 2.2 LLM-Based Semantic Reasoning Engine

**Purpose**: Handle nuanced cases requiring contextual understanding

**Architecture**:
```
Input Metadata → Prompt Template → LLM (Llama 3) → Structured Output
                       ↑                                    ↓
                  RAG Context                      Confidence Score
                       ↑                                    ↓
                Legal Documents                    Reasoning Chain
```

**Prompt Engineering Strategy**:
- **System Prompt**: Defines role as EU AI Act compliance expert
- **Context Injection**: Relevant legal articles via RAG
- **Few-Shot Examples**: Demonstrates classification reasoning
- **Structured Output**: JSON schema enforcement
- **Chain-of-Thought**: Explicit reasoning steps

**Example Prompt Template**:
```
You are an EU AI Act compliance expert. Classify the following AI system.

LEGAL CONTEXT:
{rag_retrieved_articles}

AI SYSTEM METADATA:
{system_metadata}

CLASSIFICATION RULES:
{relevant_rules}

Provide classification in JSON format:
{
  "risk_category": "PROHIBITED|HIGH_RISK|LIMITED_RISK|MINIMAL_RISK",
  "confidence": 0.0-1.0,
  "reasoning": ["step1", "step2", ...],
  "legal_articles": ["Article X", ...],
  "detected_risks": [...],
  "ambiguities": [...]
}

Think step-by-step and explain your reasoning.
```

**Hallucination Prevention**:
- Ground responses in retrieved legal documents
- Validate outputs against rule database
- Cross-check with deterministic rules
- Require explicit legal citations
- Flag low-confidence classifications for human review

### 2.3 RAG Pipeline

**Purpose**: Ground LLM reasoning in actual EU AI Act text

**Components**:

1. **Document Ingestion**:
   - EU AI Act full text
   - Annexes (I-XIII)
   - Recitals
   - Official guidance documents
   - Case studies

2. **Chunking Strategy**:
   - Article-level chunks (primary)
   - Paragraph-level chunks (secondary)
   - Maintain legal structure and context
   - Overlap between chunks for continuity

3. **Embedding Model**:
   - `sentence-transformers/all-MiniLM-L6-v2` (default)
   - Alternative: `sentence-transformers/all-mpnet-base-v2`
   - Dimension: 384 (MiniLM) or 768 (MPNet)

4. **Vector Database (ChromaDB)**:
   - Collection: `eu_ai_act_legal_corpus`
   - Metadata: article_number, section, category, date
   - Similarity metric: Cosine similarity

5. **Retrieval Strategy**:
   - Hybrid search: Vector similarity + keyword matching
   - Top-k retrieval: k=5 (configurable)
   - Re-ranking: Relevance scoring
   - Context window: 2048 tokens

**RAG Flow**:
```
Query → Embedding → Vector Search → Top-K Retrieval → Re-ranking → Context
                                                                        ↓
                                                              LLM Prompt Injection
```

### 2.4 Compliance Mapping Engine

**Purpose**: Map AI systems to specific compliance obligations

**Mapping Logic**:

```python
def map_compliance_obligations(risk_category, ai_metadata):
    obligations = []
    
    if risk_category == "PROHIBITED":
        obligations.append({
            "obligation": "System must not be placed on market or put into service",
            "article": "Article 5",
            "severity": "CRITICAL"
        })
    
    elif risk_category == "HIGH_RISK":
        # Article 9: Risk Management System
        obligations.append({
            "obligation": "Establish and maintain risk management system",
            "article": "Article 9",
            "requirements": [
                "Identify and analyze known and foreseeable risks",
                "Estimate and evaluate risks",
                "Evaluate other possibly arising risks",
                "Adopt suitable risk management measures"
            ],
            "severity": "MANDATORY"
        })
        
        # Article 10: Data and Data Governance
        obligations.append({
            "obligation": "Implement data governance practices",
            "article": "Article 10",
            "requirements": [
                "Training, validation, testing data sets",
                "Relevant design choices",
                "Data quality criteria",
                "Data preparation and labeling"
            ],
            "severity": "MANDATORY"
        })
        
        # Article 11: Technical Documentation
        # Article 12: Record-keeping
        # Article 13: Transparency and Information
        # Article 14: Human Oversight
        # Article 15: Accuracy, Robustness, Cybersecurity
        # ... (continue for all high-risk obligations)
    
    elif risk_category == "GPAI_SYSTEMIC_RISK":
        # Article 55: Additional obligations for GPAI with systemic risk
        obligations.append({
            "obligation": "Model evaluation and adversarial testing",
            "article": "Article 55(1)(a)",
            "severity": "MANDATORY"
        })
        # ... (continue for GPAI obligations)
    
    return obligations
```

**Obligation Categories**:
1. **Pre-Market Requirements**: Before deployment
2. **Technical Requirements**: System design and development
3. **Documentation Requirements**: Technical documentation
4. **Operational Requirements**: During deployment
5. **Post-Market Requirements**: Monitoring and updates
6. **Transparency Requirements**: User information
7. **Governance Requirements**: Organizational measures

### 2.5 Audit Logging System

**Purpose**: Immutable audit trail for regulatory compliance

**Log Structure**:
```json
{
  "log_id": "uuid",
  "timestamp": "ISO-8601",
  "event_type": "CLASSIFICATION_REQUEST|HUMAN_REVIEW|SYSTEM_UPDATE",
  "user_id": "uuid",
  "session_id": "uuid",
  "ai_system_id": "uuid",
  "input_data": {
    "metadata": {...},
    "questionnaire_responses": {...}
  },
  "processing_steps": [
    {
      "step": "rule_engine",
      "timestamp": "ISO-8601",
      "duration_ms": 150,
      "rules_evaluated": 47,
      "rules_matched": 3,
      "result": {...}
    },
    {
      "step": "llm_reasoning",
      "timestamp": "ISO-8601",
      "duration_ms": 1850,
      "model": "llama3:8b",
      "tokens_used": 1247,
      "result": {...}
    },
    {
      "step": "rag_retrieval",
      "timestamp": "ISO-8601",
      "duration_ms": 320,
      "documents_retrieved": 5,
      "sources": ["Article_6.pdf", "Annex_III.pdf"]
    }
  ],
  "classification_result": {...},
  "confidence_score": 0.95,
  "human_review_required": false,
  "reviewer_id": null,
  "review_timestamp": null,
  "review_decision": null,
  "hash": "SHA-256 hash of log entry",
  "previous_hash": "SHA-256 hash of previous log"
}
```

**Immutability Mechanism**:
- Blockchain-inspired hash chaining
- Write-once storage
- Cryptographic signatures
- Tamper detection

### 2.6 Human Review Workflow

**Trigger Conditions**:
1. Confidence score < 0.75
2. Conflicting classifications (rule vs LLM)
3. Novel AI system type
4. Ambiguous legal interpretation
5. User-requested review
6. High-stakes decision (e.g., prohibited classification)

**Workflow States**:
```
PENDING_REVIEW → ASSIGNED → IN_REVIEW → REVIEWED → APPROVED/REJECTED
```

**Review Interface**:
- Display AI system metadata
- Show automated classification
- Present reasoning chain
- Highlight ambiguities
- Provide legal references
- Allow reviewer comments
- Support override with justification

## 3. Security Architecture

### 3.1 Threat Model

**Threats**:
1. **Prompt Injection**: Malicious input to manipulate LLM
2. **Jailbreak Attempts**: Bypass safety guardrails
3. **RAG Poisoning**: Inject malicious documents
4. **Data Leakage**: Extract sensitive information
5. **Model Manipulation**: Tamper with model weights
6. **API Abuse**: Excessive requests, DoS
7. **Adversarial Inputs**: Crafted to evade classification

### 3.2 Defense Mechanisms

**Input Validation**:
```python
def validate_input(ai_metadata):
    # Schema validation
    validate_schema(ai_metadata, AI_METADATA_SCHEMA)
    
    # Sanitization
    sanitize_strings(ai_metadata)
    
    # Prompt injection detection
    if detect_prompt_injection(ai_metadata):
        raise SecurityException("Potential prompt injection detected")
    
    # Length limits
    enforce_length_limits(ai_metadata)
    
    # Type checking
    enforce_type_constraints(ai_metadata)
    
    return ai_metadata
```

**AI Firewall**:
- Pattern-based detection (regex, signatures)
- Behavioral analysis (anomaly detection)
- Rate limiting (per user, per IP)
- Content filtering (blocklist, allowlist)
- Output sanitization

**Sandboxing**:
- LLM runs in isolated container
- No network access from LLM
- Resource limits (CPU, memory, time)
- Restricted file system access

**Monitoring**:
- Real-time threat detection
- Anomaly alerts
- Usage analytics
- Performance metrics

## 4. Deployment Architecture

### 4.1 Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose Stack                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   FastAPI    │  │    Ollama    │  │  PostgreSQL  │      │
│  │   Backend    │  │  (Llama 3)   │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   ChromaDB   │  │    Redis     │  │    Celery    │      │
│  │              │  │              │  │    Worker    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │    Nginx     │  │  Prometheus  │                        │
│  │  (Reverse    │  │  (Monitoring)│                        │
│  │   Proxy)     │  │              │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Scaling Strategy

**Horizontal Scaling**:
- Multiple FastAPI instances behind load balancer
- Stateless API design
- Shared PostgreSQL and Redis
- Distributed ChromaDB (if needed)

**Vertical Scaling**:
- GPU acceleration for LLM inference
- Increased memory for vector database
- SSD storage for faster I/O

**Caching Strategy**:
- Redis for API response caching
- LLM response caching (deterministic inputs)
- Vector search result caching

### 4.3 High Availability

- Multi-region deployment
- Database replication (primary-replica)
- Automatic failover
- Health checks and auto-restart
- Backup and disaster recovery

## 5. Performance Optimization

### 5.1 LLM Optimization

- **Model Quantization**: 4-bit or 8-bit quantization
- **Batch Processing**: Group multiple requests
- **Prompt Caching**: Cache common prompt patterns
- **Streaming Responses**: Reduce perceived latency

### 5.2 RAG Optimization

- **Index Optimization**: HNSW algorithm for fast search
- **Embedding Caching**: Cache embeddings for common queries
- **Lazy Loading**: Load documents on-demand
- **Compression**: Compress vector storage

### 5.3 Database Optimization

- **Indexing**: Index frequently queried fields
- **Connection Pooling**: Reuse database connections
- **Query Optimization**: Optimize SQL queries
- **Partitioning**: Partition large tables

## 6. Monitoring & Observability

### 6.1 Metrics

- **Performance**: Response time, throughput, latency
- **Accuracy**: Classification accuracy, confidence distribution
- **Usage**: API calls, user activity, popular features
- **Errors**: Error rates, exception types, failure modes
- **Resources**: CPU, memory, disk, network usage

### 6.2 Logging

- **Application Logs**: Structured JSON logs
- **Audit Logs**: Immutable compliance logs
- **Security Logs**: Threat detection, access logs
- **Performance Logs**: Slow queries, bottlenecks

### 6.3 Alerting

- **Critical Alerts**: System down, security breach
- **Warning Alerts**: High error rate, performance degradation
- **Info Alerts**: Unusual patterns, capacity warnings

## 7. Future Extensibility

### 7.1 Planned Enhancements

1. **Multi-Language Support**: Support for all EU languages
2. **Advanced Analytics**: Trend analysis, risk heatmaps
3. **Integration APIs**: Connect with compliance management systems
4. **Mobile App**: iOS and Android applications
5. **AI Red-Teaming**: Automated adversarial testing
6. **Continuous Learning**: Model fine-tuning on new cases

### 7.2 Regulatory Updates

- Modular rule engine for easy updates
- Version control for legal corpus
- Backward compatibility for assessments
- Migration tools for schema changes

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-11  
**Maintained by**: Architecture Team