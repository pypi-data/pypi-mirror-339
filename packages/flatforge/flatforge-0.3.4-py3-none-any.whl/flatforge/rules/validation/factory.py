"""
Validation rule factory for FlatForge.

This module contains the ValidationRuleFactory class that creates validation rules.
"""
from typing import Dict, List, Optional, Any, Type

from flatforge.rules.base import ValidationRule
from flatforge.rules.validation import (
    RequiredRule,
    NumericRule,
    StringLengthRule,
    RegexRule,
    DateRule,
    ChoiceRule,
    LuhnRule,
    GuidRule,
)


class ValidationRuleFactory:
    """Factory class for creating validation rules."""
    
    _rules: Dict[str, str] = {
        "required": "flatforge.rules.validation.required.RequiredRule",
        "numeric": "flatforge.rules.validation.numeric.NumericRule",
        "string_length": "flatforge.rules.validation.string_length.StringLengthRule",
        "regex": "flatforge.rules.validation.regex.RegexRule",
        "date": "flatforge.rules.validation.date.DateRule",
        "choice": "flatforge.rules.validation.choice.ChoiceRule",
        "luhn": "flatforge.rules.validation.luhn.LuhnRule",
        "guid": "flatforge.rules.validation.guid.GuidRule",
    }
    
    @classmethod
    def create(cls, rule_type: str, name: str, params: Optional[dict] = None) -> ValidationRule:
        """
        Create a validation rule.
        
        Args:
            rule_type: The type of rule to create
            name: The name of the rule
            params: Optional parameters for the rule
            
        Returns:
            ValidationRule: The created rule
            
        Raises:
            ValueError: If the rule type is not recognized
        """
        if rule_type not in cls._rules:
            raise ValueError(f"Unknown validation rule type: {rule_type}")
            
        # Import the rule class dynamically
        module_path, class_name = cls._rules[rule_type].rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        rule_class = getattr(module, class_name)
        
        return rule_class(name, params) 