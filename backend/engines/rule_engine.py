"""
Rule-Based Classification Engine

Deterministic rule evaluation for EU AI Act classification.
Provides fast, explainable classification for clear-cut cases.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from pathlib import Path


logger = logging.getLogger(__name__)


class RiskCategory(str, Enum):
    """Risk categories"""
    PROHIBITED = "PROHIBITED"
    HIGH_RISK = "HIGH_RISK"
    LIMITED_RISK = "LIMITED_RISK"
    MINIMAL_RISK = "MINIMAL_RISK"
    GPAI = "GENERAL_PURPOSE_AI"
    GPAI_SYSTEMIC_RISK = "GPAI_SYSTEMIC_RISK"
    UNCLASSIFIED = "UNCLASSIFIED"


class Operator(str, Enum):
    """Comparison operators"""
    EQUALS = "=="
    NOT_EQUALS = "!="
    IN = "in"
    NOT_IN = "not_in"
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"


class LogicalOperator(str, Enum):
    """Logical operators"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


@dataclass
class RuleMatch:
    """Result of rule evaluation"""
    rule_id: str
    rule_name: str
    matched: bool
    confidence: float
    category: RiskCategory
    legal_basis: str
    priority: int
    conditions_evaluated: Dict[str, Any]
    explanation: str


@dataclass
class ClassificationRule:
    """Classification rule definition"""
    rule_id: str
    category: RiskCategory
    name: str
    description: str
    conditions: Dict[str, Any]
    legal_basis: str
    confidence: float
    priority: int
    enabled: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClassificationRule':
        """Create rule from dictionary"""
        return cls(
            rule_id=data['rule_id'],
            category=RiskCategory(data['category']),
            name=data['name'],
            description=data['description'],
            conditions=data['conditions'],
            legal_basis=data['legal_basis'],
            confidence=data['confidence'],
            priority=data['priority'],
            enabled=data.get('enabled', True)
        )


class RuleEngine:
    """
    Rule-based classification engine for EU AI Act compliance.
    
    Evaluates deterministic rules against AI system metadata to
    determine risk classification.
    """
    
    def __init__(self, rules_path: Optional[Path] = None):
        """
        Initialize rule engine
        
        Args:
            rules_path: Path to rules JSON file
        """
        self.rules: List[ClassificationRule] = []
        self.rules_by_category: Dict[RiskCategory, List[ClassificationRule]] = {}
        
        if rules_path:
            self.load_rules(rules_path)
    
    def load_rules(self, rules_path: Path) -> None:
        """
        Load rules from JSON file
        
        Args:
            rules_path: Path to rules JSON file
        """
        logger.info(f"Loading rules from {rules_path}")
        
        with open(rules_path, 'r') as f:
            rules_data = json.load(f)
        
        self.rules = []
        for rule_data in rules_data.get('rules', []):
            try:
                rule = ClassificationRule.from_dict(rule_data)
                if rule.enabled:
                    self.rules.append(rule)
            except Exception as e:
                logger.error(f"Error loading rule {rule_data.get('rule_id')}: {e}")
        
        # Sort by priority (lower number = higher priority)
        self.rules.sort(key=lambda r: r.priority)
        
        # Index by category
        self.rules_by_category = {}
        for rule in self.rules:
            if rule.category not in self.rules_by_category:
                self.rules_by_category[rule.category] = []
            self.rules_by_category[rule.category].append(rule)
        
        logger.info(f"Loaded {len(self.rules)} rules")
    
    def evaluate_all_rules(
        self,
        ai_metadata: Dict[str, Any]
    ) -> List[RuleMatch]:
        """
        Evaluate all rules against AI system metadata
        
        Args:
            ai_metadata: AI system metadata dictionary
            
        Returns:
            List of rule matches
        """
        matches = []
        
        for rule in self.rules:
            try:
                match = self.evaluate_rule(rule, ai_metadata)
                matches.append(match)
            except Exception as e:
                logger.error(f"Error evaluating rule {rule.rule_id}: {e}")
        
        return matches
    
    def evaluate_rule(
        self,
        rule: ClassificationRule,
        ai_metadata: Dict[str, Any]
    ) -> RuleMatch:
        """
        Evaluate a single rule
        
        Args:
            rule: Classification rule
            ai_metadata: AI system metadata
            
        Returns:
            Rule match result
        """
        conditions_evaluated = {}
        
        try:
            matched = self._evaluate_conditions(
                rule.conditions,
                ai_metadata,
                conditions_evaluated
            )
            
            explanation = self._generate_explanation(
                rule,
                matched,
                conditions_evaluated
            )
            
            return RuleMatch(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                matched=matched,
                confidence=rule.confidence if matched else 0.0,
                category=rule.category,
                legal_basis=rule.legal_basis,
                priority=rule.priority,
                conditions_evaluated=conditions_evaluated,
                explanation=explanation
            )
        
        except Exception as e:
            logger.error(f"Error in rule {rule.rule_id}: {e}")
            return RuleMatch(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                matched=False,
                confidence=0.0,
                category=rule.category,
                legal_basis=rule.legal_basis,
                priority=rule.priority,
                conditions_evaluated=conditions_evaluated,
                explanation=f"Error evaluating rule: {str(e)}"
            )
    
    def _evaluate_conditions(
        self,
        conditions: Dict[str, Any],
        ai_metadata: Dict[str, Any],
        conditions_evaluated: Dict[str, Any]
    ) -> bool:
        """
        Recursively evaluate conditions
        
        Args:
            conditions: Conditions dictionary
            ai_metadata: AI system metadata
            conditions_evaluated: Dictionary to store evaluation results
            
        Returns:
            True if conditions match, False otherwise
        """
        operator = conditions.get('operator', 'AND')
        
        if operator == LogicalOperator.AND:
            criteria = conditions.get('criteria', [])
            results = []
            
            for i, criterion in enumerate(criteria):
                if 'operator' in criterion and 'criteria' in criterion:
                    # Nested condition
                    result = self._evaluate_conditions(
                        criterion,
                        ai_metadata,
                        conditions_evaluated
                    )
                else:
                    # Leaf condition
                    result = self._evaluate_criterion(
                        criterion,
                        ai_metadata,
                        conditions_evaluated
                    )
                results.append(result)
            
            return all(results)
        
        elif operator == LogicalOperator.OR:
            criteria = conditions.get('criteria', [])
            results = []
            
            for criterion in criteria:
                if 'operator' in criterion and 'criteria' in criterion:
                    result = self._evaluate_conditions(
                        criterion,
                        ai_metadata,
                        conditions_evaluated
                    )
                else:
                    result = self._evaluate_criterion(
                        criterion,
                        ai_metadata,
                        conditions_evaluated
                    )
                results.append(result)
            
            return any(results)
        
        elif operator == LogicalOperator.NOT:
            criteria = conditions.get('criteria', [])
            if criteria:
                criterion = criteria[0]
                if 'operator' in criterion and 'criteria' in criterion:
                    result = self._evaluate_conditions(
                        criterion,
                        ai_metadata,
                        conditions_evaluated
                    )
                else:
                    result = self._evaluate_criterion(
                        criterion,
                        ai_metadata,
                        conditions_evaluated
                    )
                return not result
            return False
        
        else:
            logger.warning(f"Unknown logical operator: {operator}")
            return False
    
    def _evaluate_criterion(
        self,
        criterion: Dict[str, Any],
        ai_metadata: Dict[str, Any],
        conditions_evaluated: Dict[str, Any]
    ) -> bool:
        """
        Evaluate a single criterion
        
        Args:
            criterion: Criterion dictionary
            ai_metadata: AI system metadata
            conditions_evaluated: Dictionary to store evaluation results
            
        Returns:
            True if criterion matches, False otherwise
        """
        field = criterion.get('field')
        operator = criterion.get('operator')
        expected_value = criterion.get('value')
        
        # Get actual value from metadata (support nested fields)
        actual_value = self._get_nested_value(ai_metadata, field)
        
        # Store evaluation
        conditions_evaluated[field] = {
            'expected': expected_value,
            'actual': actual_value,
            'operator': operator
        }
        
        # Evaluate based on operator
        if operator == Operator.EQUALS:
            result = actual_value == expected_value
        
        elif operator == Operator.NOT_EQUALS:
            result = actual_value != expected_value
        
        elif operator == Operator.IN:
            if isinstance(expected_value, list):
                result = actual_value in expected_value
            else:
                result = False
        
        elif operator == Operator.NOT_IN:
            if isinstance(expected_value, list):
                result = actual_value not in expected_value
            else:
                result = True
        
        elif operator == Operator.GREATER_THAN:
            try:
                result = float(actual_value) > float(expected_value)
            except (TypeError, ValueError):
                result = False
        
        elif operator == Operator.GREATER_EQUAL:
            try:
                result = float(actual_value) >= float(expected_value)
            except (TypeError, ValueError):
                result = False
        
        elif operator == Operator.LESS_THAN:
            try:
                result = float(actual_value) < float(expected_value)
            except (TypeError, ValueError):
                result = False
        
        elif operator == Operator.LESS_EQUAL:
            try:
                result = float(actual_value) <= float(expected_value)
            except (TypeError, ValueError):
                result = False
        
        elif operator == Operator.CONTAINS:
            if isinstance(actual_value, str):
                result = expected_value in actual_value
            elif isinstance(actual_value, list):
                result = expected_value in actual_value
            else:
                result = False
        
        elif operator == Operator.STARTS_WITH:
            if isinstance(actual_value, str):
                result = actual_value.startswith(expected_value)
            else:
                result = False
        
        elif operator == Operator.ENDS_WITH:
            if isinstance(actual_value, str):
                result = actual_value.endswith(expected_value)
            else:
                result = False
        
        else:
            logger.warning(f"Unknown operator: {operator}")
            result = False
        
        conditions_evaluated[field]['result'] = result
        return result
    
    def _get_nested_value(
        self,
        data: Dict[str, Any],
        field_path: str
    ) -> Any:
        """
        Get value from nested dictionary using dot notation
        
        Args:
            data: Dictionary to search
            field_path: Field path (e.g., 'basic_information.sector')
            
        Returns:
            Value at field path, or None if not found
        """
        keys = field_path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return None
            else:
                return None
        
        return value
    
    def _generate_explanation(
        self,
        rule: ClassificationRule,
        matched: bool,
        conditions_evaluated: Dict[str, Any]
    ) -> str:
        """
        Generate human-readable explanation
        
        Args:
            rule: Classification rule
            matched: Whether rule matched
            conditions_evaluated: Evaluated conditions
            
        Returns:
            Explanation string
        """
        if matched:
            explanation = f"Rule '{rule.name}' matched. "
            explanation += f"Legal basis: {rule.legal_basis}. "
            
            # Add key conditions that matched
            matched_conditions = [
                f"{field}: {details['actual']}"
                for field, details in conditions_evaluated.items()
                if details.get('result', False)
            ]
            
            if matched_conditions:
                explanation += "Key conditions: " + ", ".join(matched_conditions[:3])
        else:
            explanation = f"Rule '{rule.name}' did not match. "
            
            # Add conditions that failed
            failed_conditions = [
                f"{field} (expected: {details['expected']}, actual: {details['actual']})"
                for field, details in conditions_evaluated.items()
                if not details.get('result', True)
            ]
            
            if failed_conditions:
                explanation += "Failed conditions: " + ", ".join(failed_conditions[:3])
        
        return explanation
    
    def get_best_match(
        self,
        matches: List[RuleMatch]
    ) -> Optional[RuleMatch]:
        """
        Get best matching rule based on priority and confidence
        
        Args:
            matches: List of rule matches
            
        Returns:
            Best matching rule, or None if no matches
        """
        matched_rules = [m for m in matches if m.matched]
        
        if not matched_rules:
            return None
        
        # Sort by priority (lower is higher), then confidence (higher is better)
        matched_rules.sort(key=lambda m: (m.priority, -m.confidence))
        
        return matched_rules[0]
    
    def classify(
        self,
        ai_metadata: Dict[str, Any]
    ) -> Tuple[Optional[RiskCategory], float, List[RuleMatch]]:
        """
        Classify AI system based on rules
        
        Args:
            ai_metadata: AI system metadata
            
        Returns:
            Tuple of (risk_category, confidence, all_matches)
        """
        logger.info("Starting rule-based classification")
        
        # Evaluate all rules
        all_matches = self.evaluate_all_rules(ai_metadata)
        
        # Get best match
        best_match = self.get_best_match(all_matches)
        
        if best_match:
            logger.info(
                f"Classification: {best_match.category.value} "
                f"(confidence: {best_match.confidence}, rule: {best_match.rule_id})"
            )
            return best_match.category, best_match.confidence, all_matches
        else:
            logger.info("No rules matched, defaulting to UNCLASSIFIED")
            return RiskCategory.UNCLASSIFIED, 0.0, all_matches


def create_default_rules() -> List[Dict[str, Any]]:
    """
    Create default rule set
    
    Returns:
        List of rule dictionaries
    """
    rules = [
        # Prohibited practices
        {
            "rule_id": "R-PROHIBITED-001",
            "category": "PROHIBITED",
            "name": "Social Scoring by Public Authority",
            "description": "AI systems for social scoring by public authorities",
            "conditions": {
                "operator": "AND",
                "criteria": [
                    {"field": "deployer_type", "operator": "==", "value": "public_authority"},
                    {"field": "purpose", "operator": "in", "value": ["social_scoring", "trustworthiness_evaluation"]},
                ]
            },
            "legal_basis": "Article 5(1)(c)",
            "confidence": 1.0,
            "priority": 1,
            "enabled": True
        },
        # High-risk: Creditworthiness
        {
            "rule_id": "R-HR-012",
            "category": "HIGH_RISK",
            "name": "Creditworthiness Assessment",
            "description": "AI for creditworthiness assessment in banking",
            "conditions": {
                "operator": "AND",
                "criteria": [
                    {"field": "sector", "operator": "in", "value": ["banking", "financial_services"]},
                    {"field": "purpose", "operator": "in", "value": ["creditworthiness_assessment", "loan_approval"]},
                ]
            },
            "legal_basis": "Article 6(2), Annex III(5)(b)",
            "confidence": 1.0,
            "priority": 2,
            "enabled": True
        },
        # Add more rules as needed
    ]
    
    return rules


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create sample rules file
    rules_data = {
        "version": "1.0",
        "rules": create_default_rules()
    }
    
    rules_path = Path("rules.json")
    with open(rules_path, 'w') as f:
        json.dump(rules_data, f, indent=2)
    
    # Initialize engine
    engine = RuleEngine(rules_path)
    
    # Test classification
    test_metadata = {
        "sector": "banking",
        "purpose": "creditworthiness_assessment",
        "deployer_type": "private_company"
    }
    
    category, confidence, matches = engine.classify(test_metadata)
    print(f"\nClassification: {category}")
    print(f"Confidence: {confidence}")
    print(f"\nMatched rules:")
    for match in matches:
        if match.matched:
            print(f"  - {match.rule_name} ({match.confidence})")

# Made with Bob
