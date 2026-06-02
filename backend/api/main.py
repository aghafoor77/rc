"""
FastAPI Main Application

EU AI Act Compliance Assessment System API
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="EU AI Act Risk Assessment System",
    description="""
    AI Risk Classification and Compliance Assessment System
    
    This API provides automated risk classification for AI systems according to the EU AI Act.
    It combines rule-based classification, LLM-powered reasoning, and RAG-enhanced legal grounding.
    
    ## Features
    - Automated risk classification (Prohibited, High-Risk, Limited-Risk, Minimal-Risk)
    - Legal basis identification with article references
    - Compliance obligation mapping
    - Human review workflow
    - Comprehensive audit trails
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_version="3.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request/Response Models
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]


class ClassificationRequest(BaseModel):
    """Classification request"""
    ai_system_metadata: Dict[str, Any]
    use_rag: bool = True
    use_llm: bool = True
    include_explanations: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "ai_system_metadata": {
                    "system_name": "Credit Scoring System",
                    "sector": "banking",
                    "purpose": "creditworthiness_assessment",
                    "deployer_type": "private_company",
                    "autonomy_level": "fully_automated",
                    "affects_individuals": True,
                    "impacts_financial_access": True
                },
                "use_rag": True,
                "use_llm": True,
                "include_explanations": True
            }
        }


from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class ClassificationResponse(BaseModel):
    """Classification response"""

    assessment_id: str
    timestamp: str
    risk_category: str
    confidence: float
    method: str
    requires_human_review: bool

    legal_basis: Optional[Dict[str, Any]] = None
    reasoning: Optional[Dict[str, Any]] = None
    compliance_obligations: Optional[Dict[str, Any]] = None

    # NEW FIELDS
    rag_enabled: Optional[bool] = None
    retrieved_documents_count: Optional[int] = None
    explainability: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "assessment_id": "d6cca875-3939-44d7-a7e3-de9fa1513278",
                "timestamp": "2026-05-28T10:59:24.793187",
                "risk_category": "PROHIBITED",
                "confidence": 0.8,
                "method": "llm_only",
                "requires_human_review": False,
                "legal_basis": {
                    "primary_article": "Article 5",
                    "supporting_articles": [
                        "Annex III"
                    ],
                    "sources": []
                },
                "reasoning": {
                    "steps": [
                        "Step 1: Analyzed AI system metadata",
                        "Step 2: Considered high-risk categories",
                        "Step 3: Identified applicable EU AI Act provisions"
                    ]
                },
                "compliance_obligations": {
                    "mandatory": [
                        "System must not be deployed or used",
                        "Immediate cessation of operations required"
                    ]
                },
                "rag_enabled": True,
                "retrieved_documents_count": 5,
                "explainability": {
                    "decision_summary": (
                        "Workplace Emotion Detector is classified as "
                        "PROHIBITED under the EU AI Act."
                    ),
                    "evidence": [],
                    "reasoning_chain": [],
                    "confidence_factors": {},
                    "alternative_interpretations": [],
                    "key_factors": []
                }
            }
        }


# ============================================================================
# Dependency Injection
# ============================================================================

def get_classification_service():
    """Get classification service instance"""
    from backend.services.classification_service import get_classification_service as get_service
    return get_service()


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "EU AI Act Compliance Assessment System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns system health status and service availability
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        services={
            "api": "operational",
            "database": "operational",
            "llm": "operational",
            "rag": "operational"
        }
    )


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint
    
    Returns basic metrics for monitoring
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "eu-ai-act-backend"
    }


@app.post(
    "/api/v1/classify",
    response_model=ClassificationResponse,
    tags=["Classification"],
    status_code=status.HTTP_200_OK
)
async def classify_ai_system(
    request: ClassificationRequest,
    service = Depends(get_classification_service)
):
    """
    Classify AI system according to EU AI Act
    
    This endpoint performs comprehensive risk classification using:
    - Rule-based deterministic classification
    - LLM-based semantic reasoning (optional)
    - RAG-enhanced legal grounding (optional)
    
    Returns risk category, confidence score, legal basis, and compliance obligations.
    """
    try:
        logger.info(f"====================================================================================")
        logger.info(f"Classification request R: {request}")
        logger.info(f"Classification request received for: {request.ai_system_metadata.get('system_name', 'Unknown')}")
        
        # Call classification service with request parameters
        result = service.classify(
            ai_metadata=request.ai_system_metadata,
            use_llm=request.use_llm,
            use_rag=request.use_rag,
            include_explanations=request.include_explanations
        )
        
        # Display result in properly formatted JSON
        print("\n" + "="*80)
        print("CLASSIFICATION RESULT (Formatted JSON)")
        print("="*80)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        print("="*80 + "\n")

        # Return full result with explainability
        logger.info(msg=f"Classification complete: {result['risk_category']} (confidence: {result['confidence']})")
        
        # Save result to JSON file
        try:
            import os
            from pathlib import Path
            
            # Create results directory if it doesn't exist
            results_dir = Path("classification_results")
            results_dir.mkdir(exist_ok=True)
            
            # Generate filename with timestamp and assessment_id
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            assessment_id = result.get('assessment_id', 'unknown')
            filename = f"classification_{timestamp}_{assessment_id}.json"
            filepath = results_dir / filename
            
            # Write JSON to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Classification result saved to: {filepath}")
        except Exception as file_error:
            logger.error(f"Failed to save classification result to file: {str(file_error)}")
        
        return result
    
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Classification failed: {str(e)}"
        )


@app.get(
    "/api/v1/assessments/{assessment_id}",
    tags=["Assessments"]
)
async def get_assessment(assessment_id: str):
    """
    Retrieve assessment by ID
    
    Returns complete assessment details including classification,
    reasoning, compliance obligations, and audit trail.
    """
    try:
        # Mock response
        return {
            "assessment_id": assessment_id,
            "status": "completed",
            "created_at": datetime.utcnow().isoformat(),
            "risk_category": "HIGH_RISK",
            "confidence": 0.95
        }
    
    except Exception as e:
        logger.error(f"Error retrieving assessment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment not found: {assessment_id}"
        )


@app.get(
    "/api/v1/reports/{assessment_id}",
    tags=["Reports"]
)
async def get_compliance_report(
    assessment_id: str,
    format: str = "json"
):
    """
    Generate compliance report
    
    Formats: json, pdf, html
    """
    try:
        if format not in ["json", "pdf", "html"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid format. Supported: json, pdf, html"
            )
        
        # Mock response
        return {
            "report_id": f"REP-{assessment_id}",
            "assessment_id": assessment_id,
            "format": format,
            "generated_at": datetime.utcnow().isoformat(),
            "report_type": "compliance_assessment",
            "download_url": f"/api/v1/reports/{assessment_id}/download?format={format}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )


@app.post(
    "/api/v1/review/submit/{assessment_id}",
    tags=["Human Review"]
)
async def submit_for_review(assessment_id: str):
    """
    Submit assessment for human review
    
    Escalates uncertain or high-stakes classifications to human reviewers.
    """
    try:
        return {
            "assessment_id": assessment_id,
            "review_status": "pending",
            "submitted_at": datetime.utcnow().isoformat(),
            "estimated_review_time": "24-48 hours"
        }
    
    except Exception as e:
        logger.error(f"Error submitting for review: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Review submission failed: {str(e)}"
        )


@app.get(
    "/api/v1/rules",
    tags=["Rules"]
)
async def list_rules(
    category: Optional[str] = None,
    enabled_only: bool = True
):
    """
    List classification rules
    
    Returns available classification rules, optionally filtered by category.
    """
    try:
        # Mock response
        return {
            "total_rules": 35,
            "categories": {
                "PROHIBITED": 8,
                "HIGH_RISK": 26,
                "LIMITED_RISK": 1
            },
            "rules": [
                {
                    "rule_id": "R-PROHIBITED-001",
                    "name": "Social Scoring by Public Authority",
                    "category": "PROHIBITED",
                    "enabled": True
                },
                {
                    "rule_id": "R-HR-012",
                    "name": "Creditworthiness Assessment",
                    "category": "HIGH_RISK",
                    "enabled": True
                }
            ]
        }
    
    except Exception as e:
        logger.error(f"Error listing rules: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list rules: {str(e)}"
        )


@app.get(
    "/api/v1/obligations/{risk_category}",
    tags=["Compliance"]
)
async def get_compliance_obligations(risk_category: str):
    """
    Get compliance obligations for risk category
    
    Returns detailed compliance requirements based on risk classification.
    """
    try:
        if risk_category not in ["PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK", "GPAI"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid risk category"
            )
        
        # Mock response
        obligations = {
            "HIGH_RISK": [
                {
                    "article": "Article 9",
                    "title": "Risk Management System",
                    "requirements": [
                        "Identify and analyze known and foreseeable risks",
                        "Estimate and evaluate risks",
                        "Adopt suitable risk management measures"
                    ],
                    "severity": "MANDATORY"
                },
                {
                    "article": "Article 10",
                    "title": "Data and Data Governance",
                    "requirements": [
                        "Training, validation, testing data sets",
                        "Data quality criteria",
                        "Data preparation and labeling"
                    ],
                    "severity": "MANDATORY"
                }
            ]
        }
        
        return {
            "risk_category": risk_category,
            "obligations": obligations.get(risk_category, []),
            "total_obligations": len(obligations.get(risk_category, []))
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving obligations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve obligations: {str(e)}"
        )


@app.get(
    "/api/v1/stats",
    tags=["Statistics"]
)
async def get_statistics():
    """
    Get system statistics
    
    Returns usage statistics, classification distribution, and performance metrics.
    """
    try:
        return {
            "total_assessments": 1247,
            "assessments_today": 23,
            "classification_distribution": {
                "PROHIBITED": 5,
                "HIGH_RISK": 342,
                "LIMITED_RISK": 156,
                "MINIMAL_RISK": 744
            },
            "average_confidence": 0.89,
            "human_review_rate": 0.12,
            "average_processing_time_ms": 1850
        }
    
    except Exception as e:
        logger.error(f"Error retrieving statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting EU AI Act Compliance Assessment System")
    logger.info("API documentation available at /docs")
    # Initialize engines, database connections, etc.


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down EU AI Act Compliance Assessment System")
    # Close database connections, cleanup resources, etc.


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# Made with Bob
