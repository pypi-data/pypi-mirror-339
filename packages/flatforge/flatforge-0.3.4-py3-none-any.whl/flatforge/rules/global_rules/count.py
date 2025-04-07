"""
Count validation rule for FlatForge.

This module contains the CountRule class that validates the number of records in a section.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import ValidationError, ParsedRecord, FieldValue
from flatforge.rules.base import GlobalRule


class CountRule(GlobalRule):
    """
    Rule that counts the number of records in a section.
    
    This rule verifies that the number of records in a section matches
    a specified count or a count from another field.
    """
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a CountRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.state = {"count": 0}
        self.expected_count = params.get("expected_count")
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only count records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
            
        self.state["count"] += 1
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            List[ValidationError]: List of validation errors, if any
        """
        errors = []
        
        if self.expected_count is not None and self.state["count"] != self.expected_count:
            errors.append(
                ValidationError(
                    f"Count mismatch: expected {self.expected_count}, got {self.state['count']}",
                    self.name,
                    error_code="COUNT_MISMATCH"
                )
            )
            
        return errors
        
    def calculate_value(self) -> Optional[int]:
        """
        Get the calculated count.
        
        Returns:
            Optional[int]: The calculated count, or None if not calculated
        """
        return self.state["count"] 