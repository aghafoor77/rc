"""
AI System Metadata Schema

Comprehensive metadata schema for AI applications covering all aspects
required for EU AI Act compliance assessment.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


# ============================================================================
# Risk Categories
# ============================================================================

class RiskCategoryEnum(str, Enum):
    """EU AI Act Risk Categories"""
    PROHIBITED = "prohibited"
    HIGH_RISK = "high_risk"
    LIMITED_RISK = "limited_risk"
    MINIMAL_RISK = "minimal_risk"
    GPAI = "general_purpose_ai"
    GPAI_SYSTEMIC_RISK = "gpai_systemic_risk"
    UNCLASSIFIED = "unclassified"


# ============================================================================
# Model Lifecycle
# ============================================================================

class ModelLifecycleStage(str, Enum):
    """AI Model Lifecycle Stage"""
    RESEARCH = "research"
    DEVELOPMENT = "development"
    TESTING = "testing"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    PRODUCTION = "production"
    MONITORING = "monitoring"
    RETIRED = "retired"


class ModelProvenance(BaseModel):
    """Model origin and development information"""
    developer_organization: str = Field(..., description="Organization that developed the model")
    development_location: Optional[str] = Field(None, description="Country/region of development")
    development_date: Optional[datetime] = Field(None, description="Date model was developed")
    model_version: str = Field(..., description="Model version identifier")
    parent_model: Optional[str] = Field(None, description="Parent model if fine-tuned")
    is_fine_tuned: bool = Field(default=False, description="Is this a fine-tuned model?")
    base_model_name: Optional[str] = Field(None, description="Name of base model if fine-tuned")
    license: Optional[str] = Field(None, description="Model license (e.g., MIT, Apache 2.0)")
    is_open_source: bool = Field(default=False, description="Is the model open-source?")
    repository_url: Optional[HttpUrl] = Field(None, description="Code repository URL")
    model_card_url: Optional[HttpUrl] = Field(None, description="Model card URL")


class TrainingDataMetadata(BaseModel):
    """Training data characteristics"""
    dataset_name: Optional[str] = Field(None, description="Name of training dataset")
    dataset_size: Optional[str] = Field(None, description="Size of dataset (e.g., '10M samples')")
    data_sources: Optional[List[str]] = Field(None, description="Sources of training data")
    data_collection_period: Optional[str] = Field(None, description="Time period of data collection")
    geographic_coverage: Optional[List[str]] = Field(None, description="Geographic regions covered")
    languages: Optional[List[str]] = Field(None, description="Languages in dataset")
    demographic_representation: Optional[Dict[str, Any]] = Field(
        None,
        description="Demographics represented (age, gender, ethnicity, etc.)"
    )
    data_quality_metrics: Optional[Dict[str, float]] = Field(
        None,
        description="Data quality metrics (completeness, accuracy, etc.)"
    )
    contains_personal_data: bool = Field(..., description="Contains personal data?")
    contains_sensitive_data: bool = Field(..., description="Contains sensitive/special category data?")
    data_anonymization: Optional[str] = Field(None, description="Anonymization techniques applied")
    data_consent_obtained: Optional[bool] = Field(None, description="Was consent obtained for data use?")
    data_retention_policy: Optional[str] = Field(None, description="Data retention policy")


class ModelCapabilities(BaseModel):
    """AI model capabilities and limitations"""
    primary_capabilities: List[str] = Field(..., description="Primary capabilities of the model")
    secondary_capabilities: Optional[List[str]] = Field(None, description="Secondary capabilities")
    known_limitations: Optional[List[str]] = Field(None, description="Known limitations")
    failure_modes: Optional[List[str]] = Field(None, description="Known failure modes")
    edge_cases: Optional[List[str]] = Field(None, description="Problematic edge cases")
    out_of_scope_uses: Optional[List[str]] = Field(None, description="Uses explicitly out of scope")
    recommended_uses: Optional[List[str]] = Field(None, description="Recommended use cases")
    not_recommended_uses: Optional[List[str]] = Field(None, description="Not recommended use cases")


class PerformanceMetrics(BaseModel):
    """Model performance metrics"""
    accuracy: Optional[float] = Field(None, ge=0.0, le=1.0, description="Overall accuracy")
    precision: Optional[float] = Field(None, ge=0.0, le=1.0, description="Precision")
    recall: Optional[float] = Field(None, ge=0.0, le=1.0, description="Recall")
    f1_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="F1 score")
    auc_roc: Optional[float] = Field(None, ge=0.0, le=1.0, description="AUC-ROC")
    false_positive_rate: Optional[float] = Field(None, ge=0.0, le=1.0, description="False positive rate")
    false_negative_rate: Optional[float] = Field(None, ge=0.0, le=1.0, description="False negative rate")
    performance_by_subgroup: Optional[Dict[str, Dict[str, float]]] = Field(
        None,
        description="Performance metrics broken down by demographic subgroups"
    )
    benchmark_datasets: Optional[List[str]] = Field(None, description="Benchmark datasets used")
    evaluation_date: Optional[datetime] = Field(None, description="Date of evaluation")


# ============================================================================
# Deployment Environment
# ============================================================================

class DeploymentEnvironment(BaseModel):
    """Deployment environment details"""
    deployment_type: str = Field(
        ...,
        description="cloud, on-premise, edge, hybrid"
    )
    cloud_provider: Optional[str] = Field(None, description="Cloud provider if applicable")
    geographic_locations: List[str] = Field(..., description="Deployment locations (countries)")
    infrastructure_type: Optional[str] = Field(
        None,
        description="Infrastructure type (serverless, containers, VMs, etc.)"
    )
    scaling_capability: Optional[str] = Field(
        None,
        description="Scaling capability (manual, auto-scaling, etc.)"
    )
    availability_sla: Optional[str] = Field(None, description="Availability SLA (e.g., 99.9%)")
    disaster_recovery: bool = Field(..., description="Has disaster recovery plan?")
    backup_frequency: Optional[str] = Field(None, description="Backup frequency")


class IntegrationDetails(BaseModel):
    """Third-party integrations and dependencies"""
    integrated_systems: Optional[List[str]] = Field(None, description="Integrated systems")
    data_sources: Optional[List[str]] = Field(None, description="External data sources")
    apis_used: Optional[List[str]] = Field(None, description="External APIs used")
    third_party_models: Optional[List[str]] = Field(None, description="Third-party AI models used")
    dependencies: Optional[List[str]] = Field(None, description="Software dependencies")
    supply_chain_risk_assessment: bool = Field(
        ...,
        description="Has supply chain risk assessment been conducted?"
    )


# ============================================================================
# Safety and Security
# ============================================================================

class SafetyControls(BaseModel):
    """Safety control mechanisms"""
    has_safety_controls: bool = Field(..., description="Has safety controls implemented?")
    safety_mechanisms: Optional[List[str]] = Field(None, description="Safety mechanisms in place")
    fail_safe_mechanisms: Optional[List[str]] = Field(None, description="Fail-safe mechanisms")
    emergency_stop: bool = Field(default=False, description="Has emergency stop capability?")
    safety_testing: bool = Field(..., description="Has undergone safety testing?")
    safety_certification: Optional[str] = Field(None, description="Safety certifications obtained")
    hazard_analysis: bool = Field(..., description="Has hazard analysis been conducted?")
    risk_mitigation_measures: Optional[List[str]] = Field(
        None,
        description="Risk mitigation measures implemented"
    )


class CybersecurityControls(BaseModel):
    """Cybersecurity controls"""
    security_framework: Optional[str] = Field(
        None,
        description="Security framework followed (e.g., NIST, ISO 27001)"
    )
    encryption_at_rest: bool = Field(..., description="Data encrypted at rest?")
    encryption_in_transit: bool = Field(..., description="Data encrypted in transit?")
    access_control_mechanism: Optional[str] = Field(
        None,
        description="Access control mechanism (RBAC, ABAC, etc.)"
    )
    authentication_methods: Optional[List[str]] = Field(
        None,
        description="Authentication methods (MFA, SSO, etc.)"
    )
    vulnerability_scanning: bool = Field(..., description="Regular vulnerability scanning?")
    penetration_testing: bool = Field(..., description="Has undergone penetration testing?")
    security_incident_response: bool = Field(..., description="Has incident response plan?")
    security_monitoring: bool = Field(..., description="Has security monitoring?")
    threat_modeling: bool = Field(..., description="Has threat modeling been conducted?")


class AdversarialRobustness(BaseModel):
    """Adversarial robustness and red-teaming"""
    adversarial_testing: bool = Field(..., description="Has undergone adversarial testing?")
    red_team_testing: bool = Field(..., description="Has undergone red-team testing?")
    adversarial_attacks_tested: Optional[List[str]] = Field(
        None,
        description="Types of adversarial attacks tested"
    )
    robustness_metrics: Optional[Dict[str, float]] = Field(
        None,
        description="Robustness metrics"
    )
    adversarial_defenses: Optional[List[str]] = Field(
        None,
        description="Adversarial defense mechanisms"
    )
    prompt_injection_testing: bool = Field(
        default=False,
        description="Has undergone prompt injection testing?"
    )
    jailbreak_testing: bool = Field(
        default=False,
        description="Has undergone jailbreak testing?"
    )


# ============================================================================
# Human Oversight
# ============================================================================

class HumanOversightMechanisms(BaseModel):
    """Human oversight and control mechanisms"""
    oversight_level: str = Field(
        ...,
        description="human-in-the-loop, human-on-the-loop, human-in-command"
    )
    oversight_description: str = Field(..., description="Description of oversight mechanisms")
    can_override_decisions: bool = Field(..., description="Can humans override AI decisions?")
    override_process: Optional[str] = Field(None, description="Process for overriding decisions")
    human_review_frequency: Optional[str] = Field(None, description="Frequency of human review")
    escalation_criteria: Optional[List[str]] = Field(
        None,
        description="Criteria for escalating to human review"
    )
    training_for_overseers: bool = Field(..., description="Training provided to human overseers?")
    oversight_documentation: bool = Field(..., description="Oversight activities documented?")


# ============================================================================
# Transparency and Explainability
# ============================================================================

class TransparencyMeasures(BaseModel):
    """Transparency and explainability measures"""
    users_informed_of_ai: bool = Field(..., description="Users informed they're interacting with AI?")
    disclosure_method: Optional[str] = Field(None, description="Method of disclosure to users")
    explainability_provided: bool = Field(..., description="Explanations provided for decisions?")
    explainability_method: Optional[str] = Field(
        None,
        description="Explainability method (LIME, SHAP, attention, etc.)"
    )
    decision_transparency: Optional[str] = Field(
        None,
        description="Level of decision transparency (low, medium, high)"
    )
    model_interpretability: Optional[str] = Field(
        None,
        description="Model interpretability (black-box, gray-box, white-box)"
    )
    user_documentation: bool = Field(..., description="User documentation available?")
    technical_documentation: bool = Field(..., description="Technical documentation available?")


# ============================================================================
# Compliance and Governance
# ============================================================================

class ComplianceStatus(BaseModel):
    """Compliance status and certifications"""
    eu_ai_act_assessment_date: Optional[datetime] = Field(
        None,
        description="Date of EU AI Act assessment"
    )
    risk_category: Optional[RiskCategoryEnum] = Field(None, description="Assigned risk category")
    conformity_assessment_completed: bool = Field(
        default=False,
        description="Conformity assessment completed?"
    )
    notified_body: Optional[str] = Field(None, description="Notified body (if applicable)")
    ce_marking: bool = Field(default=False, description="Has CE marking?")
    registration_number: Optional[str] = Field(None, description="EU database registration number")
    other_certifications: Optional[List[str]] = Field(
        None,
        description="Other certifications (ISO, SOC2, etc.)"
    )
    gdpr_compliance: bool = Field(..., description="GDPR compliant?")
    dpia_completed: bool = Field(..., description="Data Protection Impact Assessment completed?")
    other_regulatory_approvals: Optional[List[str]] = Field(
        None,
        description="Other regulatory approvals"
    )


class GovernanceFramework(BaseModel):
    """AI governance framework"""
    has_ai_governance_policy: bool = Field(..., description="Has AI governance policy?")
    governance_framework: Optional[str] = Field(None, description="Governance framework used")
    responsible_ai_principles: Optional[List[str]] = Field(
        None,
        description="Responsible AI principles followed"
    )
    ethics_board: bool = Field(..., description="Has AI ethics board/committee?")
    ethics_review_conducted: bool = Field(..., description="Ethics review conducted?")
    stakeholder_engagement: bool = Field(..., description="Stakeholder engagement conducted?")
    impact_assessment_conducted: bool = Field(..., description="Impact assessment conducted?")
    risk_management_framework: Optional[str] = Field(
        None,
        description="Risk management framework"
    )


class AuditAndMonitoring(BaseModel):
    """Audit and monitoring practices"""
    audit_logging_enabled: bool = Field(..., description="Audit logging enabled?")
    log_retention_period: Optional[str] = Field(None, description="Log retention period")
    logs_immutable: bool = Field(..., description="Are logs immutable?")
    continuous_monitoring: bool = Field(..., description="Continuous monitoring in place?")
    performance_monitoring: bool = Field(..., description="Performance monitoring in place?")
    bias_monitoring: bool = Field(..., description="Bias monitoring in place?")
    drift_detection: bool = Field(..., description="Model drift detection in place?")
    incident_tracking: bool = Field(..., description="Incident tracking system in place?")
    regular_audits: bool = Field(..., description="Regular audits conducted?")
    audit_frequency: Optional[str] = Field(None, description="Audit frequency")
    third_party_audits: bool = Field(..., description="Third-party audits conducted?")


class PostMarketMonitoring(BaseModel):
    """Post-market monitoring and maintenance"""
    monitoring_plan: bool = Field(..., description="Has post-market monitoring plan?")
    monitoring_frequency: Optional[str] = Field(None, description="Monitoring frequency")
    performance_tracking: bool = Field(..., description="Performance tracked in production?")
    user_feedback_collection: bool = Field(..., description="User feedback collected?")
    incident_reporting_process: bool = Field(..., description="Incident reporting process in place?")
    update_frequency: Optional[str] = Field(None, description="Model update frequency")
    version_control: bool = Field(..., description="Version control in place?")
    rollback_capability: bool = Field(..., description="Can rollback to previous versions?")
    end_of_life_plan: bool = Field(..., description="Has end-of-life plan?")


# ============================================================================
# Stakeholder Information
# ============================================================================

class StakeholderImpact(BaseModel):
    """Impact on stakeholders"""
    affected_stakeholder_groups: List[str] = Field(
        ...,
        description="Groups affected by the AI system"
    )
    estimated_number_affected: Optional[str] = Field(
        None,
        description="Estimated number of people affected"
    )
    vulnerable_groups_affected: bool = Field(
        ...,
        description="Are vulnerable groups affected?"
    )
    vulnerable_groups_description: Optional[str] = Field(
        None,
        description="Description of vulnerable groups"
    )
    fundamental_rights_impact: bool = Field(
        ...,
        description="Could impact fundamental rights?"
    )
    fundamental_rights_list: Optional[List[str]] = Field(
        None,
        description="Fundamental rights potentially impacted"
    )
    discrimination_risk: bool = Field(..., description="Risk of discrimination?")
    discrimination_mitigation: Optional[List[str]] = Field(
        None,
        description="Discrimination mitigation measures"
    )
    redress_mechanism: bool = Field(..., description="Redress mechanism available?")
    redress_description: Optional[str] = Field(None, description="Description of redress mechanism")


# ============================================================================
# Complete AI System Metadata
# ============================================================================

class AISystemMetadata(BaseModel):
    """
    Comprehensive AI System Metadata Schema
    
    This schema captures all information required for EU AI Act compliance
    assessment, covering technical, operational, governance, and impact aspects.
    """
    
    # Basic Information
    system_id: Optional[str] = Field(None, description="Unique system identifier")
    system_name: str = Field(..., description="Name of the AI system")
    system_version: str = Field(..., description="Version of the AI system")
    system_description: str = Field(..., description="Detailed description")
    
    # Lifecycle
    lifecycle_stage: ModelLifecycleStage = Field(..., description="Current lifecycle stage")
    
    # Provenance
    provenance: ModelProvenance
    
    # Training Data
    training_data: TrainingDataMetadata
    
    # Capabilities
    capabilities: ModelCapabilities
    
    # Performance
    performance: PerformanceMetrics
    
    # Deployment
    deployment: DeploymentEnvironment
    
    # Integrations
    integrations: IntegrationDetails
    
    # Safety
    safety_controls: SafetyControls
    
    # Security
    cybersecurity: CybersecurityControls
    
    # Adversarial Robustness
    adversarial_robustness: AdversarialRobustness
    
    # Human Oversight
    human_oversight: HumanOversightMechanisms
    
    # Transparency
    transparency: TransparencyMeasures
    
    # Compliance
    compliance: ComplianceStatus
    
    # Governance
    governance: GovernanceFramework
    
    # Audit and Monitoring
    audit_monitoring: AuditAndMonitoring
    
    # Post-Market Monitoring
    post_market_monitoring: PostMarketMonitoring
    
    # Stakeholder Impact
    stakeholder_impact: StakeholderImpact
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(None, description="User who created this record")
    
    class Config:
        json_schema_extra = {
            "example": {
                "system_name": "Credit Scoring AI",
                "system_version": "2.1.0",
                "system_description": "AI system for automated creditworthiness assessment",
                "lifecycle_stage": "production",
                "provenance": {
                    "developer_organization": "Example Bank Ltd",
                    "model_version": "2.1.0",
                    "is_fine_tuned": False,
                    "is_open_source": False
                },
                "training_data": {
                    "dataset_size": "5M samples",
                    "contains_personal_data": True,
                    "contains_sensitive_data": False
                },
                "capabilities": {
                    "primary_capabilities": ["credit risk assessment", "default prediction"],
                    "known_limitations": ["Limited to consumer credit", "Requires minimum credit history"]
                },
                "performance": {
                    "accuracy": 0.87,
                    "precision": 0.85,
                    "recall": 0.89,
                    "f1_score": 0.87
                },
                "deployment": {
                    "deployment_type": "cloud",
                    "geographic_locations": ["DE"],
                    "disaster_recovery": True
                },
                "integrations": {
                    "supply_chain_risk_assessment": True
                },
                "safety_controls": {
                    "has_safety_controls": True,
                    "safety_testing": True,
                    "hazard_analysis": True
                },
                "cybersecurity": {
                    "encryption_at_rest": True,
                    "encryption_in_transit": True,
                    "vulnerability_scanning": True,
                    "penetration_testing": True,
                    "security_incident_response": True,
                    "security_monitoring": True,
                    "threat_modeling": True
                },
                "adversarial_robustness": {
                    "adversarial_testing": True,
                    "red_team_testing": False,
                    "prompt_injection_testing": False,
                    "jailbreak_testing": False
                },
                "human_oversight": {
                    "oversight_level": "human-on-the-loop",
                    "oversight_description": "Credit officers review high-risk cases",
                    "can_override_decisions": True,
                    "training_for_overseers": True,
                    "oversight_documentation": True
                },
                "transparency": {
                    "users_informed_of_ai": True,
                    "explainability_provided": True,
                    "user_documentation": True,
                    "technical_documentation": True
                },
                "compliance": {
                    "conformity_assessment_completed": False,
                    "ce_marking": False,
                    "gdpr_compliance": True,
                    "dpia_completed": True
                },
                "governance": {
                    "has_ai_governance_policy": True,
                    "ethics_board": True,
                    "ethics_review_conducted": True,
                    "stakeholder_engagement": True,
                    "impact_assessment_conducted": True
                },
                "audit_monitoring": {
                    "audit_logging_enabled": True,
                    "logs_immutable": True,
                    "continuous_monitoring": True,
                    "performance_monitoring": True,
                    "bias_monitoring": True,
                    "drift_detection": True,
                    "incident_tracking": True,
                    "regular_audits": True,
                    "third_party_audits": True
                },
                "post_market_monitoring": {
                    "monitoring_plan": True,
                    "performance_tracking": True,
                    "user_feedback_collection": True,
                    "incident_reporting_process": True,
                    "version_control": True,
                    "rollback_capability": True,
                    "end_of_life_plan": True
                },
                "stakeholder_impact": {
                    "affected_stakeholder_groups": ["loan applicants", "bank customers"],
                    "vulnerable_groups_affected": False,
                    "fundamental_rights_impact": True,
                    "fundamental_rights_list": ["right to non-discrimination", "right to fair treatment"],
                    "discrimination_risk": True,
                    "redress_mechanism": True
                }
            }
        }

# Made with Bob
