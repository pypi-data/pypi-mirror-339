"""
Sum validation rule for FlatForge.

This module contains the SumRule class that validates the sum of numeric fields.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import ValidationError, ParsedRecord, FieldValue
from flatforge.rules.base import GlobalRule


class SumRule(GlobalRule):
    """
    Rule that validates the sum of numeric fields.
    
    This rule verifies that the sum of numeric fields matches
    a specified value or a value from another field.
    """
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a SumRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.state = {"sum": 0}
        self.field_name = params.get("field")
        self.expected_sum = params.get("expected_sum")
        
        if not self.field_name:
            raise ValueError("field parameter is required")
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only process records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
            
        field_value = record.field_values.get(self.field_name)
        if field_value:
            try:
                self.state["sum"] += int(field_value.value)
            except (ValueError, TypeError):
                pass  # Skip non-numeric values
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            List[ValidationError]: List of validation errors, if any
        """
        errors = []
        
        if self.expected_sum is not None and self.state["sum"] != self.expected_sum:
            errors.append(
                ValidationError(
                    f"Sum mismatch: expected {self.expected_sum}, got {self.state['sum']}",
                    self.name,
                    error_code="SUM_MISMATCH"
                )
            )
            
        return errors
        
    def calculate_value(self) -> Optional[int]:
        """
        Get the calculated sum.
        
        Returns:
            Optional[int]: The calculated sum, or None if not calculated
        """
        return self.state["sum"] 