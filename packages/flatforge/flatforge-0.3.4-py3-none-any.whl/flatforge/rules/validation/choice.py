"""
Choice validation rule for FlatForge.

This module contains the ChoiceRule class that validates that a field value is one of a set of allowed values.
"""
from typing import Dict, List, Optional, Any, Set

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class ChoiceRule(ValidationRule):
    """Rule that validates that a field value is one of a set of allowed values."""
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a ChoiceRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.choices = set(params.get("choices", []))
        self.case_sensitive = params.get("case_sensitive", True)
        
        if not self.case_sensitive:
            self.choices = {str(choice).lower() for choice in self.choices}
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate that a field value is one of the allowed choices.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field value is not one of the allowed choices
        """
        value = str(field_value.value)
        if not self.case_sensitive:
            value = value.lower()
            
        if value not in self.choices:
            raise ValidationError(
                f"Field value must be one of: {', '.join(sorted(self.choices))}",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            ) 