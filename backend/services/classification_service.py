"""
Classification Service
Integrates rule-based and LLM engines for AI system classification
Enhanced with EUAIAct_Assistant ChromaDB integration and explainability features
"""

import logging
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from backend.engines.rule_engine import RuleEngine, create_default_rules
from backend.engines.llm_engine import LLMEngine, HybridClassificationEngine
from backend.rag.rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)


class ClassificationService:
    """Service for AI system classification with RAG support"""
    
    def __init__(self):
        """Initialize classification service"""
        self.rule_engine = None
        self.llm_engine = None
        self.hybrid_engine = None
        self.rag_pipeline = None
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize classification engines and RAG pipeline"""
        # Initialize rule engine (critical - must succeed)
        try:
            # Create default rules if not exists
            rules_path = Path("/app/config/classification_rules.json")
            if not rules_path.exists():
                rules_path.parent.mkdir(parents=True, exist_ok=True)
                rules_data = {
                    "version": "1.0",
                    "rules": create_default_rules()
                }
                with open(rules_path, 'w') as f:
                    json.dump(rules_data, f, indent=2)
                logger.info(f"Created default rules at {rules_path}")
            
            # Initialize rule engine
            self.rule_engine = RuleEngine(rules_path)
            logger.info("Rule engine initialized successfully")
            
        except Exception as e:
            logger.error(f"CRITICAL: Failed to initialize rule engine: {e}")
            logger.error("System will use basic fallback classification")
            self.rule_engine = None
        
        # Initialize LLM engine (optional - can fail gracefully)
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        llm_model = os.getenv("LLM_MODEL", "llama3:8b")
        
        try:
            self.llm_engine = LLMEngine(
                model_name=llm_model,
                temperature=0.1,
                ollama_host=ollama_url
            )
            logger.info(f"LLM engine initialized with model '{llm_model}' at {ollama_url}")
        except Exception as e:
            logger.warning(f"LLM engine initialization failed: {e}")
            logger.info("LLM engine will not be available - using rule-based classification only")
            self.llm_engine = None
        
        # Initialize RAG pipeline (optional - can fail gracefully)
        try:
            embedding_backend = os.getenv("EMBEDDING_BACKEND", "sentence-transformers")
            embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
            
            # If using Ollama embeddings, use nomic-embed-text
            if embedding_backend == "ollama":
                embedding_model = "nomic-embed-text"
            
            self.rag_pipeline = RAGPipeline(
                embedding_backend=embedding_backend,
                embedding_model=embedding_model,
                ollama_host=ollama_url,
                use_euaiact_data=True  # Use EUAIAct_Assistant ChromaDB
            )
            logger.info(f"RAG pipeline initialized with {embedding_backend} embeddings")
            
            # Log collection stats
            stats = self.rag_pipeline.get_collection_stats()
            logger.info(f"RAG collection: {stats['document_count']} documents")
        except Exception as e:
            logger.warning(f"RAG pipeline initialization failed: {e}")
            logger.info("RAG pipeline will not be available")
            self.rag_pipeline = None
        
        # Initialize hybrid engine only if LLM engine is available
        if self.llm_engine and self.rule_engine:
            try:
                # Get confidence threshold from environment (default 0.85)
                # Lower threshold = more LLM usage, Higher = more rule-based
                confidence_threshold = float(os.getenv("HYBRID_CONFIDENCE_THRESHOLD", "0.85"))
                
                self.hybrid_engine = HybridClassificationEngine(
                    rule_engine=self.rule_engine,
                    llm_engine=self.llm_engine,
                    confidence_threshold=confidence_threshold
                )
                logger.info(f"Hybrid classification engine initialized (threshold: {confidence_threshold})")
            except Exception as e:
                logger.error(f"Failed to initialize hybrid engine: {e}")
                self.hybrid_engine = None
        else:
            self.hybrid_engine = None
            if not self.llm_engine:
                logger.info("Hybrid engine not initialized - LLM engine unavailable")
            if not self.rule_engine:
                logger.warning("Hybrid engine not initialized - Rule engine unavailable")
    
    def classify(
        self,
        ai_metadata: Dict[str, Any],
        use_llm: bool = True,
        use_rag: bool = True,
        include_explanations: bool = True
    ) -> Dict[str, Any]:
        """
        Classify AI system with enhanced explainability
        
        Args:
            ai_metadata: AI system metadata
            use_llm: Whether to use LLM engine
            use_rag: Whether to use RAG context (default: True)
            include_explanations: Include detailed explanations and evidence
            
        Returns:
            Classification result with explainability features
        """
        assessment_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        try:
            # Retrieve RAG context if enabled and available
            rag_context = None
            retrieved_docs = []
            
            if use_rag and self.rag_pipeline:
                try:
                    rag_context, retrieved_docs = self.rag_pipeline.retrieve_for_classification(ai_metadata)
                    logger.info(f"Retrieved {len(retrieved_docs)} documents from RAG")
                except Exception as e:
                    logger.warning(f"RAG retrieval failed: {e}")
            
            if self.hybrid_engine and use_llm:
                # Use hybrid classification with RAG context
                result = self.hybrid_engine.classify(ai_metadata, rag_context=rag_context)
                
                # Extract compliance obligations
                compliance_obligations = self._get_compliance_obligations(result['risk_category'])
                
                # Build response with enhanced explainability
                response = {
                    "assessment_id": assessment_id,
                    "timestamp": timestamp,
                    "risk_category": result['risk_category'],
                    "confidence": result['confidence'],
                    "method": result['method'],
                    "requires_human_review": result['requires_human_review'],
                    "legal_basis": self._extract_legal_basis(result, retrieved_docs),
                    "reasoning": self._extract_reasoning(result),
                    "compliance_obligations": compliance_obligations,
                    "rag_enabled": use_rag and self.rag_pipeline is not None,
                    "retrieved_documents_count": len(retrieved_docs) if retrieved_docs else 0
                }
                
                # Add enhanced explainability features
                if include_explanations:
                    response["explainability"] = self._build_explainability(
                        result,
                        retrieved_docs,
                        ai_metadata
                    )
                
                return response
            
            elif self.rule_engine:
                # Use rule-based only
                category, confidence, matches = self.rule_engine.classify(ai_metadata)
                
                best_match = self.rule_engine.get_best_match(matches)
                
                # Build result dict for _extract_legal_basis
                rule_result = {
                    'rule_based': {
                        'matched_rules': [{'legal_basis': best_match.legal_basis}] if best_match else []
                    }
                }
                
                legal_basis = self._extract_legal_basis(rule_result, retrieved_docs)
                
                reasoning = {
                    "steps": [best_match.explanation] if best_match else ["No matching rules found"]
                }
                
                compliance_obligations = self._get_compliance_obligations(category.value if category else "UNCLASSIFIED")
                
                response = {
                    "assessment_id": assessment_id,
                    "timestamp": timestamp,
                    "risk_category": category.value if category else "UNCLASSIFIED",
                    "confidence": confidence,
                    "method": "rule_based",
                    "requires_human_review": confidence < 0.75,
                    "legal_basis": legal_basis,
                    "reasoning": reasoning,
                    "compliance_obligations": compliance_obligations,
                    "rag_enabled": use_rag and self.rag_pipeline is not None,
                    "retrieved_documents_count": len(retrieved_docs) if retrieved_docs else 0
                }
                
                # Add explainability if requested
                if include_explanations:
                    response["explainability"] = {
                        "decision_summary": self._generate_decision_summary(
                            {"risk_category": category.value if category else "UNCLASSIFIED", "confidence": confidence},
                            ai_metadata
                        ),
                        "evidence": [],
                        "reasoning_chain": [
                            {
                                "step": i + 1,
                                "description": step,
                                "source": "Rule-Based Engine"
                            }
                            for i, step in enumerate(reasoning["steps"])
                        ],
                        "confidence_factors": {
                            "overall_confidence": confidence,
                            "contributing_factors": [
                                {
                                    "factor": "Rule-based match",
                                    "impact": "positive",
                                    "strength": confidence,
                                    "description": f"Deterministic rules matched with {confidence:.0%} confidence"
                                }
                            ],
                            "uncertainty_sources": [] if confidence >= 0.75 else [
                                {
                                    "source": "Low confidence",
                                    "description": f"Confidence below threshold ({confidence:.0%} < 75%)"
                                }
                            ]
                        },
                        "alternative_interpretations": [],
                        "key_factors": self._extract_key_factors(ai_metadata, {
                            "risk_category": category.value if category else "UNCLASSIFIED",
                            "confidence": confidence
                        })
                    }
                
                return response
            
            else:
                # Fallback classification
                return self._fallback_classification(ai_metadata, assessment_id, timestamp)
        
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return self._fallback_classification(ai_metadata, assessment_id, timestamp)
    
    def _extract_legal_basis(
        self,
        result: Dict[str, Any],
        retrieved_docs: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Extract legal basis from classification result with VectorDB sources
        
        Args:
            result: Classification result
            retrieved_docs: Retrieved documents from VectorDB
            
        Returns:
            Legal basis with primary article, supporting articles, and sources
        """
        legal_basis = {
            "primary_article": "Unknown",
            "supporting_articles": [],
            "sources": []
        }
        
        # Priority 1: Extract from LLM-based legal articles
        if 'llm_based' in result and result['llm_based'].get('legal_articles'):
            articles = result['llm_based']['legal_articles']
            if articles:
                legal_basis['primary_article'] = articles[0]
                legal_basis['supporting_articles'] = articles[1:]
        
        # Priority 2: Extract from rule-based matched rules
        elif 'rule_based' in result and result['rule_based'].get('matched_rules'):
            matched_rules = result['rule_based']['matched_rules']
            if matched_rules:
                # Extract from first matched rule
                legal_basis['primary_article'] = "Article 6(2), Annex III"
        
        # Priority 3: Extract from VectorDB retrieved documents
        elif retrieved_docs and len(retrieved_docs) > 0:
            # Use the most relevant document (first one) as primary article
            primary_doc = retrieved_docs[0]
            metadata = primary_doc.get('metadata', {})
            article_number = metadata.get('article_number', 'Unknown')
            
            if article_number != 'Unknown':
                legal_basis['primary_article'] = article_number
                
                # Add section information if available
                section = metadata.get('section', '')
                if section:
                    legal_basis['primary_article'] += f" - {section}"
                
                # Add source information for primary article
                legal_basis['sources'].append({
                    "article": article_number,
                    "section": section,
                    "relevance_score": 1.0 - primary_doc.get('distance', 0.5),
                    "excerpt": primary_doc['text'][:300] + "..." if len(primary_doc['text']) > 300 else primary_doc['text'],
                    "source_type": "VectorDB",
                    "document_id": primary_doc.get('id', 'unknown')
                })
                
                # Add supporting articles from remaining documents
                for doc in retrieved_docs[1:5]:  # Top 5 documents
                    doc_metadata = doc.get('metadata', {})
                    doc_article = doc_metadata.get('article_number', 'Unknown')
                    
                    if doc_article != 'Unknown' and doc_article != article_number:
                        if doc_article not in legal_basis['supporting_articles']:
                            legal_basis['supporting_articles'].append(doc_article)
                        
                        # Add source information
                        legal_basis['sources'].append({
                            "article": doc_article,
                            "section": doc_metadata.get('section', ''),
                            "relevance_score": 1.0 - doc.get('distance', 0.5),
                            "excerpt": doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text'],
                            "source_type": "VectorDB",
                            "document_id": doc.get('id', 'unknown')
                        })
        
        # If still unknown, provide a helpful message
        if legal_basis['primary_article'] == "Unknown":
            legal_basis['note'] = "Unable to determine primary article. Please provide more specific information about the AI system."
        
        return legal_basis
    
    def _extract_reasoning(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract reasoning from classification result"""
        reasoning = {"steps": []}
        
        if 'llm_based' in result and result['llm_based'].get('reasoning_steps'):
            reasoning['steps'] = result['llm_based']['reasoning_steps']
        
        elif 'rule_based' in result and result['rule_based'].get('matched_rules'):
            reasoning['steps'] = [
                rule['explanation']
                for rule in result['rule_based']['matched_rules']
            ]
        
        if not reasoning['steps']:
            reasoning['steps'] = [f"Classified as {result['risk_category']} based on system characteristics"]
        
        return reasoning
    
    def _get_compliance_obligations(self, risk_category: str) -> Dict[str, Any]:
        """Get compliance obligations for risk category"""
        obligations = {
            "HIGH_RISK": [
                "Risk management system (Article 9)",
                "Data governance (Article 10)",
                "Technical documentation (Article 11)",
                "Record-keeping (Article 12)",
                "Transparency (Article 13)",
                "Human oversight (Article 14)",
                "Accuracy, robustness, cybersecurity (Article 15)"
            ],
            "PROHIBITED": [
                "System must not be deployed or used",
                "Immediate cessation of operations required"
            ],
            "LIMITED_RISK": [
                "Transparency obligations (Article 52)",
                "Inform users about AI interaction"
            ],
            "MINIMAL_RISK": [
                "No specific obligations",
                "Voluntary codes of conduct encouraged"
            ]
        }
        
        return {
            "mandatory": obligations.get(risk_category, [])
        }
    
    def _build_explainability(
        self,
        result: Dict[str, Any],
        retrieved_docs: List[Dict[str, Any]],
        ai_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build comprehensive explainability information
        
        Args:
            result: Classification result
            retrieved_docs: Retrieved legal documents
            ai_metadata: AI system metadata
            
        Returns:
            Explainability dictionary with evidence and reasoning
        """
        explainability = {
            "decision_summary": self._generate_decision_summary(result, ai_metadata),
            "evidence": self._format_evidence(retrieved_docs),
            "reasoning_chain": self._extract_reasoning_chain(result),
            "confidence_factors": self._analyze_confidence_factors(result),
            "alternative_interpretations": self._identify_alternatives(result),
            "key_factors": self._extract_key_factors(ai_metadata, result)
        }
        
        return explainability
    
    def _generate_decision_summary(
        self,
        result: Dict[str, Any],
        ai_metadata: Dict[str, Any]
    ) -> str:
        """Generate human-readable decision summary"""
        system_name = ai_metadata.get('system_name', 'The AI system')
        risk_category = result['risk_category']
        confidence = result['confidence']
        
        summaries = {
            "PROHIBITED": f"{system_name} is classified as PROHIBITED under the EU AI Act. This system cannot be deployed or used as it violates fundamental rights.",
            "HIGH_RISK": f"{system_name} is classified as HIGH-RISK under the EU AI Act. This system requires strict compliance with regulatory requirements before deployment.",
            "LIMITED_RISK": f"{system_name} is classified as LIMITED-RISK under the EU AI Act. This system must comply with transparency obligations.",
            "MINIMAL_RISK": f"{system_name} is classified as MINIMAL-RISK under the EU AI Act. This system has no specific regulatory obligations but voluntary codes of conduct are encouraged."
        }
        
        summary = summaries.get(risk_category, f"{system_name} has been classified as {risk_category}.")
        summary += f" (Confidence: {confidence:.0%})"
        
        return summary
    
    def _format_evidence(
        self,
        retrieved_docs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Format retrieved documents as evidence with source information
        
        Args:
            retrieved_docs: Retrieved documents from VectorDB
            
        Returns:
            List of evidence items with sources
        """
        evidence = []
        
        for i, doc in enumerate(retrieved_docs[:5], 1):  # Top 5 documents
            metadata = doc.get('metadata', {})
            
            evidence_item = {
                "rank": i,
                "article": metadata.get('article_number', 'Unknown'),
                "section": metadata.get('section', ''),
                "type": metadata.get('type', 'article'),
                "category": metadata.get('category', ''),
                "importance": metadata.get('importance', ''),
                "relevance_score": 1.0 - doc.get('distance', 0.5),  # Convert distance to relevance
                "excerpt": doc['text'][:300] + "..." if len(doc['text']) > 300 else doc['text'],
                "full_text": doc['text'],
                "source": {
                    "type": "VectorDB",
                    "document_id": doc.get('id', 'unknown'),
                    "collection": "eu_ai_act",
                    "retrieval_method": "semantic_search"
                }
            }
            
            evidence.append(evidence_item)
        
        return evidence
    
    def _extract_reasoning_chain(
        self,
        result: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Extract step-by-step reasoning chain"""
        reasoning_chain = []
        
        # Add LLM reasoning if available
        if 'llm_based' in result and result['llm_based'].get('reasoning_steps'):
            for i, step in enumerate(result['llm_based']['reasoning_steps'], 1):
                reasoning_chain.append({
                    "step": i,
                    "description": step,
                    "source": "LLM Analysis"
                })
        
        # Add rule-based reasoning if available
        if 'rule_based' in result and result['rule_based'].get('matched_rules'):
            for rule in result['rule_based']['matched_rules']:
                reasoning_chain.append({
                    "step": len(reasoning_chain) + 1,
                    "description": rule['explanation'],
                    "source": f"Rule: {rule['rule_name']}"
                })
        
        return reasoning_chain
    
    def _analyze_confidence_factors(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze factors contributing to confidence score"""
        factors = {
            "overall_confidence": result['confidence'],
            "contributing_factors": [],
            "uncertainty_sources": []
        }
        
        # Rule-based confidence
        if 'rule_based' in result:
            rule_conf = result['rule_based'].get('confidence', 0)
            if rule_conf > 0:
                factors["contributing_factors"].append({
                    "factor": "Rule-based match",
                    "impact": "positive",
                    "strength": rule_conf,
                    "description": f"Deterministic rules matched with {rule_conf:.0%} confidence"
                })
        
        # LLM confidence
        if 'llm_based' in result:
            llm_conf = result['llm_based'].get('confidence', 0)
            if llm_conf > 0:
                factors["contributing_factors"].append({
                    "factor": "LLM semantic analysis",
                    "impact": "positive",
                    "strength": llm_conf,
                    "description": f"LLM analysis confidence: {llm_conf:.0%}"
                })
        
        # Ambiguities as uncertainty sources
        if 'llm_based' in result and result['llm_based'].get('ambiguities'):
            for ambiguity in result['llm_based']['ambiguities']:
                factors["uncertainty_sources"].append({
                    "source": "Ambiguous interpretation",
                    "description": ambiguity
                })
        
        # Method agreement/disagreement
        if result.get('method') == 'hybrid_agreement':
            factors["contributing_factors"].append({
                "factor": "Method agreement",
                "impact": "positive",
                "strength": 0.1,
                "description": "Rule-based and LLM methods agree on classification"
            })
        elif result.get('method') in ['llm_override', 'rule_override']:
            factors["uncertainty_sources"].append({
                "source": "Method disagreement",
                "description": "Rule-based and LLM methods produced different classifications"
            })
        
        return factors
    
    def _identify_alternatives(
        self,
        result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify alternative interpretations or edge cases"""
        alternatives = []
        
        # Check for disagreement between methods
        if 'rule_based' in result and 'llm_based' in result:
            rule_cat = result['rule_based'].get('category')
            llm_cat = result['llm_based'].get('category')
            
            if rule_cat and llm_cat and rule_cat != llm_cat:
                alternatives.append({
                    "interpretation": f"Alternative classification: {rule_cat}",
                    "source": "Rule-based engine",
                    "confidence": result['rule_based'].get('confidence', 0),
                    "rationale": "Deterministic rules suggest different classification"
                })
        
        # Check for detected risks that might suggest different category
        if 'llm_based' in result and result['llm_based'].get('detected_risks'):
            for risk in result['llm_based']['detected_risks']:
                if 'high-risk' in risk.lower() and result['risk_category'] != 'HIGH_RISK':
                    alternatives.append({
                        "interpretation": "Potential HIGH_RISK classification",
                        "source": "Risk detection",
                        "confidence": 0.6,
                        "rationale": f"Detected risk: {risk}"
                    })
        
        return alternatives
    
    def _extract_key_factors(
        self,
        ai_metadata: Dict[str, Any],
        result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract key factors that influenced the decision"""
        key_factors = []
        
        # Sector influence
        if 'sector' in ai_metadata:
            key_factors.append({
                "factor": "Sector",
                "value": ai_metadata['sector'],
                "influence": "high" if ai_metadata['sector'] in ['banking', 'healthcare', 'law_enforcement'] else "medium",
                "explanation": f"Operating in {ai_metadata['sector']} sector affects risk classification"
            })
        
        # Purpose influence
        if 'purpose' in ai_metadata:
            key_factors.append({
                "factor": "Purpose",
                "value": ai_metadata['purpose'],
                "influence": "high",
                "explanation": f"System purpose: {ai_metadata['purpose']}"
            })
        
        # Autonomy level
        if 'autonomy_level' in ai_metadata:
            key_factors.append({
                "factor": "Autonomy Level",
                "value": ai_metadata['autonomy_level'],
                "influence": "medium",
                "explanation": f"System operates with {ai_metadata['autonomy_level']} autonomy"
            })
        
        # Impact on individuals
        if ai_metadata.get('affects_individuals'):
            key_factors.append({
                "factor": "Individual Impact",
                "value": "Yes",
                "influence": "high",
                "explanation": "System directly affects individuals' rights or access to services"
            })
        
        return key_factors
    
    def _fallback_classification(
        self,
        ai_metadata: Dict[str, Any],
        assessment_id: str,
        timestamp: str
    ) -> Dict[str, Any]:
        """Fallback classification when engines are not available"""
        # Simple heuristic-based classification
        risk_category = "MINIMAL_RISK"
        confidence = 0.5
        
        # Check for high-risk indicators
        if ai_metadata.get('sector') in ['banking', 'healthcare', 'law_enforcement']:
            risk_category = "HIGH_RISK"
            confidence = 0.7
        
        if ai_metadata.get('purpose') in ['creditworthiness_assessment', 'biometric_identification']:
            risk_category = "HIGH_RISK"
            confidence = 0.8
        
        if ai_metadata.get('purpose') == 'social_scoring':
            risk_category = "PROHIBITED"
            confidence = 0.9
        
        reasoning_steps = [
            f"System operates in {ai_metadata.get('sector', 'unknown')} sector",
            f"Primary purpose: {ai_metadata.get('purpose', 'unknown')}",
            "Classification based on heuristic rules (engines unavailable)"
        ]
        
        return {
            "assessment_id": assessment_id,
            "timestamp": timestamp,
            "risk_category": risk_category,
            "confidence": confidence,
            "method": "fallback_heuristic",
            "requires_human_review": True,
            "legal_basis": {
                "primary_article": "Article 6(2), Annex III",
                "supporting_articles": []
            },
            "reasoning": {
                "steps": reasoning_steps
            },
            "compliance_obligations": self._get_compliance_obligations(risk_category),
            "rag_enabled": False,
            "retrieved_documents_count": 0,
            "explainability": {
                "decision_summary": f"The AI system has been classified as {risk_category} using basic heuristic rules. (Confidence: {confidence:.0%}). Note: Advanced classification engines are unavailable.",
                "evidence": [],
                "reasoning_chain": [
                    {
                        "step": i + 1,
                        "description": step,
                        "source": "Fallback Heuristic"
                    }
                    for i, step in enumerate(reasoning_steps)
                ],
                "confidence_factors": {
                    "overall_confidence": confidence,
                    "contributing_factors": [
                        {
                            "factor": "Basic heuristic rules",
                            "impact": "positive",
                            "strength": confidence,
                            "description": "Simple sector and purpose-based classification"
                        }
                    ],
                    "uncertainty_sources": [
                        {
                            "source": "Limited analysis",
                            "description": "Advanced classification engines unavailable - using basic heuristics only"
                        }
                    ]
                },
                "alternative_interpretations": [],
                "key_factors": self._extract_key_factors(ai_metadata, {
                    "risk_category": risk_category,
                    "confidence": confidence
                })
            }
        }


# Global service instance
_classification_service = None

def get_classification_service() -> ClassificationService:
    """Get or create classification service instance"""
    global _classification_service
    if _classification_service is None:
        _classification_service = ClassificationService()
    return _classification_service

# Made with Bob
