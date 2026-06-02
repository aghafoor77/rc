# Explainability Feature Guide

## Overview

The EU AI Act Compliance System now includes comprehensive explainability features that provide detailed insights into classification decisions, building trust and transparency.

## What's New

### Enhanced Classification Response

Every classification now includes an `explainability` object with:

1. **Decision Summary** - Human-readable explanation
2. **Evidence** - Retrieved legal documents with relevance scores
3. **Reasoning Chain** - Step-by-step decision process
4. **Confidence Factors** - What contributed to the confidence score
5. **Alternative Interpretations** - Other possible classifications
6. **Key Factors** - What influenced the decision most

## API Usage

### Request with Explainability (Default)

```bash
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_metadata": {
      "system_name": "Credit Scoring System",
      "sector": "banking",
      "purpose": "creditworthiness_assessment",
      "autonomy_level": "fully_automated",
      "affects_individuals": true
    },
    "use_rag": true,
    "use_llm": true,
    "include_explanations": true
  }'
```

### Response Structure

```json
{
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-05-18T10:00:00Z",
  "risk_category": "HIGH_RISK",
  "confidence": 0.92,
  "method": "hybrid_agreement",
  "requires_human_review": false,
  
  "legal_basis": {
    "primary_article": "Article 6(2), Annex III(5)(b)",
    "supporting_articles": ["Article 9", "Article 10"]
  },
  
  "reasoning": {
    "steps": [
      "System operates in banking sector",
      "Purpose is creditworthiness assessment",
      "Matches Annex III(5)(b) criteria"
    ]
  },
  
  "compliance_obligations": {
    "mandatory": [
      "Risk management system (Article 9)",
      "Data governance (Article 10)",
      "Technical documentation (Article 11)"
    ]
  },
  
  "rag_enabled": true,
  "retrieved_documents_count": 5,
  
  "explainability": {
    "decision_summary": "Credit Scoring System is classified as HIGH-RISK under the EU AI Act. This system requires strict compliance with regulatory requirements before deployment. (Confidence: 92%)",
    
    "evidence": [
      {
        "rank": 1,
        "article": "Annex III",
        "type": "annex",
        "relevance_score": 0.89,
        "excerpt": "Annex III - High-Risk AI Systems (Article 6(2))\n\n5. Access to and enjoyment of essential private services and public services and benefits:\n\n(b) AI systems intended to be used to evaluate the creditworthiness of natural persons...",
        "full_text": "..."
      },
      {
        "rank": 2,
        "article": "Article 6",
        "type": "article",
        "relevance_score": 0.85,
        "excerpt": "Article 6 - Classification Rules for High-Risk AI Systems\n\n1. Irrespective of whether an AI system is placed on the market...",
        "full_text": "..."
      }
    ],
    
    "reasoning_chain": [
      {
        "step": 1,
        "description": "System operates in banking sector, which is regulated under EU AI Act",
        "source": "LLM Analysis"
      },
      {
        "step": 2,
        "description": "Primary purpose is creditworthiness assessment, explicitly listed in Annex III(5)(b)",
        "source": "LLM Analysis"
      },
      {
        "step": 3,
        "description": "System is fully automated, increasing risk level",
        "source": "LLM Analysis"
      },
      {
        "step": 4,
        "description": "Matched rule: Creditworthiness Assessment in Banking",
        "source": "Rule: R-HR-012"
      }
    ],
    
    "confidence_factors": {
      "overall_confidence": 0.92,
      "contributing_factors": [
        {
          "factor": "Rule-based match",
          "impact": "positive",
          "strength": 0.95,
          "description": "Deterministic rules matched with 95% confidence"
        },
        {
          "factor": "LLM semantic analysis",
          "impact": "positive",
          "strength": 0.90,
          "description": "LLM analysis confidence: 90%"
        },
        {
          "factor": "Method agreement",
          "impact": "positive",
          "strength": 0.1,
          "description": "Rule-based and LLM methods agree on classification"
        }
      ],
      "uncertainty_sources": []
    },
    
    "alternative_interpretations": [],
    
    "key_factors": [
      {
        "factor": "Sector",
        "value": "banking",
        "influence": "high",
        "explanation": "Operating in banking sector affects risk classification"
      },
      {
        "factor": "Purpose",
        "value": "creditworthiness_assessment",
        "influence": "high",
        "explanation": "System purpose: creditworthiness_assessment"
      },
      {
        "factor": "Autonomy Level",
        "value": "fully_automated",
        "influence": "medium",
        "explanation": "System operates with fully_automated autonomy"
      },
      {
        "factor": "Individual Impact",
        "value": "Yes",
        "influence": "high",
        "explanation": "System directly affects individuals' rights or access to services"
      }
    ]
  }
}
```

## Explainability Components

### 1. Decision Summary

**Purpose**: Provide a clear, non-technical explanation of the decision.

**Example**:
```
"Credit Scoring System is classified as HIGH-RISK under the EU AI Act. 
This system requires strict compliance with regulatory requirements before deployment. 
(Confidence: 92%)"
```

**Use Case**: Display to stakeholders who need quick understanding.

---

### 2. Evidence

**Purpose**: Show the actual legal text that supports the decision.

**Features**:
- Ranked by relevance (1-5)
- Article/Annex identification
- Relevance score (0.0-1.0)
- Text excerpt and full text
- Retrieved from ChromaDB

**Use Case**: Legal review, audit trails, compliance documentation.

---

### 3. Reasoning Chain

**Purpose**: Show step-by-step how the decision was reached.

**Features**:
- Sequential steps
- Source attribution (LLM vs Rule-based)
- Clear logical flow

**Use Case**: Understanding the decision process, debugging, training.

---

### 4. Confidence Factors

**Purpose**: Explain what contributed to the confidence score.

**Components**:
- **Contributing Factors**: What increased confidence
  - Rule-based matches
  - LLM analysis
  - Method agreement
  
- **Uncertainty Sources**: What decreased confidence
  - Ambiguous interpretations
  - Method disagreements
  - Edge cases

**Use Case**: Risk assessment, deciding if human review is needed.

---

### 5. Alternative Interpretations

**Purpose**: Show other possible classifications that were considered.

**Features**:
- Alternative risk categories
- Confidence scores for alternatives
- Rationale for why they weren't chosen

**Use Case**: Edge cases, borderline classifications, human review.

---

### 6. Key Factors

**Purpose**: Highlight the most important factors that influenced the decision.

**Features**:
- Factor name (Sector, Purpose, Autonomy, etc.)
- Factor value
- Influence level (high/medium/low)
- Explanation

**Use Case**: Quick understanding of decision drivers, what-if analysis.

## Use Cases

### 1. Compliance Documentation

```python
# Generate compliance report with full explainability
response = classify_system(
    system_metadata,
    include_explanations=True
)

# Extract evidence for documentation
for evidence in response['explainability']['evidence']:
    print(f"Article {evidence['article']}: {evidence['excerpt']}")
```

### 2. Human Review Workflow

```python
# Check if human review is needed
if response['requires_human_review']:
    # Show confidence factors to reviewer
    factors = response['explainability']['confidence_factors']
    
    # Show alternative interpretations
    alternatives = response['explainability']['alternative_interpretations']
    
    # Reviewer can make informed decision
```

### 3. Stakeholder Communication

```python
# Get non-technical summary
summary = response['explainability']['decision_summary']

# Get key factors for presentation
key_factors = response['explainability']['key_factors']

# Present to business stakeholders
```

### 4. Audit Trail

```python
# Store complete explainability for audit
audit_record = {
    'assessment_id': response['assessment_id'],
    'decision': response['risk_category'],
    'evidence': response['explainability']['evidence'],
    'reasoning': response['explainability']['reasoning_chain'],
    'timestamp': response['timestamp']
}
```

## Frontend Integration

### Display Decision Summary

```javascript
// Show summary prominently
const summary = response.explainability.decision_summary;
document.getElementById('decision-summary').textContent = summary;
```

### Show Evidence

```javascript
// Display retrieved legal documents
response.explainability.evidence.forEach(doc => {
  const card = `
    <div class="evidence-card">
      <h4>Rank ${doc.rank}: ${doc.article}</h4>
      <p class="relevance">Relevance: ${(doc.relevance_score * 100).toFixed(0)}%</p>
      <p class="excerpt">${doc.excerpt}</p>
      <button onclick="showFullText('${doc.article}')">Read Full Text</button>
    </div>
  `;
  document.getElementById('evidence-list').innerHTML += card;
});
```

### Visualize Reasoning Chain

```javascript
// Show step-by-step reasoning
response.explainability.reasoning_chain.forEach(step => {
  const stepElement = `
    <div class="reasoning-step">
      <span class="step-number">${step.step}</span>
      <p>${step.description}</p>
      <span class="source">${step.source}</span>
    </div>
  `;
  document.getElementById('reasoning-chain').innerHTML += stepElement;
});
```

### Display Confidence Breakdown

```javascript
// Show confidence factors
const factors = response.explainability.confidence_factors;

// Positive factors
factors.contributing_factors.forEach(factor => {
  // Show as green bars
  addFactorBar(factor, 'positive');
});

// Uncertainty sources
factors.uncertainty_sources.forEach(source => {
  // Show as yellow/red warnings
  addUncertaintyWarning(source);
});
```

## Benefits

### 1. Trust & Transparency
- Users understand why decisions were made
- Clear evidence from legal sources
- Traceable reasoning process

### 2. Compliance
- Audit trail for regulatory review
- Legal citations for documentation
- Evidence-based decisions

### 3. Debugging & Improvement
- Identify weak points in classification
- Understand edge cases
- Improve rules and prompts

### 4. Human Review
- Reviewers have full context
- Alternative interpretations available
- Confidence factors guide review priority

### 5. Stakeholder Communication
- Non-technical summaries
- Visual evidence
- Clear key factors

## Configuration

### Enable/Disable Explainability

```python
# Full explainability (default)
response = classify(metadata, include_explanations=True)

# Minimal response (faster)
response = classify(metadata, include_explanations=False)
```

### Control Detail Level

The explainability system automatically adjusts detail based on:
- Number of retrieved documents (more evidence = more detail)
- Confidence level (low confidence = more alternatives shown)
- Method agreement (disagreement = more explanation)

## Performance Considerations

- **With Explainability**: ~100-200ms additional processing
- **Without Explainability**: Standard classification time
- **Recommendation**: Enable for user-facing requests, disable for batch processing

## Future Enhancements

1. **Visual Explanations**: Generate diagrams and flowcharts
2. **Counterfactual Explanations**: "What if X was different?"
3. **Feature Importance**: Quantify impact of each factor
4. **Comparison Mode**: Compare multiple systems side-by-side
5. **Export Formats**: PDF reports, JSON, XML for different systems

## Summary

The explainability feature provides:
- ✅ Clear decision summaries
- ✅ Legal evidence with citations
- ✅ Step-by-step reasoning
- ✅ Confidence analysis
- ✅ Alternative interpretations
- ✅ Key factor identification

This builds trust, enables compliance, and supports informed decision-making in EU AI Act risk classification.