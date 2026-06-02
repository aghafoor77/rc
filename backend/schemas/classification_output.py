"""
Classification Output Schema

Defines the structure of classification results, compliance reports,
and audit outputs for EU AI Act assessments.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# ============================================================================
# Risk Categories
# ============================================================================

class RiskCategory(str, Enum):
    """EU AI Act Risk Categories"""
    PROHIBITED = "PROHIBITED"
    HIGH_RISK = "HIGH_RISK"
    LIMITED_RISK = "LIMITED_RISK"
    MINIMAL_RISK = "MINIMAL_RISK"
    GPAI = "GENERAL_PURPOSE_AI"
    GPAI_SYSTEMIC_RISK = "GPAI_SYSTEMIC_RISK"
    UNCLASSIFIED = "UNCLASSIFIED"


class ConfidenceLevel(str, Enum):
    """Confidence level in classification"""
    VERY_HIGH = "VERY_HIGH"  # 0.95-1.0
    HIGH = "HIGH"  # 0.85-0.95
    MEDIUM = "MEDIUM"  # 0.70-0.85
    LOW = "LOW"  # 0.50-0.70
    VERY_LOW = "VERY_LOW"  # 0.0-0.50


# ============================================================================
# Legal Basis
# ============================================================================

class LegalArticle(BaseModel):
    """EU AI Act legal article reference"""
    article_number: str = Field(..., description="Article number (e.g., 'Article 5', 'Article 6(2)')")
    article_title: Optional[str] = Field(None, description="Article title")
    relevant_text: Optional[str] = Field(None, description="Relevant excerpt from article")
    annex_reference: Optional[str] = Field(None, description="Annex reference if applicable")


class LegalBasis(BaseModel):
    """Legal basis for classification"""
    primary_article: str = Field(..., description="Primary legal article")
    primary_article_details: LegalArticle
    supporting_articles: List[LegalArticle] = Field(
        default_factory=list,
        description="Supporting legal articles"
    )
    relevant_recitals: Optional[List[str]] = Field(
        None,
        description="Relevant recitals from EU AI Act"
    )
    annex_references: Optional[List[str]] = Field(
        None,
        description="References to annexes"
    )


# ============================================================================
# Reasoning Chain
# ============================================================================

class ReasoningStep(BaseModel):
    """Single step in reasoning chain"""
    step_number: int = Field(..., description="Step number in sequence")
    description: str = Field(..., description="Description of reasoning step")
    evidence: Optional[List[str]] = Field(None, description="Evidence supporting this step")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence in this step")


class ReasoningChain(BaseModel):
    """Complete reasoning chain for classification"""
    steps: List[ReasoningStep] = Field(..., description="Reasoning steps")
    conclusion: str = Field(..., description="Final conclusion")
    alternative_interpretations: Optional[List[str]] = Field(
        None,
        description="Alternative interpretations considered"
    )


# ============================================================================
# Detected Risks
# ============================================================================

class DetectedRisk(BaseModel):
    """Individual detected risk"""
    risk_id: str = Field(..., description="Unique risk identifier")
    risk_category: str = Field(..., description="Category of risk")
    risk_description: str = Field(..., description="Description of the risk")
    severity: str = Field(..., description="Severity: CRITICAL, HIGH, MEDIUM, LOW")
    likelihood: Optional[str] = Field(None, description="Likelihood: VERY_HIGH, HIGH, MEDIUM, LOW")
    impact: Optional[str] = Field(None, description="Impact: CRITICAL, HIGH, MEDIUM, LOW")
    legal_basis: Optional[str] = Field(None, description="Legal basis for this risk")
    mitigation_required: bool = Field(..., description="Is mitigation required?")
    mitigation_recommendations: Optional[List[str]] = Field(
        None,
        description="Recommended mitigation measures"
    )


# ============================================================================
# Compliance Obligations
# ============================================================================

class ComplianceObligation(BaseModel):
    """Individual compliance obligation"""
    obligation_id: str = Field(..., description="Unique obligation identifier")
    article: str = Field(..., description="EU AI Act article")
    obligation_title: str = Field(..., description="Title of obligation")
    obligation_description: str = Field(..., description="Detailed description")
    requirements: List[str] = Field(..., description="Specific requirements")
    severity: str = Field(..., description="MANDATORY, RECOMMENDED, OPTIONAL")
    deadline: Optional[str] = Field(None, description="Compliance deadline if applicable")
    status: Optional[str] = Field(
        None,
        description="Current status: NOT_STARTED, IN_PROGRESS, COMPLETED, NOT_APPLICABLE"
    )
    evidence_required: Optional[List[str]] = Field(
        None,
        description="Evidence required to demonstrate compliance"
    )
    guidance_links: Optional[List[str]] = Field(
        None,
        description="Links to guidance documents"
    )


class ComplianceObligations(BaseModel):
    """Complete set of compliance obligations"""
    total_obligations: int = Field(..., description="Total number of obligations")
    mandatory_obligations: List[ComplianceObligation] = Field(
        default_factory=list,
        description="Mandatory obligations"
    )
    recommended_obligations: List[ComplianceObligation] = Field(
        default_factory=list,
        description="Recommended obligations"
    )
    optional_obligations: List[ComplianceObligation] = Field(
        default_factory=list,
        description="Optional obligations"
    )


# ============================================================================
# Gap Analysis
# ============================================================================

class ComplianceGap(BaseModel):
    """Identified compliance gap"""
    gap_id: str = Field(..., description="Unique gap identifier")
    obligation_id: str = Field(..., description="Related obligation ID")
    gap_description: str = Field(..., description="Description of the gap")
    severity: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
    current_state: str = Field(..., description="Current state")
    required_state: str = Field(..., description="Required state")
    remediation_steps: List[str] = Field(..., description="Steps to close the gap")
    estimated_effort: Optional[str] = Field(None, description="Estimated effort to close gap")
    priority: Optional[int] = Field(None, description="Priority (1=highest)")


class GapAnalysis(BaseModel):
    """Complete gap analysis"""
    total_gaps: int = Field(..., description="Total number of gaps identified")
    critical_gaps: List[ComplianceGap] = Field(default_factory=list)
    high_priority_gaps: List[ComplianceGap] = Field(default_factory=list)
    medium_priority_gaps: List[ComplianceGap] = Field(default_factory=list)
    low_priority_gaps: List[ComplianceGap] = Field(default_factory=list)
    overall_compliance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall compliance score (0-1)"
    )


# ============================================================================
# Missing Information
# ============================================================================

class MissingInformation(BaseModel):
    """Information missing from assessment"""
    field_name: str = Field(..., description="Name of missing field")
    field_description: str = Field(..., description="Description of what's missing")
    importance: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
    impact_on_classification: str = Field(
        ...,
        description="How missing info impacts classification"
    )
    how_to_obtain: Optional[str] = Field(None, description="How to obtain this information")


# ============================================================================
# Ambiguities
# ============================================================================

class Ambiguity(BaseModel):
    """Ambiguous aspect of classification"""
    ambiguity_id: str = Field(..., description="Unique ambiguity identifier")
    description: str = Field(..., description="Description of ambiguity")
    possible_interpretations: List[str] = Field(
        ...,
        description="Possible interpretations"
    )
    recommended_interpretation: str = Field(
        ...,
        description="Recommended interpretation"
    )
    requires_legal_review: bool = Field(
        ...,
        description="Requires legal expert review?"
    )
    additional_information_needed: Optional[List[str]] = Field(
        None,
        description="Additional information that would resolve ambiguity"
    )


# ============================================================================
# Remediation Recommendations
# ============================================================================

class RemediationRecommendation(BaseModel):
    """Remediation recommendation"""
    recommendation_id: str = Field(..., description="Unique recommendation identifier")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed description")
    priority: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
    category: str = Field(
        ...,
        description="Category: TECHNICAL, ORGANIZATIONAL, LEGAL, DOCUMENTATION"
    )
    implementation_steps: List[str] = Field(..., description="Implementation steps")
    estimated_effort: Optional[str] = Field(None, description="Estimated effort")
    estimated_cost: Optional[str] = Field(None, description="Estimated cost")
    timeline: Optional[str] = Field(None, description="Recommended timeline")
    dependencies: Optional[List[str]] = Field(None, description="Dependencies")
    success_criteria: Optional[List[str]] = Field(None, description="Success criteria")


# ============================================================================
# Audit Trail
# ============================================================================

class RuleEvaluation(BaseModel):
    """Rule evaluation result"""
    rule_id: str = Field(..., description="Rule identifier")
    rule_name: str = Field(..., description="Rule name")
    matched: bool = Field(..., description="Did rule match?")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in match")
    conditions_evaluated: Dict[str, Any] = Field(..., description="Conditions evaluated")
    result: Optional[str] = Field(None, description="Result if matched")


class LLMReasoning(BaseModel):
    """LLM reasoning details"""
    model_name: str = Field(..., description="LLM model used")
    model_version: Optional[str] = Field(None, description="Model version")
    prompt_template: str = Field(..., description="Prompt template used")
    prompt_tokens: int = Field(..., description="Number of prompt tokens")
    completion_tokens: int = Field(..., description="Number of completion tokens")
    total_tokens: int = Field(..., description="Total tokens used")
    temperature: float = Field(..., description="Temperature setting")
    raw_response: str = Field(..., description="Raw LLM response")
    parsed_response: Dict[str, Any] = Field(..., description="Parsed response")
    reasoning_steps: List[str] = Field(..., description="LLM reasoning steps")


class RAGRetrieval(BaseModel):
    """RAG retrieval details"""
    query: str = Field(..., description="Query used for retrieval")
    num_documents_retrieved: int = Field(..., description="Number of documents retrieved")
    documents: List[Dict[str, Any]] = Field(..., description="Retrieved documents")
    relevance_scores: List[float] = Field(..., description="Relevance scores")
    sources: List[str] = Field(..., description="Source documents")


class ProcessingStep(BaseModel):
    """Individual processing step"""
    step_name: str = Field(..., description="Name of processing step")
    timestamp: datetime = Field(..., description="Timestamp of step")
    duration_ms: int = Field(..., description="Duration in milliseconds")
    status: str = Field(..., description="SUCCESS, FAILED, SKIPPED")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")
    error: Optional[str] = Field(None, description="Error message if failed")


class AuditTrail(BaseModel):
    """Complete audit trail"""
    assessment_id: str = Field(..., description="Unique assessment identifier")
    timestamp: datetime = Field(..., description="Assessment timestamp")
    user_id: Optional[str] = Field(None, description="User who initiated assessment")
    session_id: Optional[str] = Field(None, description="Session identifier")
    
    processing_steps: List[ProcessingStep] = Field(..., description="Processing steps")
    
    rules_evaluated: List[RuleEvaluation] = Field(
        default_factory=list,
        description="Rules evaluated"
    )
    rules_matched: List[str] = Field(default_factory=list, description="Rules that matched")
    
    llm_reasoning: Optional[LLMReasoning] = Field(None, description="LLM reasoning details")
    
    rag_retrieval: Optional[RAGRetrieval] = Field(None, description="RAG retrieval details")
    
    total_duration_ms: int = Field(..., description="Total processing duration")
    
    hash: Optional[str] = Field(None, description="SHA-256 hash of audit trail")
    previous_hash: Optional[str] = Field(None, description="Hash of previous audit entry")


# ============================================================================
# Human Review
# ============================================================================

class HumanReviewRequest(BaseModel):
    """Human review request"""
    requires_review: bool = Field(..., description="Requires human review?")
    review_reason: Optional[str] = Field(None, description="Reason for review")
    review_priority: Optional[str] = Field(None, description="URGENT, HIGH, MEDIUM, LOW")
    suggested_reviewers: Optional[List[str]] = Field(None, description="Suggested reviewers")
    review_deadline: Optional[datetime] = Field(None, description="Review deadline")
    review_questions: Optional[List[str]] = Field(
        None,
        description="Specific questions for reviewer"
    )


class HumanReviewResult(BaseModel):
    """Human review result"""
    reviewed_by: str = Field(..., description="Reviewer name/ID")
    review_date: datetime = Field(..., description="Review date")
    review_decision: str = Field(
        ...,
        description="APPROVED, REJECTED, MODIFIED, ESCALATED"
    )
    reviewer_comments: Optional[str] = Field(None, description="Reviewer comments")
    modified_classification: Optional[RiskCategory] = Field(
        None,
        description="Modified classification if changed"
    )
    modified_confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Modified confidence if changed"
    )
    additional_obligations: Optional[List[str]] = Field(
        None,
        description="Additional obligations identified"
    )
    justification: Optional[str] = Field(None, description="Justification for decision")


# ============================================================================
# Complete Classification Result
# ============================================================================

class ClassificationResult(BaseModel):
    """
    Complete EU AI Act Classification Result
    
    This is the primary output of the classification system, containing
    all information needed for compliance assessment and audit.
    """
    
    # Identification
    assessment_id: str = Field(..., description="Unique assessment identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Assessment timestamp")
    system_name: str = Field(..., description="Name of assessed AI system")
    system_version: str = Field(..., description="Version of assessed AI system")
    
    # Classification
    risk_category: RiskCategory = Field(..., description="Assigned risk category")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    confidence_level: ConfidenceLevel = Field(..., description="Confidence level")
    
    # Legal Basis
    legal_basis: LegalBasis = Field(..., description="Legal basis for classification")
    
    # Reasoning
    reasoning_chain: ReasoningChain = Field(..., description="Reasoning chain")
    
    # Risks
    detected_risks: List[DetectedRisk] = Field(
        default_factory=list,
        description="Detected risks"
    )
    total_risks: int = Field(..., description="Total number of risks detected")
    critical_risks: int = Field(..., description="Number of critical risks")
    
    # Compliance
    compliance_obligations: ComplianceObligations = Field(
        ...,
        description="Compliance obligations"
    )
    
    # Gap Analysis
    gap_analysis: GapAnalysis = Field(..., description="Gap analysis")
    
    # Missing Information
    missing_information: List[MissingInformation] = Field(
        default_factory=list,
        description="Missing information"
    )
    
    # Ambiguities
    ambiguities: List[Ambiguity] = Field(
        default_factory=list,
        description="Ambiguities in classification"
    )
    
    # Recommendations
    remediation_recommendations: List[RemediationRecommendation] = Field(
        default_factory=list,
        description="Remediation recommendations"
    )
    
    # Human Review
    human_review_request: HumanReviewRequest = Field(
        ...,
        description="Human review request"
    )
    human_review_result: Optional[HumanReviewResult] = Field(
        None,
        description="Human review result (if completed)"
    )
    
    # Audit Trail
    audit_trail: AuditTrail = Field(..., description="Audit trail")
    
    # Metadata
    classification_version: str = Field(
        default="1.0",
        description="Classification system version"
    )
    eu_ai_act_version: str = Field(
        default="2024",
        description="EU AI Act version used"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2026-05-11T13:30:00Z",
                "system_name": "Credit Scoring System",
                "system_version": "2.1.0",
                "risk_category": "HIGH_RISK",
                "confidence_score": 0.95,
                "confidence_level": "VERY_HIGH",
                "legal_basis": {
                    "primary_article": "Article 6(2), Annex III(5)(b)",
                    "primary_article_details": {
                        "article_number": "Article 6(2)",
                        "article_title": "Classification rules for high-risk AI systems"
                    },
                    "supporting_articles": [
                        {
                            "article_number": "Article 9",
                            "article_title": "Risk management system"
                        }
                    ]
                },
                "reasoning_chain": {
                    "steps": [
                        {
                            "step_number": 1,
                            "description": "System operates in banking sector",
                            "confidence": 1.0
                        },
                        {
                            "step_number": 2,
                            "description": "Makes automated creditworthiness decisions",
                            "confidence": 1.0
                        },
                        {
                            "step_number": 3,
                            "description": "Impacts access to financial services",
                            "confidence": 0.95
                        }
                    ],
                    "conclusion": "System matches Annex III(5)(b) criteria for high-risk AI"
                },
                "detected_risks": [
                    {
                        "risk_id": "RISK-001",
                        "risk_category": "DISCRIMINATION",
                        "risk_description": "Potential for discriminatory outcomes in credit decisions",
                        "severity": "HIGH",
                        "mitigation_required": True
                    }
                ],
                "total_risks": 3,
                "critical_risks": 0,
                "compliance_obligations": {
                    "total_obligations": 15,
                    "mandatory_obligations": [
                        {
                            "obligation_id": "OBL-001",
                            "article": "Article 9",
                            "obligation_title": "Risk Management System",
                            "obligation_description": "Establish and maintain risk management system",
                            "requirements": [
                                "Identify and analyze known and foreseeable risks",
                                "Estimate and evaluate risks",
                                "Adopt suitable risk management measures"
                            ],
                            "severity": "MANDATORY"
                        }
                    ],
                    "recommended_obligations": [],
                    "optional_obligations": []
                },
                "gap_analysis": {
                    "total_gaps": 5,
                    "critical_gaps": [],
                    "high_priority_gaps": [
                        {
                            "gap_id": "GAP-001",
                            "obligation_id": "OBL-001",
                            "gap_description": "Bias testing not comprehensive",
                            "severity": "HIGH",
                            "current_state": "Basic bias testing conducted",
                            "required_state": "Comprehensive bias testing across all demographics",
                            "remediation_steps": [
                                "Expand bias testing to cover all protected attributes",
                                "Document testing methodology",
                                "Establish ongoing monitoring"
                            ],
                            "priority": 1
                        }
                    ],
                    "medium_priority_gaps": [],
                    "low_priority_gaps": [],
                    "overall_compliance_score": 0.75
                },
                "missing_information": [
                    {
                        "field_name": "training_data_demographics",
                        "field_description": "Demographics represented in training data",
                        "importance": "HIGH",
                        "impact_on_classification": "Needed for bias assessment"
                    }
                ],
                "ambiguities": [],
                "remediation_recommendations": [
                    {
                        "recommendation_id": "REC-001",
                        "title": "Implement Comprehensive Bias Testing",
                        "description": "Expand bias testing to cover all protected attributes",
                        "priority": "HIGH",
                        "category": "TECHNICAL",
                        "implementation_steps": [
                            "Define protected attributes",
                            "Collect demographic data",
                            "Run fairness metrics",
                            "Document results"
                        ]
                    }
                ],
                "human_review_request": {
                    "requires_review": False,
                    "review_reason": None
                },
                "audit_trail": {
                    "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
                    "timestamp": "2026-05-11T13:30:00Z",
                    "processing_steps": [
                        {
                            "step_name": "rule_engine",
                            "timestamp": "2026-05-11T13:30:00.100Z",
                            "duration_ms": 150,
                            "status": "SUCCESS"
                        }
                    ],
                    "rules_matched": ["R-HR-005", "R-HR-012"],
                    "total_duration_ms": 2000
                }
            }
        }


# ============================================================================
# Report Formats
# ============================================================================

class ComplianceReport(BaseModel):
    """Compliance report for stakeholders"""
    report_id: str = Field(..., description="Unique report identifier")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    report_type: str = Field(..., description="EXECUTIVE_SUMMARY, DETAILED, TECHNICAL, AUDIT")
    
    classification_result: ClassificationResult
    
    executive_summary: str = Field(..., description="Executive summary")
    key_findings: List[str] = Field(..., description="Key findings")
    recommendations_summary: List[str] = Field(..., description="Summary of recommendations")
    
    next_steps: List[str] = Field(..., description="Recommended next steps")
    
    report_format: str = Field(default="JSON", description="JSON, PDF, HTML")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "REP-550e8400",
                "generated_at": "2026-05-11T13:30:00Z",
                "report_type": "EXECUTIVE_SUMMARY",
                "executive_summary": "The Credit Scoring System has been classified as HIGH_RISK under the EU AI Act...",
                "key_findings": [
                    "System classified as HIGH_RISK (Annex III(5)(b))",
                    "15 mandatory compliance obligations identified",
                    "5 compliance gaps requiring remediation",
                    "Overall compliance score: 75%"
                ],
                "recommendations_summary": [
                    "Implement comprehensive bias testing",
                    "Enhance human oversight mechanisms",
                    "Complete technical documentation"
                ],
                "next_steps": [
                    "Address high-priority compliance gaps",
                    "Conduct conformity assessment",
                    "Register in EU database"
                ]
            }
        }

# Made with Bob
