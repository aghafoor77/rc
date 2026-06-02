# EU AI Act Classification Rules

## Overview

This document defines all classification rules for determining AI system risk categories under the EU AI Act. Rules are organized by risk category and include deterministic conditions, confidence scores, and legal basis.

## Rule Structure

Each rule follows this structure:

```json
{
  "rule_id": "R-[CATEGORY]-[NUMBER]",
  "category": "PROHIBITED|HIGH_RISK|LIMITED_RISK|MINIMAL_RISK|GPAI",
  "name": "Rule name",
  "description": "Detailed description",
  "conditions": {
    "operator": "AND|OR",
    "criteria": [...]
  },
  "legal_basis": "Article reference",
  "confidence": 0.0-1.0,
  "priority": 1-10,
  "enabled": true
}
```

---

## 1. PROHIBITED AI PRACTICES (Article 5)

### R-PROHIBITED-001: Social Scoring by Public Authority

**Legal Basis**: Article 5(1)(c)

**Description**: AI systems for social scoring by public authorities

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "deployer_type", "operator": "==", "value": "public_authority"},
    {"field": "purpose", "operator": "in", "value": ["social_scoring", "trustworthiness_evaluation"]},
    {"field": "evaluates_general_population", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 1 (Highest)

---

### R-PROHIBITED-002: Subliminal Manipulation

**Legal Basis**: Article 5(1)(a)

**Description**: AI systems using subliminal techniques to manipulate behavior

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "uses_subliminal_techniques", "operator": "==", "value": true},
    {"field": "manipulates_behavior", "operator": "==", "value": true},
    {"field": "causes_harm", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 1

---

### R-PROHIBITED-003: Exploitation of Vulnerabilities

**Legal Basis**: Article 5(1)(b)

**Description**: AI systems exploiting vulnerabilities of specific groups

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "targets_vulnerable_groups", "operator": "==", "value": true},
    {"field": "exploits_vulnerabilities", "operator": "==", "value": true},
    {
      "field": "vulnerable_group_type",
      "operator": "in",
      "value": ["age", "disability", "social_situation", "economic_situation"]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 1

---

### R-PROHIBITED-004: Criminal Risk Assessment (Profiling Only)

**Legal Basis**: Article 5(1)(d)

**Description**: Risk assessment based solely on profiling

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "predicts_criminal_offense_risk", "operator": "==", "value": true},
    {"field": "based_solely_on_profiling", "operator": "==", "value": true},
    {"field": "no_objective_verifiable_facts", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 1

---

### R-PROHIBITED-005: Facial Recognition Database (Scraping)

**Legal Basis**: Article 5(1)(e)

**Description**: Creating facial recognition databases via untargeted scraping

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "creates_facial_recognition_database", "operator": "==", "value": true},
    {"field": "uses_untargeted_scraping", "operator": "==", "value": true},
    {
      "field": "scraping_source",
      "operator": "in",
      "value": ["internet", "cctv_footage"]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 1

---

### R-PROHIBITED-006: Emotion Recognition (Workplace/Education)

**Legal Basis**: Article 5(1)(f)

**Description**: Emotion recognition in workplace or education (with exceptions)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "performs_emotion_recognition", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "emotion_recognition_in_workplace", "operator": "==", "value": true},
        {"field": "emotion_recognition_in_education", "operator": "==", "value": true}
      ]
    },
    {"field": "has_medical_safety_justification", "operator": "==", "value": false}
  ]
}
```

**Confidence**: 0.95  
**Priority**: 1

---

### R-PROHIBITED-007: Biometric Categorization (Sensitive Attributes)

**Legal Basis**: Article 5(1)(g)

**Description**: Biometric categorization inferring sensitive attributes

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "performs_biometric_categorization", "operator": "==", "value": true},
    {"field": "infers_sensitive_attributes", "operator": "==", "value": true},
    {
      "field": "sensitive_attributes",
      "operator": "in",
      "value": [
        "race",
        "political_opinions",
        "trade_union_membership",
        "religious_beliefs",
        "sex_life",
        "sexual_orientation"
      ]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 1

---

### R-PROHIBITED-008: Real-time Remote Biometric ID (Law Enforcement)

**Legal Basis**: Article 5(1)(h)

**Description**: Real-time remote biometric identification by law enforcement (with exceptions)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "performs_realtime_remote_biometric_id", "operator": "==", "value": true},
    {"field": "used_by_law_enforcement", "operator": "==", "value": true},
    {"field": "publicly_accessible_space", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "has_judicial_authorization", "operator": "==", "value": false},
        {"field": "meets_strict_necessity_test", "operator": "==", "value": false}
      ]
    }
  ]
}
```

**Confidence**: 0.95  
**Priority**: 1

---

## 2. HIGH-RISK AI SYSTEMS (Annex III)

### Annex III(1): Biometric Identification and Categorization

#### R-HR-001: Remote Biometric Identification

**Legal Basis**: Article 6(2), Annex III(1)(a)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "biometric_identification_system", "operator": "==", "value": true},
    {"field": "remote_identification", "operator": "==", "value": true},
    {"field": "identifies_natural_persons", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-002: Biometric Categorization

**Legal Basis**: Article 6(2), Annex III(1)(b)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "biometric_categorization_system", "operator": "==", "value": true},
    {"field": "categorizes_by_sensitive_attributes", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

### Annex III(2): Critical Infrastructure

#### R-HR-003: Critical Infrastructure Management

**Legal Basis**: Article 6(2), Annex III(2)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "manages_critical_infrastructure", "operator": "==", "value": true},
    {
      "field": "infrastructure_type",
      "operator": "in",
      "value": [
        "road_traffic",
        "water_supply",
        "gas_supply",
        "heating_supply",
        "electricity_supply"
      ]
    },
    {"field": "safety_component", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

### Annex III(3): Education and Vocational Training

#### R-HR-004: Educational Access Determination

**Legal Basis**: Article 6(2), Annex III(3)(a)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_education", "operator": "==", "value": true},
    {"field": "determines_educational_access", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-005: Learning Outcome Evaluation

**Legal Basis**: Article 6(2), Annex III(3)(b)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_education", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "evaluates_learning_outcomes", "operator": "==", "value": true},
        {"field": "exam_scoring", "operator": "==", "value": true}
      ]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-006: Education Level Assessment

**Legal Basis**: Article 6(2), Annex III(3)(c)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_education", "operator": "==", "value": true},
    {"field": "assesses_appropriate_education_level", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-007: Student Monitoring

**Legal Basis**: Article 6(2), Annex III(3)(d)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_education", "operator": "==", "value": true},
    {"field": "monitors_students", "operator": "==", "value": true},
    {"field": "detects_prohibited_behavior", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

### Annex III(4): Employment, Workers Management, Self-Employment

#### R-HR-008: Recruitment and Selection

**Legal Basis**: Article 6(2), Annex III(4)(a)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_employment", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "recruitment_or_selection", "operator": "==", "value": true},
        {"field": "purpose", "operator": "==", "value": "recruitment_screening"}
      ]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-009: Promotion and Termination Decisions

**Legal Basis**: Article 6(2), Annex III(4)(b)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_employment", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "promotion_or_termination_decisions", "operator": "==", "value": true},
        {"field": "purpose", "operator": "in", "value": ["promotion_decision", "termination_decision"]}
      ]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-010: Task Allocation

**Legal Basis**: Article 6(2), Annex III(4)(c)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_employment", "operator": "==", "value": true},
    {"field": "task_allocation", "operator": "==", "value": true},
    {"field": "based_on_individual_behavior", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-011: Performance Monitoring

**Legal Basis**: Article 6(2), Annex III(4)(d)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_employment", "operator": "==", "value": true},
    {"field": "performance_monitoring", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

### Annex III(5): Essential Private and Public Services

#### R-HR-012: Creditworthiness Assessment

**Legal Basis**: Article 6(2), Annex III(5)(b)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {
      "field": "sector",
      "operator": "in",
      "value": ["banking", "financial_services"]
    },
    {
      "operator": "OR",
      "criteria": [
        {"field": "creditworthiness_assessment", "operator": "==", "value": true},
        {"field": "purpose", "operator": "in", "value": ["creditworthiness_assessment", "loan_approval"]}
      ]
    },
    {"field": "purpose", "operator": "!=", "value": "fraud_detection"}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-013: Insurance Pricing and Risk Assessment

**Legal Basis**: Article 6(2), Annex III(5)(b)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "sector", "operator": "==", "value": "insurance"},
    {
      "operator": "OR",
      "criteria": [
        {"field": "purpose", "operator": "==", "value": "insurance_pricing"},
        {"field": "purpose", "operator": "==", "value": "risk_assessment"}
      ]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-014: Emergency Services Dispatch

**Legal Basis**: Article 6(2), Annex III(5)(c)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "emergency_services_dispatch", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "dispatches_emergency_services", "operator": "==", "value": true},
        {"field": "prioritizes_emergency_services", "operator": "==", "value": true}
      ]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-015: Public Assistance Benefits

**Legal Basis**: Article 6(2), Annex III(5)(a)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "evaluates_public_assistance", "operator": "==", "value": true},
    {"field": "deployer_type", "operator": "==", "value": "public_authority"}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

### Annex III(6): Law Enforcement

#### R-HR-016: Individual Risk Assessment (Law Enforcement)

**Legal Basis**: Article 6(2), Annex III(6)(a)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_law_enforcement", "operator": "==", "value": true},
    {"field": "individual_risk_assessment", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-017: Lie Detection (Law Enforcement)

**Legal Basis**: Article 6(2), Annex III(6)(b)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_law_enforcement", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "lie_detection", "operator": "==", "value": true},
        {"field": "detects_emotional_state", "operator": "==", "value": true}
      ]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-018: Evidence Reliability Assessment

**Legal Basis**: Article 6(2), Annex III(6)(c)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_law_enforcement", "operator": "==", "value": true},
    {"field": "evidence_reliability_assessment", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-019: Crime Prediction

**Legal Basis**: Article 6(2), Annex III(6)(d)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_law_enforcement", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "crime_prediction", "operator": "==", "value": true},
        {"field": "purpose", "operator": "==", "value": "predictive_policing"}
      ]
    }
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-020: Profiling During Investigation

**Legal Basis**: Article 6(2), Annex III(6)(e)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_law_enforcement", "operator": "==", "value": true},
    {"field": "profiling_during_investigation", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

### Annex III(7): Migration, Asylum, Border Control

#### R-HR-021: Polygraph/Lie Detection (Migration)

**Legal Basis**: Article 6(2), Annex III(7)(a)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_migration_asylum_border", "operator": "==", "value": true},
    {"field": "polygraph_or_lie_detection_migration", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-022: Risk Assessment (Migration)

**Legal Basis**: Article 6(2), Annex III(7)(b)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_migration_asylum_border", "operator": "==", "value": true},
    {"field": "risk_assessment_migration", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-023: Application Examination (Migration)

**Legal Basis**: Article 6(2), Annex III(7)(c)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_migration_asylum_border", "operator": "==", "value": true},
    {"field": "examines_applications", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-024: Identity Document Fraud Detection

**Legal Basis**: Article 6(2), Annex III(7)(d)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_migration_asylum_border", "operator": "==", "value": true},
    {"field": "detects_identity_fraud", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

### Annex III(8): Administration of Justice

#### R-HR-025: Judicial Research and Interpretation

**Legal Basis**: Article 6(2), Annex III(8)(a)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_justice_system", "operator": "==", "value": true},
    {"field": "assists_judicial_authority", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

#### R-HR-026: Application of Law to Facts

**Legal Basis**: Article 6(2), Annex III(8)(b)

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "used_in_justice_system", "operator": "==", "value": true},
    {"field": "applies_law_to_facts", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 1.0  
**Priority**: 2

---

## 3. GENERAL PURPOSE AI (GPAI)

### R-GPAI-001: General Purpose AI Model

**Legal Basis**: Article 3(44), Article 51

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "is_general_purpose_ai", "operator": "==", "value": true},
    {"field": "can_perform_multiple_tasks", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 0.90  
**Priority**: 3

---

### R-GPAI-002: GPAI with Systemic Risk

**Legal Basis**: Article 3(65), Article 51

**Conditions**:
```json
{
  "operator": "AND",
  "criteria": [
    {"field": "is_general_purpose_ai", "operator": "==", "value": true},
    {
      "operator": "OR",
      "criteria": [
        {"field": "training_compute", "operator": ">=", "value": 1e25},
        {"field": "has_high_impact_capabilities", "operator": "==", "value": true}
      ]
    }
  ]
}
```

**Confidence**: 0.95  
**Priority**: 2

---

## 4. LIMITED-RISK AI SYSTEMS

### R-LR-001: Transparency Obligations

**Legal Basis**: Article 52

**Conditions**:
```json
{
  "operator": "OR",
  "criteria": [
    {"field": "interacts_with_humans", "operator": "==", "value": true},
    {"field": "generates_synthetic_content", "operator": "==", "value": true},
    {"field": "performs_emotion_recognition", "operator": "==", "value": true},
    {"field": "performs_biometric_categorization", "operator": "==", "value": true}
  ]
}
```

**Confidence**: 0.85  
**Priority**: 4

---

## 5. MINIMAL-RISK AI SYSTEMS

### R-MR-001: Default Category

**Legal Basis**: Recital 6

**Description**: AI systems not falling into other categories

**Conditions**:
```json
{
  "operator": "NOT",
  "criteria": [
    {"matches_any_higher_risk_rule": true}
  ]
}
```

**Confidence**: 0.80  
**Priority**: 10 (Lowest)

---

## Rule Evaluation Logic

### Priority Order

1. **Priority 1**: Prohibited practices (highest priority)
2. **Priority 2**: High-risk systems
3. **Priority 3**: GPAI with systemic risk
4. **Priority 4**: Limited-risk systems
5. **Priority 10**: Minimal-risk (default)

### Conflict Resolution

When multiple rules match:

1. Select rule with highest priority
2. If same priority, select rule with highest confidence
3. If still tied, escalate to human review

### Confidence Thresholds

- **1.0**: Deterministic match, no ambiguity
- **0.95-0.99**: Very high confidence, minor edge cases
- **0.85-0.94**: High confidence, some interpretation needed
- **0.70-0.84**: Medium confidence, requires LLM reasoning
- **<0.70**: Low confidence, requires human review

---

## Rule Maintenance

### Version Control

- All rules are versioned
- Changes tracked in git
- Backward compatibility maintained

### Update Process

1. Identify need for new/updated rule
2. Draft rule with legal basis
3. Review by legal team
4. Test against validation dataset
5. Deploy with version increment
6. Document in changelog

### Testing

- Unit tests for each rule
- Integration tests for rule combinations
- Validation against known cases
- Regular audits for accuracy

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-11  
**Total Rules**: 35+  
**Maintained by**: Compliance Rules Team