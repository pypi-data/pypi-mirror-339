"""
Global rule factory for FlatForge.

This module contains the GlobalRuleFactory class that creates global rules.
"""
from typing import Dict, List, Optional, Any, Type

from flatforge.rules.base import GlobalRule
from flatforge.rules.global_rules.count import CountRule
from flatforge.rules.global_rules.sum import SumRule
from flatforge.rules.global_rules.checksum import ChecksumRule
from flatforge.rules.global_rules.uniqueness import UniquenessRule


class GlobalRuleFactory:
    """Factory class for creating global rules."""
    
    _rules: Dict[str, Type[GlobalRule]] = {
        "count": CountRule,
        "sum": SumRule,
        "checksum": ChecksumRule,
        "uniqueness": UniquenessRule,
    }
    
    @classmethod
    def create(cls, rule_type: str, name: str, params: Optional[dict] = None) -> GlobalRule:
        """
        Create a global rule.
        
        Args:
            rule_type: The type of rule to create
            name: The name of the rule
            params: Optional parameters for the rule
            
        Returns:
            GlobalRule: The created rule
            
        Raises:
            ValueError: If the rule type is not recognized
        """
        if rule_type not in cls._rules:
            raise ValueError(f"Unknown global rule type: {rule_type}")
            
        rule_class = cls._rules[rule_type]
        return rule_class(name, params) 