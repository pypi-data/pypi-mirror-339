"""
Date validation rule for FlatForge.

This module contains the DateRule class that validates date formats.
"""
import datetime
from typing import Dict, List, Optional, Any

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class DateRule(ValidationRule):
    """Rule that validates date formats."""
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a DateRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.format = params.get("format", "%Y-%m-%d")
        self.min_date = params.get("min_date")
        self.max_date = params.get("max_date")
        
        if self.min_date:
            self.min_date = datetime.datetime.strptime(self.min_date, self.format).date()
        if self.max_date:
            self.max_date = datetime.datetime.strptime(self.max_date, self.format).date()
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate a date field.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the date is invalid or out of range
        """
        try:
            date = datetime.datetime.strptime(str(field_value.value), self.format).date()
            
            if self.min_date and date < self.min_date:
                raise ValidationError(
                    f"Date must be on or after {self.min_date}",
                    field_name=field_value.field.name,
                    value=field_value.value,
                    rule_name=self.name
                )
                
            if self.max_date and date > self.max_date:
                raise ValidationError(
                    f"Date must be on or before {self.max_date}",
                    field_name=field_value.field.name,
                    value=field_value.value,
                    rule_name=self.name
                )
                
        except ValueError:
            raise ValidationError(
                f"Invalid date format. Expected format: {self.format}",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            ) 