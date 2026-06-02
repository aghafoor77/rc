#!/bin/bash

# Three CURL Examples That Should Give Different Results
# Run these after restarting Docker: docker compose down && docker compose up -d
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
  }' | jq 


echo -e "\n\n=========================================="
echo "RESULTS "
echo "=========================================="

# Made with Bob
