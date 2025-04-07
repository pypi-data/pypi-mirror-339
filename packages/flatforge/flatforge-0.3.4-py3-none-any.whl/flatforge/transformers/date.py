"""
Date format transformer for FlatForge.

This module contains the DateFormatRule transformer for formatting date fields.
"""
import datetime
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class DateFormatRule(TransformerRule):
    """Rule that formats a date field."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Format a date field.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The formatted date
        """
        value = field_value.value.strip()
        if not value:
            return value
            
        input_format = self.params.get("input_format", "%Y%m%d")
        output_format = self.params.get("output_format", "%Y-%m-%d")
        
        try:
            date = datetime.datetime.strptime(value, input_format)
            return date.strftime(output_format)
        except ValueError:
            # If the date can't be parsed, return the original value
            return value 