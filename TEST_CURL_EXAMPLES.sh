#!/bin/bash

# Three CURL Examples That Should Give Different Results
# Run these after restarting Docker: docker compose down && docker compose up -d

echo "=========================================="
echo "Test 1: Banking Credit Scoring (HIGH-RISK)"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Credit Scoring System",
      "sector": "banking",
      "purpose": "creditworthiness_assessment",
      "autonomy_level": "fully_automated",
      "affects_individuals": true,
      "impacts_financial_access": true
    },
    "use_rag": true,
    "use_llm": true,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article
  }'

echo -e "\n\n=========================================="
echo "Test 2: Social Scoring System (PROHIBITED)"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Social Credit System",
      "sector": "government",
      "purpose": "social_scoring",
      "deployer_type": "public_authority",
      "ranks_people": true,
      "affects_individuals": true
    },
    "use_rag": true,
    "use_llm": true,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article
  }'

echo -e "\n\n=========================================="
echo "Test 3: Simple Chatbot (MINIMAL-RISK)"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Customer Service Chatbot",
      "sector": "retail",
      "purpose": "customer_support",
      "autonomy_level": "human_in_loop",
      "affects_individuals": false,
      "safety_critical": false
    },
    "use_rag": true,
    "use_llm": true,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article
  }'

echo -e "\n\n=========================================="
echo "Test 4: Simple Customer Service Chatbot"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Test Chatbot",
      "sector": "customer_service",
      "purpose": "customer_support"
    }
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article,
    sources_count: (.legal_basis.sources | length)
  }'

echo -e "\n\n=========================================="
echo "Test 5: Healthcare Diagnostic AI (LLM-Only)"
echo "Force LLM classification with RAG"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Medical Diagnostic Assistant",
      "sector": "healthcare",
      "purpose": "medical_diagnosis",
      "autonomy_level": "fully_automated",
      "affects_individuals": true,
      "safety_critical": true,
      "processes_health_data": true
    },
    "use_rag": true,
    "use_llm": true,
    "use_rules": false,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article,
    supporting_articles: .legal_basis.supporting_articles,
    sources_count: (.legal_basis.sources | length),
    llm_reasoning: .evidence.llm_based.reasoning[:200]
  }'

echo -e "\n\n=========================================="
echo "Test 6: Recruitment AI System (LLM-Only)"
echo "Force LLM classification with RAG"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "AI Recruitment Platform",
      "sector": "employment",
      "purpose": "candidate_screening",
      "autonomy_level": "semi_automated",
      "affects_individuals": true,
      "impacts_employment": true,
      "uses_biometric_data": false
    },
    "use_rag": true,
    "use_llm": true,
    "use_rules": false,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article,
    supporting_articles: .legal_basis.supporting_articles,
    sources_count: (.legal_basis.sources | length),
    llm_reasoning: .evidence.llm_based.reasoning[:200]
  }'

echo -e "\n\n=========================================="
echo "Test 7: Emotion Recognition System (LLM-Only)"
echo "Force LLM classification with RAG"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Workplace Emotion Detector",
      "sector": "workplace_monitoring",
      "purpose": "emotion_recognition",
      "autonomy_level": "fully_automated",
      "affects_individuals": true,
      "uses_biometric_data": true,
      "deployed_in_workplace": true
    },
    "use_rag": true,
    "use_llm": true,
    "use_rules": false,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article,
    supporting_articles: .legal_basis.supporting_articles,
    sources_count: (.legal_basis.sources | length),
    llm_reasoning: .evidence.llm_based.reasoning[:200]
  }'

echo -e "\n\n=========================================="
echo "Test 8: Educational Assessment AI (LLM-Only)"
echo "Force LLM classification with RAG"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Student Performance Evaluator",
      "sector": "education",
      "purpose": "educational_assessment",
      "autonomy_level": "semi_automated",
      "affects_individuals": true,
      "impacts_educational_access": true,
      "processes_minors_data": true
    },
    "use_rag": true,
    "use_llm": true,
    "use_rules": false,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article,
    supporting_articles: .legal_basis.supporting_articles,
    sources_count: (.legal_basis.sources | length),
    llm_reasoning: .evidence.llm_based.reasoning[:200]
  }'

echo -e "\n\n=========================================="
echo "Test 9: Law Enforcement Predictive Policing (LLM-Only)"
echo "Force LLM classification with RAG"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Crime Prediction System",
      "sector": "law_enforcement",
      "purpose": "risk_assessment",
      "autonomy_level": "fully_automated",
      "affects_individuals": true,
      "deployer_type": "public_authority",
      "used_by_law_enforcement": true
    },
    "use_rag": true,
    "use_llm": true,
    "use_rules": false,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article,
    supporting_articles: .legal_basis.supporting_articles,
    sources_count: (.legal_basis.sources | length),
    llm_reasoning: .evidence.llm_based.reasoning[:200]
  }'

echo -e "\n\n=========================================="
echo "Test 10: Content Moderation AI (LLM-Only)"
echo "Force LLM classification with RAG"
echo "=========================================="
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Social Media Content Filter",
      "sector": "social_media",
      "purpose": "content_moderation",
      "autonomy_level": "fully_automated",
      "affects_individuals": true,
      "impacts_freedom_of_expression": true,
      "large_scale_deployment": true
    },
    "use_rag": true,
    "use_llm": true,
    "use_rules": false,
    "include_explanations": true
  }' | jq '{
    risk_category: .risk_category,
    confidence: .confidence,
    method: .method,
    rag_enabled: .rag_enabled,
    retrieved_docs: .retrieved_documents_count,
    primary_article: .legal_basis.primary_article,
    supporting_articles: .legal_basis.supporting_articles,
    sources_count: (.legal_basis.sources | length),
    llm_reasoning: .evidence.llm_based.reasoning[:200]
  }'

echo -e "\n\n=========================================="
echo "EXPECTED RESULTS SUMMARY"
echo "=========================================="
echo "Tests 1-4: Hybrid or LLM-based (with rules enabled)"
echo "  Test 1 (Banking): HIGH_RISK, confidence 0.85-0.95"
echo "  Test 2 (Social Scoring): PROHIBITED, confidence 0.90-0.99"
echo "  Test 3 (Chatbot): MINIMAL_RISK, confidence 0.70-0.85"
echo "  Test 4 (Simple Chatbot): MINIMAL_RISK or LIMITED_RISK"
echo ""
echo "Tests 5-10: LLM-ONLY (rules disabled, Ollama forced)"
echo "  Test 5 (Healthcare): HIGH_RISK, Article 6 (Annex III)"
echo "  Test 6 (Recruitment): HIGH_RISK, Article 6 (Annex III)"
echo "  Test 7 (Emotion Recognition): PROHIBITED, Article 5"
echo "  Test 8 (Education): HIGH_RISK, Article 6 (Annex III)"
echo "  Test 9 (Law Enforcement): HIGH_RISK, Article 6 (Annex III)"
echo "  Test 10 (Content Moderation): LIMITED_RISK or HIGH_RISK"
echo ""
echo "All LLM-only tests (5-10) should show:"
echo "  - method: 'llm_only' (NOT 'hybrid' or 'rule_based')"
echo "  - rag_enabled: true"
echo "  - retrieved_docs: 5"
echo "  - primary_article: Specific article from VectorDB"
echo "  - supporting_articles: Array of related articles"
echo "  - sources_count: >0 (legal sources from VectorDB)"
echo "  - llm_reasoning: First 200 chars of Ollama's reasoning"
echo "=========================================="

# Made with Bob
