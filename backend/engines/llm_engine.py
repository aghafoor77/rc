"""
LLM-Based Semantic Reasoning Engine

Uses Meta Llama 3 via Ollama for nuanced classification cases
that require contextual understanding and legal reasoning.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import ollama


logger = logging.getLogger(__name__)


@dataclass
class LLMClassificationResult:
    """Result from LLM classification"""
    risk_category: str
    confidence: float
    reasoning_steps: List[str]
    legal_articles: List[str]
    detected_risks: List[str]
    ambiguities: List[str]
    raw_response: str
    tokens_used: int


class LLMEngine:
    """
    LLM-based classification engine using Meta Llama 3.
    
    Handles nuanced cases requiring semantic understanding
    and provides explainable reasoning chains.
    """
    
    def __init__(
        self,
        model_name: str = "llama3:8b",
        temperature: float = 0.1,
        max_tokens: int = 2048,
        ollama_host: str = "http://localhost:11434"
    ):
        """
        Initialize LLM engine
        
        Args:
            model_name: Ollama model name
            temperature: Temperature for generation (lower = more deterministic)
            max_tokens: Maximum tokens to generate
            ollama_host: Ollama server URL
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.ollama_host = ollama_host
        
        # Initialize Ollama client
        self.client = ollama.Client(host=ollama_host)
        
        logger.info(f"Initialized LLM engine with model: {model_name}")
    
    def classify(
        self,
        ai_metadata: Dict[str, Any],
        rag_context: Optional[str] = None,
        rule_results: Optional[List[Dict[str, Any]]] = None
    ) -> LLMClassificationResult:
        """
        Classify AI system using LLM reasoning
        
        Args:
            ai_metadata: AI system metadata
            rag_context: Retrieved legal context from RAG
            rule_results: Results from rule-based engine
            
        Returns:
            LLM classification result
        """
        logger.info("Starting LLM-based classification")
        
        # Build prompt
        prompt = self._build_prompt(ai_metadata, rag_context, rule_results)
        
        # Generate response
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                }
            )
            
            raw_response = response['response']
            
            # Parse structured output
            result = self._parse_response(raw_response)
            
            # Calculate tokens (approximate)
            tokens_used = len(prompt.split()) + len(raw_response.split())
            result.tokens_used = tokens_used
            
            logger.info(
                f"LLM classification complete: {result.risk_category} "
                f"(confidence: {result.confidence})"
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Error in LLM classification: {e}")
            raise
    
    def _build_prompt(
        self,
        ai_metadata: Dict[str, Any],
        rag_context: Optional[str],
        rule_results: Optional[List[Dict[str, Any]]]
    ) -> str:
        """
        Build prompt for LLM
        
        Args:
            ai_metadata: AI system metadata
            rag_context: RAG context
            rule_results: Rule engine results
            
        Returns:
            Formatted prompt
        """
        prompt = """You are an expert EU AI Act compliance specialist. Your task is to classify an AI system according to the EU AI Act risk categories.

RISK CATEGORIES:
1. PROHIBITED - AI practices that are banned (Article 5)
2. HIGH_RISK - AI systems with significant risks requiring strict compliance (Annex III)
3. LIMITED_RISK - AI systems with transparency obligations (Article 52)
4. MINIMAL_RISK - AI systems with no specific obligations
5. GENERAL_PURPOSE_AI - Foundation models (Article 51)
6. GPAI_SYSTEMIC_RISK - GPAI with systemic risk (>10^25 FLOPs)

"""
        
        # Add legal context from RAG
        if rag_context:
            prompt += f"""RELEVANT LEGAL PROVISIONS:
{rag_context}

"""
        
        # Add rule engine results if available
        if rule_results:
            prompt += "RULE-BASED ANALYSIS:\n"
            for result in rule_results[:5]:  # Top 5 rules
                if result.get('matched'):
                    prompt += f"- Rule {result['rule_id']}: {result['rule_name']} (matched)\n"
            prompt += "\n"
        
        # Add AI system metadata
        prompt += f"""AI SYSTEM METADATA:
{json.dumps(ai_metadata, indent=2)}

INSTRUCTIONS:
1. Analyze the AI system carefully
2. Consider all risk categories
3. Identify which EU AI Act provisions apply
4. Provide step-by-step reasoning
5. Assign a risk category with confidence score (0.0-1.0)
6. List detected risks and ambiguities

Respond in the following JSON format:
{{
  "risk_category": "PROHIBITED|HIGH_RISK|LIMITED_RISK|MINIMAL_RISK|GENERAL_PURPOSE_AI|GPAI_SYSTEMIC_RISK",
  "confidence": 0.0-1.0,
  "reasoning_steps": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "legal_articles": [
    "Article X",
    "Annex Y"
  ],
  "detected_risks": [
    "Risk 1",
    "Risk 2"
  ],
  "ambiguities": [
    "Ambiguity 1 if any"
  ]
}}

Think step-by-step and provide your analysis:
"""
        
        return prompt
    
    def _parse_response(self, raw_response: str) -> LLMClassificationResult:
        """
        Parse LLM response into structured result
        
        Args:
            raw_response: Raw LLM response
            
        Returns:
            Parsed classification result
        """
        try:
            # Try to extract JSON from response
            json_start = raw_response.find('{')
            json_end = raw_response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = raw_response[json_start:json_end]
                data = json.loads(json_str)
                
                return LLMClassificationResult(
                    risk_category=data.get('risk_category', 'UNCLASSIFIED'),
                    confidence=float(data.get('confidence', 0.0)),
                    reasoning_steps=data.get('reasoning_steps', []),
                    legal_articles=data.get('legal_articles', []),
                    detected_risks=data.get('detected_risks', []),
                    ambiguities=data.get('ambiguities', []),
                    raw_response=raw_response,
                    tokens_used=0  # Will be set by caller
                )
            else:
                # Fallback: parse unstructured response
                logger.warning("Could not parse JSON from LLM response, using fallback")
                return self._parse_unstructured_response(raw_response)
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return self._parse_unstructured_response(raw_response)
    
    def _parse_unstructured_response(self, raw_response: str) -> LLMClassificationResult:
        """
        Fallback parser for unstructured responses
        
        Args:
            raw_response: Raw response text
            
        Returns:
            Best-effort classification result
        """
        # Extract risk category
        risk_category = "UNCLASSIFIED"
        for category in ["PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK", 
                        "GENERAL_PURPOSE_AI", "GPAI_SYSTEMIC_RISK"]:
            if category in raw_response.upper():
                risk_category = category
                break
        
        # Extract confidence (look for numbers between 0 and 1)
        confidence = 0.5  # Default
        import re
        confidence_match = re.search(r'confidence[:\s]+([0-9.]+)', raw_response, re.IGNORECASE)
        if confidence_match:
            try:
                confidence = float(confidence_match.group(1))
                confidence = max(0.0, min(1.0, confidence))
            except ValueError:
                pass
        
        return LLMClassificationResult(
            risk_category=risk_category,
            confidence=confidence,
            reasoning_steps=[raw_response],
            legal_articles=[],
            detected_risks=[],
            ambiguities=["Unable to parse structured response"],
            raw_response=raw_response,
            tokens_used=0
        )
    
    def explain_classification(
        self,
        ai_metadata: Dict[str, Any],
        classification: str,
        rag_context: Optional[str] = None
    ) -> str:
        """
        Generate detailed explanation for a classification
        
        Args:
            ai_metadata: AI system metadata
            classification: Assigned classification
            rag_context: Legal context
            
        Returns:
            Detailed explanation
        """
        prompt = f"""You are an EU AI Act compliance expert. Explain why the following AI system was classified as {classification}.

AI SYSTEM:
{json.dumps(ai_metadata, indent=2)}

"""
        
        if rag_context:
            prompt += f"""LEGAL BASIS:
{rag_context}

"""
        
        prompt += """Provide a clear, detailed explanation that:
1. Identifies the key characteristics that led to this classification
2. References specific EU AI Act articles
3. Explains the compliance implications
4. Is understandable to non-technical stakeholders

Explanation:
"""
        
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.3,
                    "num_predict": 1024,
                }
            )
            
            return response['response']
        
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Error generating explanation: {str(e)}"


class HybridClassificationEngine:
    """
    Hybrid engine combining rule-based and LLM-based classification.
    
    Uses deterministic rules for clear cases and LLM for nuanced cases.
    """
    
    def __init__(
        self,
        rule_engine,
        llm_engine: LLMEngine,
        confidence_threshold: float = 0.85
    ):
        """
        Initialize hybrid engine
        
        Args:
            rule_engine: Rule-based engine instance
            llm_engine: LLM engine instance
            confidence_threshold: Threshold for rule-based confidence
        """
        self.rule_engine = rule_engine
        self.llm_engine = llm_engine
        self.confidence_threshold = confidence_threshold
        
        logger.info("Initialized hybrid classification engine")
    
    def classify(
        self,
        ai_metadata: Dict[str, Any],
        rag_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classify using hybrid approach
        
        Args:
            ai_metadata: AI system metadata
            rag_context: RAG context
            
        Returns:
            Classification result with reasoning
        """
        logger.info("Starting hybrid classification")
        
        # Step 1: Try rule-based classification
        rule_category, rule_confidence, rule_matches = self.rule_engine.classify(ai_metadata)
        
        # Prepare rule results for LLM
        rule_results = [
            {
                'rule_id': m.rule_id,
                'rule_name': m.rule_name,
                'matched': m.matched,
                'confidence': m.confidence,
                'category': m.category.value
            }
            for m in rule_matches if m.matched
        ]
        
        # Step 2: Decide whether to use LLM
        use_llm = False
        reason = ""
        
        if rule_confidence >= self.confidence_threshold:
            # High confidence rule match - use rule result
            final_category = rule_category
            final_confidence = rule_confidence
            method = "rule_based"
            reason = f"High confidence rule match ({rule_confidence:.2f})"
            logger.info(f"Using rule-based result: {final_category} ({rule_confidence})")
        
        elif rule_confidence > 0.0:
            # Medium confidence - use LLM to verify
            use_llm = True
            reason = f"Medium confidence rule match ({rule_confidence:.2f}), using LLM for verification"
            logger.info("Medium confidence, using LLM for verification")
        
        else:
            # No rule match - use LLM
            use_llm = True
            reason = "No rule match, using LLM for classification"
            logger.info("No rule match, using LLM")
        
        # Step 3: LLM classification if needed
        llm_result = None
        if use_llm:
            llm_result = self.llm_engine.classify(
                ai_metadata,
                rag_context,
                rule_results
            )
            
            # Combine results
            if rule_confidence > 0.0:
                # Verify rule result with LLM
                if llm_result.risk_category == rule_category.value:
                    # Agreement - boost confidence
                    final_category = rule_category
                    final_confidence = min(1.0, (rule_confidence + llm_result.confidence) / 2 + 0.1)
                    method = "hybrid_agreement"
                    reason = "Rule and LLM agree"
                else:
                    # Disagreement - use higher confidence
                    if llm_result.confidence > rule_confidence:
                        final_category = llm_result.risk_category
                        final_confidence = llm_result.confidence
                        method = "llm_override"
                        reason = f"LLM override (LLM: {llm_result.confidence:.2f} > Rule: {rule_confidence:.2f})"
                    else:
                        final_category = rule_category
                        final_confidence = rule_confidence
                        method = "rule_override"
                        reason = f"Rule override (Rule: {rule_confidence:.2f} > LLM: {llm_result.confidence:.2f})"
            else:
                # No rule match - use LLM result
                final_category = llm_result.risk_category
                final_confidence = llm_result.confidence
                method = "llm_only"
                reason = "LLM classification (no rule match)"
        
        # Step 4: Determine if human review is needed
        requires_human_review = (
            final_confidence < 0.75 or
            (use_llm and rule_confidence > 0.0 and 
             llm_result and llm_result.risk_category != rule_category.value)
        )
        
        # Step 5: Build result
        result = {
            'risk_category': final_category.value if hasattr(final_category, 'value') else final_category,
            'confidence': final_confidence,
            'method': method,
            'reason': reason,
            'requires_human_review': requires_human_review,
            'rule_based': {
                'category': rule_category.value if rule_category else None,
                'confidence': rule_confidence,
                'matched_rules': [
                    {
                        'rule_id': m.rule_id,
                        'rule_name': m.rule_name,
                        'confidence': m.confidence,
                        'explanation': m.explanation
                    }
                    for m in rule_matches if m.matched
                ]
            }
        }
        
        if llm_result:
            result['llm_based'] = {
                'category': llm_result.risk_category,
                'confidence': llm_result.confidence,
                'reasoning_steps': llm_result.reasoning_steps,
                'legal_articles': llm_result.legal_articles,
                'detected_risks': llm_result.detected_risks,
                'ambiguities': llm_result.ambiguities,
                'tokens_used': llm_result.tokens_used
            }
        
        logger.info(
            f"Hybrid classification complete: {result['risk_category']} "
            f"(confidence: {result['confidence']:.2f}, method: {method})"
        )
        
        return result


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Initialize LLM engine
    llm_engine = LLMEngine(model_name="llama3:8b")
    
    # Test classification
    test_metadata = {
        "system_name": "Credit Scoring System",
        "sector": "banking",
        "purpose": "creditworthiness_assessment",
        "autonomy_level": "fully_automated",
        "affects_individuals": True,
        "impacts_financial_access": True
    }
    
    result = llm_engine.classify(test_metadata)
    
    print(f"\nClassification: {result.risk_category}")
    print(f"Confidence: {result.confidence}")
    print(f"\nReasoning:")
    for i, step in enumerate(result.reasoning_steps, 1):
        print(f"  {i}. {step}")
    print(f"\nLegal Articles: {', '.join(result.legal_articles)}")

# Made with Bob
