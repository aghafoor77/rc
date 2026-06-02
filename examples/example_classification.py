"""
Example: EU AI Act Classification

This example demonstrates how to use the EU AI Act Compliance Assessment System
to classify an AI application and retrieve compliance obligations.
"""

import json
import requests
from typing import Dict, Any


# ============================================================================
# Configuration
# ============================================================================

API_BASE_URL = "http://localhost:8000"


# ============================================================================
# Example AI Systems
# ============================================================================

def example_credit_scoring_system() -> Dict[str, Any]:
    """Example: High-Risk Credit Scoring System"""
    return {
        "system_name": "SmartCredit AI",
        "system_version": "2.1.0",
        "system_description": "AI-powered credit scoring and loan approval system",
        
        # Basic Information
        "sector": "banking",
        "purpose": "creditworthiness_assessment",
        "deployer_type": "private_company",
        "deployer_name": "Example Bank Ltd",
        "geographic_scope": "single_eu_country",
        "deployment_countries": ["DE"],
        "is_already_deployed": True,
        
        # Prohibited Practices Check
        "uses_subliminal_techniques": False,
        "manipulates_behavior": False,
        "targets_vulnerable_groups": False,
        "performs_social_scoring": False,
        "performs_emotion_recognition": False,
        "performs_biometric_categorization": False,
        "performs_realtime_remote_biometric_id": False,
        
        # High-Risk Assessment
        "evaluates_access_to_services": True,
        "creditworthiness_assessment": True,
        "used_in_law_enforcement": False,
        "used_in_education": False,
        "used_in_employment": False,
        
        # Technical Characteristics
        "model_type": "machine_learning",
        "autonomy_level": "semi_automated",
        "has_human_oversight": True,
        "makes_autonomous_decisions": True,
        "decision_reversibility": True,
        "uses_personal_data": True,
        "uses_sensitive_data": False,
        "has_bias_testing": True,
        "has_technical_documentation": True,
        
        # Impact Assessment
        "affects_individuals": True,
        "affects_fundamental_rights": True,
        "decision_impact_level": "high",
        "impacts_financial_access": True,
        "could_cause_discrimination": True,
        "has_appeal_mechanism": True,
        
        # Safety & Security
        "safety_critical_system": False,
        "cybersecurity_measures": True,
        "vulnerability_assessment": True,
        "has_incident_response_plan": True,
        "data_encryption": True,
        "access_controls": True,
        "audit_logging": True,
        
        # Compliance & Governance
        "has_risk_management_system": True,
        "has_quality_management_system": True,
        "has_data_governance": True,
        "has_model_governance": True,
        "has_ethics_review": True,
        "has_impact_assessment": True,
        "has_post_market_monitoring": True,
        "incident_reporting_process": True,
        "has_transparency_obligations": True,
        "users_informed_of_ai": True
    }


def example_chatbot_system() -> Dict[str, Any]:
    """Example: Limited-Risk Chatbot System"""
    return {
        "system_name": "CustomerSupport AI",
        "system_version": "1.5.0",
        "system_description": "AI chatbot for customer support",
        
        "sector": "ecommerce",
        "purpose": "customer_support",
        "deployer_type": "private_company",
        "autonomy_level": "advisory_only",
        
        "performs_emotion_recognition": False,
        "generates_synthetic_content": True,
        "interacts_with_humans": True,
        
        "affects_individuals": True,
        "decision_impact_level": "low",
        "users_informed_of_ai": True,
        
        "has_technical_documentation": True,
        "cybersecurity_measures": True
    }


def example_prohibited_system() -> Dict[str, Any]:
    """Example: Prohibited Social Scoring System"""
    return {
        "system_name": "CitizenScore",
        "system_version": "1.0.0",
        "system_description": "Social scoring system for public services",
        
        "sector": "government_services",
        "purpose": "social_scoring",
        "deployer_type": "public_authority",
        
        "performs_social_scoring": True,
        "social_scoring_by_public_authority": True,
        "evaluates_general_population": True,
        "leads_to_detrimental_treatment": True,
        
        "affects_individuals": True,
        "affects_fundamental_rights": True,
        "decision_impact_level": "critical"
    }


# ============================================================================
# API Functions
# ============================================================================

def classify_ai_system(ai_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify AI system using the API
    
    Args:
        ai_metadata: AI system metadata
        
    Returns:
        Classification result
    """
    url = f"{API_BASE_URL}/api/v1/classify"
    
    payload = {
        "ai_system_metadata": ai_metadata,
        "use_rag": True,
        "use_llm": True
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return response.json()


def get_compliance_obligations(risk_category: str) -> Dict[str, Any]:
    """
    Get compliance obligations for risk category
    
    Args:
        risk_category: Risk category
        
    Returns:
        Compliance obligations
    """
    url = f"{API_BASE_URL}/api/v1/obligations/{risk_category}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()


def generate_report(assessment_id: str, format: str = "json") -> Dict[str, Any]:
    """
    Generate compliance report
    
    Args:
        assessment_id: Assessment ID
        format: Report format (json, pdf, html)
        
    Returns:
        Report information
    """
    url = f"{API_BASE_URL}/api/v1/reports/{assessment_id}"
    params = {"format": format}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()


# ============================================================================
# Example Usage
# ============================================================================

def main():
    """Main example function"""
    
    print("=" * 80)
    print("EU AI Act Compliance Assessment System - Examples")
    print("=" * 80)
    print()
    
    # Example 1: High-Risk Credit Scoring System
    print("Example 1: Credit Scoring System (Expected: HIGH_RISK)")
    print("-" * 80)
    
    credit_system = example_credit_scoring_system()
    print(f"System: {credit_system['system_name']}")
    print(f"Sector: {credit_system['sector']}")
    print(f"Purpose: {credit_system['purpose']}")
    print()
    
    try:
        result = classify_ai_system(credit_system)
        
        print(f"✓ Classification: {result['risk_category']}")
        print(f"✓ Confidence: {result['confidence']:.2%}")
        print(f"✓ Method: {result['method']}")
        print(f"✓ Requires Human Review: {result['requires_human_review']}")
        
        if result.get('legal_basis'):
            print(f"✓ Legal Basis: {result['legal_basis']['primary_article']}")
        
        print()
        
        # Get compliance obligations
        if result['risk_category'] != "UNCLASSIFIED":
            obligations = get_compliance_obligations(result['risk_category'])
            print(f"Compliance Obligations: {obligations['total_obligations']}")
            
            if obligations.get('obligations'):
                print("\nKey Obligations:")
                for i, obl in enumerate(obligations['obligations'][:3], 1):
                    print(f"  {i}. {obl['title']} ({obl['article']})")
        
        print()
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")
        print("  Make sure the API server is running at http://localhost:8000")
    
    print()
    
    # Example 2: Limited-Risk Chatbot
    print("Example 2: Customer Support Chatbot (Expected: LIMITED_RISK)")
    print("-" * 80)
    
    chatbot_system = example_chatbot_system()
    print(f"System: {chatbot_system['system_name']}")
    print(f"Sector: {chatbot_system['sector']}")
    print(f"Purpose: {chatbot_system['purpose']}")
    print()
    
    try:
        result = classify_ai_system(chatbot_system)
        
        print(f"✓ Classification: {result['risk_category']}")
        print(f"✓ Confidence: {result['confidence']:.2%}")
        print(f"✓ Method: {result['method']}")
        
        print()
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")
    
    print()
    
    # Example 3: Prohibited Social Scoring
    print("Example 3: Social Scoring System (Expected: PROHIBITED)")
    print("-" * 80)
    
    prohibited_system = example_prohibited_system()
    print(f"System: {prohibited_system['system_name']}")
    print(f"Sector: {prohibited_system['sector']}")
    print(f"Purpose: {prohibited_system['purpose']}")
    print()
    
    try:
        result = classify_ai_system(prohibited_system)
        
        print(f"✓ Classification: {result['risk_category']}")
        print(f"✓ Confidence: {result['confidence']:.2%}")
        
        if result['risk_category'] == "PROHIBITED":
            print("⚠️  WARNING: This AI system is PROHIBITED under EU AI Act Article 5")
            print("   It must not be placed on the market or put into service.")
        
        print()
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")
    
    print()
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

# Made with Bob
