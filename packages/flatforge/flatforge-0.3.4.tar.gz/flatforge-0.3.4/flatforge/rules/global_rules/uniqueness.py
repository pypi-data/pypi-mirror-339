"""
Uniqueness validation rule for FlatForge.

This module contains the UniquenessRule class that validates field uniqueness.
"""
from typing import Dict, List, Optional, Any, Set, Tuple, Union

from flatforge.core import ValidationError, ParsedRecord, FieldValue
from flatforge.rules.base import GlobalRule


class UniquenessRule(GlobalRule):
    """
    Rule that validates field uniqueness.
    
    This rule verifies that values in a field or combination of fields
    are unique across all records.
    """
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a UniquenessRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.state = {"values": set(), "duplicates": set()}
        
        # Get fields to check for uniqueness
        fields = params.get("fields", [])
        if isinstance(fields, str):
            fields = [fields]
        self.fields = fields
            
        self.case_sensitive = params.get("case_sensitive", True)
    
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
            
        # Get values for all fields
        values = []
        for field in self.fields:
            field_value = record.field_values.get(field)
            if field_value:
                value = str(field_value.value)
                if not self.case_sensitive:
                    value = value.lower()
                values.append(value)
            else:
                values.append("")
                
        # Create a composite key for uniqueness check
        composite_key = "|".join(values)
                
        if composite_key in self.state["values"]:
            self.state["duplicates"].add(composite_key)
        else:
            self.state["values"].add(composite_key)
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            List[ValidationError]: List of validation errors, if any
        """
        errors = []
        for value in self.state["duplicates"]:
            values = value.split("|")
            field_values = dict(zip(self.fields, values))
            if len(self.fields) == 1:
                # Single field
                errors.append(
                    ValidationError(
                        f"Duplicate value found: {field_values}",
                        self.name,
                        error_code="DUPLICATE_VALUE"
                    )
                )
            else:
                # Composite fields
                errors.append(
                    ValidationError(
                        f"Duplicate composite value found: {field_values}",
                        self.name,
                        error_code="DUPLICATE_VALUE"
                    )
                )
        return errors 