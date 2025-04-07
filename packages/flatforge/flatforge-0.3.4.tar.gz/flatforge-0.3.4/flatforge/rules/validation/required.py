"""
Required validation rule for FlatForge.

This module contains the RequiredRule class that validates that a field is not empty.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class RequiredRule(ValidationRule):
    """Rule that validates that a field is not empty."""
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate that a field is not empty.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field is empty
        """
        if not field_value.value or field_value.value.strip() == "":
            raise ValidationError(
                "Field is required",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            ) 