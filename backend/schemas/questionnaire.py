"""
EU AI Act Compliance Questionnaire Schema

Comprehensive questionnaire for determining AI system risk classification
under the EU AI Act. Covers all risk categories, prohibited practices,
high-risk systems, GPAI, and compliance requirements.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


# ============================================================================
# Enumerations
# ============================================================================

class SectorEnum(str, Enum):
    """Industry sectors"""
    BANKING = "banking"
    FINANCIAL_SERVICES = "financial_services"
    INSURANCE = "insurance"
    HEALTHCARE = "healthcare"
    MEDICAL_DEVICES = "medical_devices"
    EDUCATION = "education"
    VOCATIONAL_TRAINING = "vocational_training"
    RECRUITMENT = "recruitment"
    HR_MANAGEMENT = "hr_management"
    LAW_ENFORCEMENT = "law_enforcement"
    BORDER_CONTROL = "border_control"
    MIGRATION = "migration"
    ASYLUM = "asylum"
    JUSTICE = "justice"
    CRITICAL_INFRASTRUCTURE = "critical_infrastructure"
    ENERGY = "energy"
    TRANSPORTATION = "transportation"
    WATER_SUPPLY = "water_supply"
    TELECOMMUNICATIONS = "telecommunications"
    GOVERNMENT_SERVICES = "government_services"
    SOCIAL_SERVICES = "social_services"
    ECOMMERCE = "ecommerce"
    MANUFACTURING = "manufacturing"
    INDUSTRIAL_AUTOMATION = "industrial_automation"
    SOCIAL_MEDIA = "social_media"
    CONTENT_MODERATION = "content_moderation"
    CYBERSECURITY = "cybersecurity"
    CONSUMER_APPLICATIONS = "consumer_applications"
    GENERATIVE_AI = "generative_ai"
    FOUNDATION_MODELS = "foundation_models"
    OTHER = "other"


class PurposeEnum(str, Enum):
    """AI system purposes"""
    BIOMETRIC_IDENTIFICATION = "biometric_identification"
    BIOMETRIC_CATEGORIZATION = "biometric_categorization"
    EMOTION_RECOGNITION = "emotion_recognition"
    SOCIAL_SCORING = "social_scoring"
    CREDITWORTHINESS_ASSESSMENT = "creditworthiness_assessment"
    LOAN_APPROVAL = "loan_approval"
    INSURANCE_PRICING = "insurance_pricing"
    RISK_ASSESSMENT = "risk_assessment"
    FRAUD_DETECTION = "fraud_detection"
    MEDICAL_DIAGNOSIS = "medical_diagnosis"
    TREATMENT_RECOMMENDATION = "treatment_recommendation"
    PATIENT_TRIAGE = "patient_triage"
    EDUCATIONAL_ASSESSMENT = "educational_assessment"
    EXAM_SCORING = "exam_scoring"
    ADMISSION_DECISION = "admission_decision"
    RECRUITMENT_SCREENING = "recruitment_screening"
    HIRING_DECISION = "hiring_decision"
    PERFORMANCE_EVALUATION = "performance_evaluation"
    PROMOTION_DECISION = "promotion_decision"
    TASK_ALLOCATION = "task_allocation"
    PREDICTIVE_POLICING = "predictive_policing"
    CRIME_RISK_ASSESSMENT = "crime_risk_assessment"
    LIE_DETECTION = "lie_detection"
    EVIDENCE_EVALUATION = "evidence_evaluation"
    BORDER_SCREENING = "border_screening"
    VISA_ASSESSMENT = "visa_assessment"
    ASYLUM_EVALUATION = "asylum_evaluation"
    INFRASTRUCTURE_MANAGEMENT = "infrastructure_management"
    SAFETY_MONITORING = "safety_monitoring"
    AUTONOMOUS_DRIVING = "autonomous_driving"
    CONTENT_RECOMMENDATION = "content_recommendation"
    CONTENT_MODERATION_AI = "content_moderation_ai"
    PERSONALIZATION = "personalization"
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    CODE_GENERATION = "code_generation"
    DEEPFAKE_CREATION = "deepfake_creation"
    VULNERABILITY_DETECTION = "vulnerability_detection"
    THREAT_DETECTION = "threat_detection"
    PROCESS_AUTOMATION = "process_automation"
    QUALITY_CONTROL = "quality_control"
    PREDICTIVE_MAINTENANCE = "predictive_maintenance"
    OTHER = "other"


class DeployerTypeEnum(str, Enum):
    """Type of organization deploying the AI system"""
    PUBLIC_AUTHORITY = "public_authority"
    PRIVATE_COMPANY = "private_company"
    NON_PROFIT = "non_profit"
    RESEARCH_INSTITUTION = "research_institution"
    INDIVIDUAL = "individual"
    OTHER = "other"


class AutonomyLevelEnum(str, Enum):
    """Level of automation in decision-making"""
    FULLY_AUTOMATED = "fully_automated"
    SEMI_AUTOMATED = "semi_automated"
    HUMAN_IN_THE_LOOP = "human_in_the_loop"
    HUMAN_ON_THE_LOOP = "human_on_the_loop"
    ADVISORY_ONLY = "advisory_only"


class DataSensitivityEnum(str, Enum):
    """Sensitivity level of processed data"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SENSITIVE_PERSONAL = "sensitive_personal"
    SPECIAL_CATEGORY = "special_category"  # GDPR Article 9


class GeographicScopeEnum(str, Enum):
    """Geographic deployment scope"""
    SINGLE_EU_COUNTRY = "single_eu_country"
    MULTIPLE_EU_COUNTRIES = "multiple_eu_countries"
    EU_WIDE = "eu_wide"
    GLOBAL = "global"


class ModelTypeEnum(str, Enum):
    """Type of AI model"""
    MACHINE_LEARNING = "machine_learning"
    DEEP_LEARNING = "deep_learning"
    NEURAL_NETWORK = "neural_network"
    TRANSFORMER = "transformer"
    LARGE_LANGUAGE_MODEL = "large_language_model"
    COMPUTER_VISION = "computer_vision"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    GENERATIVE_MODEL = "generative_model"
    RULE_BASED = "rule_based"
    HYBRID = "hybrid"
    OTHER = "other"


# ============================================================================
# Questionnaire Sections
# ============================================================================

class BasicInformation(BaseModel):
    """Section 1: Basic AI System Information"""
    
    system_name: str = Field(..., description="Name of the AI system")
    system_version: str = Field(..., description="Version of the AI system")
    system_description: str = Field(..., description="Detailed description of the AI system")
    
    sector: SectorEnum = Field(..., description="Primary industry sector")
    additional_sectors: Optional[List[SectorEnum]] = Field(
        default=None, 
        description="Additional sectors if applicable"
    )
    
    purpose: PurposeEnum = Field(..., description="Primary purpose of the AI system")
    additional_purposes: Optional[List[PurposeEnum]] = Field(
        default=None,
        description="Additional purposes if applicable"
    )
    
    deployer_type: DeployerTypeEnum = Field(..., description="Type of deploying organization")
    deployer_name: str = Field(..., description="Name of deploying organization")
    
    provider_name: Optional[str] = Field(None, description="Name of AI system provider/developer")
    is_third_party_system: bool = Field(..., description="Is this a third-party AI system?")
    
    geographic_scope: GeographicScopeEnum = Field(..., description="Geographic deployment scope")
    deployment_countries: Optional[List[str]] = Field(
        None,
        description="List of countries where deployed (ISO codes)"
    )
    
    deployment_date: Optional[str] = Field(None, description="Planned or actual deployment date (ISO format)")
    is_already_deployed: bool = Field(..., description="Is the system already in production?")


class ProhibitedPracticesAssessment(BaseModel):
    """Section 2: Prohibited AI Practices (Article 5)"""
    
    # Article 5(1)(a): Subliminal manipulation
    uses_subliminal_techniques: bool = Field(
        ...,
        description="Does the system use subliminal techniques beyond conscious awareness?"
    )
    manipulates_behavior: bool = Field(
        ...,
        description="Does it manipulate behavior in ways that cause harm?"
    )
    
    # Article 5(1)(b): Exploitation of vulnerabilities
    targets_vulnerable_groups: bool = Field(
        ...,
        description="Does it target vulnerable groups (age, disability, social/economic situation)?"
    )
    exploits_vulnerabilities: bool = Field(
        ...,
        description="Does it exploit vulnerabilities to distort behavior causing harm?"
    )
    vulnerable_groups_description: Optional[str] = Field(
        None,
        description="Describe vulnerable groups if applicable"
    )
    
    # Article 5(1)(c): Social scoring
    performs_social_scoring: bool = Field(
        ...,
        description="Does it evaluate or classify trustworthiness of natural persons?"
    )
    social_scoring_by_public_authority: bool = Field(
        ...,
        description="Is social scoring performed by or on behalf of public authorities?"
    )
    social_scoring_scope: Optional[str] = Field(
        None,
        description="Describe scope of social scoring if applicable"
    )
    leads_to_detrimental_treatment: bool = Field(
        default=False,
        description="Could it lead to detrimental treatment unjustified by conduct?"
    )
    
    # Article 5(1)(d): Risk assessment for criminal offenses
    predicts_criminal_offense_risk: bool = Field(
        ...,
        description="Does it assess risk of committing criminal offenses?"
    )
    based_solely_on_profiling: bool = Field(
        default=False,
        description="Is prediction based solely on profiling or personality traits?"
    )
    
    # Article 5(1)(e): Biometric databases (scraping)
    creates_facial_recognition_database: bool = Field(
        ...,
        description="Does it create/expand facial recognition databases?"
    )
    uses_untargeted_scraping: bool = Field(
        default=False,
        description="Uses untargeted scraping from internet or CCTV?"
    )
    
    # Article 5(1)(f): Emotion recognition (workplace/education)
    performs_emotion_recognition: bool = Field(
        ...,
        description="Does it infer emotions of natural persons?"
    )
    emotion_recognition_in_workplace: bool = Field(
        default=False,
        description="Used in workplace context?"
    )
    emotion_recognition_in_education: bool = Field(
        default=False,
        description="Used in educational institutions?"
    )
    emotion_recognition_justification: Optional[str] = Field(
        None,
        description="Medical or safety reasons justification if applicable"
    )
    
    # Article 5(1)(g): Biometric categorization
    performs_biometric_categorization: bool = Field(
        ...,
        description="Does it categorize persons based on biometric data?"
    )
    infers_sensitive_attributes: bool = Field(
        default=False,
        description="Infers race, political opinions, trade union membership, religious beliefs, sex life, sexual orientation?"
    )
    
    # Article 5(1)(h): Real-time remote biometric identification (law enforcement)
    performs_realtime_remote_biometric_id: bool = Field(
        ...,
        description="Real-time remote biometric identification in publicly accessible spaces?"
    )
    used_by_law_enforcement: bool = Field(
        default=False,
        description="Used by law enforcement?"
    )
    has_judicial_authorization: bool = Field(
        default=False,
        description="Has prior judicial authorization?"
    )
    meets_strict_necessity_test: bool = Field(
        default=False,
        description="Meets strict necessity and proportionality test?"
    )


class HighRiskAssessment(BaseModel):
    """Section 3: High-Risk AI Systems (Annex III)"""
    
    # Annex III(1): Biometric identification and categorization
    biometric_identification_system: bool = Field(
        ...,
        description="Remote biometric identification of natural persons?"
    )
    biometric_categorization_system: bool = Field(
        ...,
        description="Biometric categorization according to sensitive attributes?"
    )
    
    # Annex III(2): Critical infrastructure
    manages_critical_infrastructure: bool = Field(
        ...,
        description="Manages or operates critical infrastructure?"
    )
    critical_infrastructure_type: Optional[str] = Field(
        None,
        description="Type: road traffic, water, gas, heating, electricity supply"
    )
    safety_component: bool = Field(
        default=False,
        description="Is it a safety component of critical infrastructure?"
    )
    
    # Annex III(3): Education and vocational training
    used_in_education: bool = Field(
        ...,
        description="Used in educational or vocational training context?"
    )
    determines_educational_access: bool = Field(
        default=False,
        description="Determines access to educational institutions?"
    )
    evaluates_learning_outcomes: bool = Field(
        default=False,
        description="Evaluates learning outcomes, including exams?"
    )
    assesses_appropriate_education_level: bool = Field(
        default=False,
        description="Assesses appropriate level of education?"
    )
    monitors_students: bool = Field(
        default=False,
        description="Monitors and detects prohibited behavior during tests?"
    )
    
    # Annex III(4): Employment, workers management, self-employment
    used_in_employment: bool = Field(
        ...,
        description="Used in employment, worker management, or self-employment?"
    )
    recruitment_or_selection: bool = Field(
        default=False,
        description="Recruitment or selection of persons?"
    )
    promotion_or_termination_decisions: bool = Field(
        default=False,
        description="Decisions on promotion or termination?"
    )
    task_allocation: bool = Field(
        default=False,
        description="Task allocation based on individual behavior/traits?"
    )
    performance_monitoring: bool = Field(
        default=False,
        description="Monitors and evaluates performance and behavior?"
    )
    
    # Annex III(5): Essential private/public services and benefits
    evaluates_access_to_services: bool = Field(
        ...,
        description="Evaluates eligibility for essential services/benefits?"
    )
    creditworthiness_assessment: bool = Field(
        default=False,
        description="Assesses creditworthiness (except fraud detection)?"
    )
    emergency_services_dispatch: bool = Field(
        default=False,
        description="Dispatches or prioritizes emergency services?"
    )
    evaluates_public_assistance: bool = Field(
        default=False,
        description="Evaluates eligibility for public assistance benefits?"
    )
    
    # Annex III(6): Law enforcement
    used_in_law_enforcement: bool = Field(
        ...,
        description="Used by law enforcement authorities?"
    )
    individual_risk_assessment: bool = Field(
        default=False,
        description="Assesses risk of person being victim or perpetrator?"
    )
    lie_detection: bool = Field(
        default=False,
        description="Detects emotional state or lie detection?"
    )
    evidence_reliability_assessment: bool = Field(
        default=False,
        description="Evaluates reliability of evidence?"
    )
    crime_prediction: bool = Field(
        default=False,
        description="Predicts occurrence or reoccurrence of crime?"
    )
    profiling_during_investigation: bool = Field(
        default=False,
        description="Profiling in course of detection/investigation?"
    )
    
    # Annex III(7): Migration, asylum, border control
    used_in_migration_asylum_border: bool = Field(
        ...,
        description="Used in migration, asylum, or border control?"
    )
    polygraph_or_lie_detection_migration: bool = Field(
        default=False,
        description="Lie detection for migration/asylum/border control?"
    )
    risk_assessment_migration: bool = Field(
        default=False,
        description="Assesses security/health/migration risk?"
    )
    examines_applications: bool = Field(
        default=False,
        description="Examines visa/asylum/residence permit applications?"
    )
    detects_identity_fraud: bool = Field(
        default=False,
        description="Detects identity document fraud?"
    )
    
    # Annex III(8): Administration of justice and democratic processes
    used_in_justice_system: bool = Field(
        ...,
        description="Used in administration of justice or democratic processes?"
    )
    assists_judicial_authority: bool = Field(
        default=False,
        description="Assists judicial authority in researching/interpreting facts and law?"
    )
    applies_law_to_facts: bool = Field(
        default=False,
        description="Applies law to concrete set of facts?"
    )


class GeneralPurposeAIAssessment(BaseModel):
    """Section 4: General Purpose AI (GPAI) / Foundation Models"""
    
    is_general_purpose_ai: bool = Field(
        ...,
        description="Is this a general-purpose AI model (foundation model)?"
    )
    
    can_perform_multiple_tasks: bool = Field(
        default=False,
        description="Can perform wide range of distinct tasks?"
    )
    
    training_compute: Optional[float] = Field(
        None,
        description="Training compute in FLOPs (if known)"
    )
    
    exceeds_systemic_risk_threshold: bool = Field(
        default=False,
        description="Training compute > 10^25 FLOPs (systemic risk threshold)?"
    )
    
    has_high_impact_capabilities: bool = Field(
        default=False,
        description="Has capabilities/impact equivalent to systemic risk models?"
    )
    
    model_size_parameters: Optional[float] = Field(
        None,
        description="Number of model parameters (billions)"
    )
    
    is_open_source: bool = Field(
        default=False,
        description="Is the model open-source?"
    )
    
    provides_api_access: bool = Field(
        default=False,
        description="Provides API access to third parties?"
    )
    
    downstream_applications: Optional[List[str]] = Field(
        None,
        description="Known downstream applications or use cases"
    )


class TechnicalCharacteristics(BaseModel):
    """Section 5: Technical Characteristics"""
    
    model_type: ModelTypeEnum = Field(..., description="Type of AI model")
    model_architecture: Optional[str] = Field(None, description="Model architecture details")
    
    autonomy_level: AutonomyLevelEnum = Field(..., description="Level of automation")
    
    has_human_oversight: bool = Field(..., description="Is there human oversight?")
    human_oversight_description: Optional[str] = Field(
        None,
        description="Describe human oversight mechanisms"
    )
    
    makes_autonomous_decisions: bool = Field(
        ...,
        description="Makes decisions without human intervention?"
    )
    
    decision_reversibility: bool = Field(
        ...,
        description="Can decisions be easily reversed or overridden?"
    )
    
    uses_personal_data: bool = Field(..., description="Processes personal data?")
    uses_sensitive_data: bool = Field(..., description="Processes sensitive/special category data?")
    data_sensitivity: Optional[DataSensitivityEnum] = Field(None, description="Data sensitivity level")
    
    training_data_size: Optional[str] = Field(None, description="Size of training dataset")
    training_data_sources: Optional[List[str]] = Field(None, description="Sources of training data")
    training_data_demographics: Optional[str] = Field(
        None,
        description="Demographics represented in training data"
    )
    
    has_bias_testing: bool = Field(..., description="Has undergone bias testing?")
    bias_testing_results: Optional[str] = Field(None, description="Summary of bias testing results")
    
    has_adversarial_testing: bool = Field(..., description="Has undergone adversarial testing?")
    adversarial_testing_results: Optional[str] = Field(
        None,
        description="Summary of adversarial testing results"
    )
    
    accuracy_metrics: Optional[Dict[str, float]] = Field(
        None,
        description="Model accuracy metrics (precision, recall, F1, etc.)"
    )
    
    explainability_level: Optional[str] = Field(
        None,
        description="Level of explainability (black-box, interpretable, fully explainable)"
    )
    
    has_technical_documentation: bool = Field(
        ...,
        description="Has comprehensive technical documentation?"
    )


class ImpactAssessment(BaseModel):
    """Section 6: Impact on Individuals and Society"""
    
    affects_individuals: bool = Field(..., description="Directly affects natural persons?")
    
    number_of_affected_persons: Optional[str] = Field(
        None,
        description="Estimated number of affected persons (range)"
    )
    
    affects_fundamental_rights: bool = Field(
        ...,
        description="Could impact fundamental rights?"
    )
    fundamental_rights_affected: Optional[List[str]] = Field(
        None,
        description="Which fundamental rights could be affected?"
    )
    
    decision_impact_level: str = Field(
        ...,
        description="Impact level: low, medium, high, critical"
    )
    
    impacts_financial_access: bool = Field(
        default=False,
        description="Impacts access to financial services?"
    )
    
    impacts_employment: bool = Field(
        default=False,
        description="Impacts employment opportunities?"
    )
    
    impacts_education: bool = Field(
        default=False,
        description="Impacts educational opportunities?"
    )
    
    impacts_healthcare: bool = Field(
        default=False,
        description="Impacts healthcare access or treatment?"
    )
    
    impacts_justice: bool = Field(
        default=False,
        description="Impacts justice or legal proceedings?"
    )
    
    impacts_safety: bool = Field(
        default=False,
        description="Impacts physical safety?"
    )
    
    could_cause_discrimination: bool = Field(
        ...,
        description="Could lead to discriminatory outcomes?"
    )
    discrimination_risk_description: Optional[str] = Field(
        None,
        description="Describe discrimination risks if applicable"
    )
    
    has_appeal_mechanism: bool = Field(
        ...,
        description="Is there an appeal or redress mechanism?"
    )
    appeal_mechanism_description: Optional[str] = Field(
        None,
        description="Describe appeal mechanism"
    )


class SafetyAndSecurity(BaseModel):
    """Section 7: Safety and Cybersecurity"""
    
    safety_critical_system: bool = Field(
        ...,
        description="Is this a safety-critical system?"
    )
    
    potential_physical_harm: bool = Field(
        ...,
        description="Could malfunction cause physical harm?"
    )
    
    has_safety_certification: bool = Field(
        ...,
        description="Has safety certification (if applicable)?"
    )
    safety_standards_compliance: Optional[List[str]] = Field(
        None,
        description="Safety standards complied with"
    )
    
    cybersecurity_measures: bool = Field(
        ...,
        description="Has cybersecurity measures in place?"
    )
    cybersecurity_standards: Optional[List[str]] = Field(
        None,
        description="Cybersecurity standards followed"
    )
    
    vulnerability_assessment: bool = Field(
        ...,
        description="Has undergone vulnerability assessment?"
    )
    
    has_incident_response_plan: bool = Field(
        ...,
        description="Has incident response plan?"
    )
    
    data_encryption: bool = Field(..., description="Uses data encryption?")
    access_controls: bool = Field(..., description="Has access controls in place?")
    
    audit_logging: bool = Field(..., description="Has audit logging?")
    log_retention_period: Optional[str] = Field(None, description="Log retention period")


class ComplianceAndGovernance(BaseModel):
    """Section 8: Compliance and Governance"""
    
    has_risk_management_system: bool = Field(
        ...,
        description="Has risk management system in place?"
    )
    
    has_quality_management_system: bool = Field(
        ...,
        description="Has quality management system?"
    )
    
    has_data_governance: bool = Field(
        ...,
        description="Has data governance framework?"
    )
    
    has_model_governance: bool = Field(
        ...,
        description="Has AI/ML model governance?"
    )
    
    has_ethics_review: bool = Field(
        ...,
        description="Has undergone ethics review?"
    )
    
    has_impact_assessment: bool = Field(
        ...,
        description="Has conducted impact assessment (DPIA, FRIA, etc.)?"
    )
    
    has_conformity_assessment: bool = Field(
        ...,
        description="Has undergone conformity assessment?"
    )
    conformity_assessment_body: Optional[str] = Field(
        None,
        description="Name of notified body (if applicable)"
    )
    
    has_ce_marking: bool = Field(
        default=False,
        description="Has CE marking (if applicable)?"
    )
    
    has_post_market_monitoring: bool = Field(
        ...,
        description="Has post-market monitoring plan?"
    )
    
    incident_reporting_process: bool = Field(
        ...,
        description="Has incident reporting process?"
    )
    
    has_transparency_obligations: bool = Field(
        ...,
        description="Meets transparency obligations?"
    )
    users_informed_of_ai: bool = Field(
        ...,
        description="Are users informed they're interacting with AI?"
    )


class AdditionalContext(BaseModel):
    """Section 9: Additional Context"""
    
    regulatory_approvals: Optional[List[str]] = Field(
        None,
        description="Other regulatory approvals obtained"
    )
    
    industry_certifications: Optional[List[str]] = Field(
        None,
        description="Industry certifications held"
    )
    
    previous_incidents: bool = Field(
        ...,
        description="Any previous incidents or issues?"
    )
    previous_incidents_description: Optional[str] = Field(
        None,
        description="Describe previous incidents"
    )
    
    third_party_audits: bool = Field(
        ...,
        description="Has undergone third-party audits?"
    )
    audit_reports_available: bool = Field(
        default=False,
        description="Are audit reports available?"
    )
    
    insurance_coverage: bool = Field(
        ...,
        description="Has liability insurance coverage?"
    )
    
    additional_notes: Optional[str] = Field(
        None,
        description="Any additional relevant information"
    )


# ============================================================================
# Complete Questionnaire
# ============================================================================

class AISystemQuestionnaire(BaseModel):
    """
    Complete EU AI Act Compliance Questionnaire
    
    This comprehensive questionnaire collects all necessary information
    to classify an AI system under the EU AI Act and determine compliance
    obligations.
    """
    
    # Metadata
    questionnaire_version: str = Field(default="1.0", description="Questionnaire version")
    submission_date: Optional[str] = Field(None, description="Submission date (ISO format)")
    submitted_by: Optional[str] = Field(None, description="Name of person submitting")
    organization: Optional[str] = Field(None, description="Organization name")
    
    # Questionnaire sections
    basic_information: BasicInformation
    prohibited_practices: ProhibitedPracticesAssessment
    high_risk_assessment: HighRiskAssessment
    gpai_assessment: GeneralPurposeAIAssessment
    technical_characteristics: TechnicalCharacteristics
    impact_assessment: ImpactAssessment
    safety_security: SafetyAndSecurity
    compliance_governance: ComplianceAndGovernance
    additional_context: AdditionalContext
    
    class Config:
        json_schema_extra = {
            "example": {
                "questionnaire_version": "1.0",
                "submission_date": "2026-05-11",
                "submitted_by": "John Doe",
                "organization": "Example Bank Ltd",
                "basic_information": {
                    "system_name": "Credit Scoring System",
                    "system_version": "2.1.0",
                    "system_description": "AI system for automated creditworthiness assessment",
                    "sector": "banking",
                    "purpose": "creditworthiness_assessment",
                    "deployer_type": "private_company",
                    "deployer_name": "Example Bank Ltd",
                    "is_third_party_system": False,
                    "geographic_scope": "single_eu_country",
                    "deployment_countries": ["DE"],
                    "is_already_deployed": True
                },
                "prohibited_practices": {
                    "uses_subliminal_techniques": False,
                    "manipulates_behavior": False,
                    "targets_vulnerable_groups": False,
                    "exploits_vulnerabilities": False,
                    "performs_social_scoring": False,
                    "social_scoring_by_public_authority": False,
                    "predicts_criminal_offense_risk": False,
                    "creates_facial_recognition_database": False,
                    "performs_emotion_recognition": False,
                    "performs_biometric_categorization": False,
                    "performs_realtime_remote_biometric_id": False
                },
                "high_risk_assessment": {
                    "biometric_identification_system": False,
                    "manages_critical_infrastructure": False,
                    "used_in_education": False,
                    "used_in_employment": False,
                    "evaluates_access_to_services": True,
                    "creditworthiness_assessment": True,
                    "used_in_law_enforcement": False,
                    "used_in_migration_asylum_border": False,
                    "used_in_justice_system": False
                },
                "gpai_assessment": {
                    "is_general_purpose_ai": False
                },
                "technical_characteristics": {
                    "model_type": "machine_learning",
                    "autonomy_level": "semi_automated",
                    "has_human_oversight": True,
                    "makes_autonomous_decisions": True,
                    "decision_reversibility": True,
                    "uses_personal_data": True,
                    "uses_sensitive_data": False,
                    "has_bias_testing": True,
                    "has_adversarial_testing": False,
                    "has_technical_documentation": True
                },
                "impact_assessment": {
                    "affects_individuals": True,
                    "affects_fundamental_rights": True,
                    "decision_impact_level": "high",
                    "impacts_financial_access": True,
                    "could_cause_discrimination": True,
                    "has_appeal_mechanism": True
                },
                "safety_security": {
                    "safety_critical_system": False,
                    "potential_physical_harm": False,
                    "has_safety_certification": False,
                    "cybersecurity_measures": True,
                    "vulnerability_assessment": True,
                    "has_incident_response_plan": True,
                    "data_encryption": True,
                    "access_controls": True,
                    "audit_logging": True
                },
                "compliance_governance": {
                    "has_risk_management_system": True,
                    "has_quality_management_system": True,
                    "has_data_governance": True,
                    "has_model_governance": True,
                    "has_ethics_review": True,
                    "has_impact_assessment": True,
                    "has_conformity_assessment": False,
                    "has_post_market_monitoring": True,
                    "incident_reporting_process": True,
                    "has_transparency_obligations": True,
                    "users_informed_of_ai": True
                },
                "additional_context": {
                    "previous_incidents": False,
                    "third_party_audits": True,
                    "insurance_coverage": True
                }
            }
        }


# ============================================================================
# Validation Functions
# ============================================================================

def validate_questionnaire_completeness(questionnaire: AISystemQuestionnaire) -> Dict[str, Any]:
    """
    Validate questionnaire completeness and identify missing critical information
    
    Returns:
        Dictionary with validation results and missing fields
    """
    missing_fields = []
    warnings = []
    
    # Check for critical missing information based on responses
    if questionnaire.high_risk_assessment.creditworthiness_assessment:
        if not questionnaire.technical_characteristics.has_bias_testing:
            warnings.append("Bias testing recommended for creditworthiness assessment")
    
    if questionnaire.impact_assessment.affects_fundamental_rights:
        if not questionnaire.compliance_governance.has_impact_assessment:
            missing_fields.append("Fundamental Rights Impact Assessment required")
    
    if questionnaire.technical_characteristics.uses_sensitive_data:
        if not questionnaire.compliance_governance.has_data_governance:
            missing_fields.append("Data governance framework required for sensitive data")
    
    return {
        "is_complete": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "warnings": warnings,
        "completeness_score": 1.0 - (len(missing_fields) * 0.1)
    }

# Made with Bob
