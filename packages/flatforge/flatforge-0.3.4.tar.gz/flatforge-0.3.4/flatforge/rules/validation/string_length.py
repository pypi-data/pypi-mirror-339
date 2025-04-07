"""
String length validation rule for FlatForge.

This module contains the StringLengthRule class that validates the length of a string field.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class StringLengthRule(ValidationRule):
    """Rule that validates the length of a string field."""
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a StringLengthRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.min_length = params.get("min_length")
        self.max_length = params.get("max_length")
        self.exact_length = params.get("exact_length")
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate the length of a string field.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field length is invalid
        """
        value = str(field_value.value)
        length = len(value)
        
        if self.exact_length is not None and length != self.exact_length:
            raise ValidationError(
                f"Field must be exactly {self.exact_length} characters long",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            )
            
        if self.min_length is not None and length < self.min_length:
            raise ValidationError(
                f"Field must be at least {self.min_length} characters long",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            )
            
        if self.max_length is not None and length > self.max_length:
            raise ValidationError(
                f"Field must be at most {self.max_length} characters long",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            ) 