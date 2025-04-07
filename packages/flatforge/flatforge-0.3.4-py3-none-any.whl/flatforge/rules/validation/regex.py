"""
Regex validation rule for FlatForge.

This module contains the RegexRule class that validates a field against a regular expression pattern.
"""
import re
from typing import Dict, List, Optional, Any, Pattern

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class RegexRule(ValidationRule):
    """Rule that validates a field against a regular expression pattern."""
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a RegexRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.pattern = params.get("pattern")
        if self.pattern:
            self.regex = re.compile(self.pattern)
        else:
            self.regex = None
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate a field against a regular expression pattern.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field does not match the pattern
        """
        if not self.regex:
            raise ValidationError(
                "No pattern specified for regex validation",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            )
            
        if not self.regex.match(str(field_value.value)):
            raise ValidationError(
                f"Field does not match pattern: {self.pattern}",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            ) 