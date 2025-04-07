"""
Global rules for FlatForge.

This module contains the global rules for validating across multiple records.
"""
import hashlib
from typing import Dict, List, Optional, Any, Set, Tuple

from flatforge.core import ValidationError, ParsedRecord
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
            A list of validation errors, if any
        """
        errors = []
        
        # Check if the count matches the expected count
        expected_count = self.params.get("expected_count")
        if expected_count is not None:
            expected_count = int(expected_count)
            actual_count = self.state["count"]
            
            if actual_count != expected_count:
                errors.append(ValidationError(
                    f"Record count mismatch: expected {expected_count}, got {actual_count}",
                    rule_name=self.name,
                    error_code="COUNT_MISMATCH"
                ))
                
        # Check if the count matches a field value
        count_field = self.params.get("count_field")
        if count_field and not self.should_insert_value():
            section_name, field_name = count_field.split(".")
            # This would require access to the parsed records, which we don't have here
            # In a real implementation, we would need to store the parsed records
            # or the specific field value in the state
            pass
            
        return errors
        
    def calculate_value(self) -> Any:
        """
        Calculate the count value.
        
        Returns:
            The count of records
        """
        return self.state["count"]


class SumRule(GlobalRule):
    """
    Rule that sums the values of a field across all records.
    
    This rule verifies that the sum of a field across all records matches
    a specified sum or a sum from another field.
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
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only sum records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
            
        # Get the field to sum
        field_name = self.params.get("field")
        if not field_name:
            return
            
        # Get the field value
        field_value = record.field_values.get(field_name)
        if not field_value:
            return
            
        # Try to convert the value to a number and add it to the sum
        try:
            value = field_value.value.strip()
            if value:
                self.state["sum"] += float(value)
        except (ValueError, TypeError):
            # Ignore non-numeric values
            pass
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            A list of validation errors, if any
        """
        errors = []
        
        # Check if the sum matches the expected sum
        expected_sum = self.params.get("expected_sum")
        if expected_sum is not None:
            expected_sum = float(expected_sum)
            actual_sum = self.state["sum"]
            
            # Allow for a small tolerance due to floating point precision
            tolerance = float(self.params.get("tolerance", 0.0001))
            
            if abs(actual_sum - expected_sum) > tolerance:
                errors.append(ValidationError(
                    f"Sum mismatch: expected {expected_sum}, got {actual_sum}",
                    rule_name=self.name,
                    error_code="SUM_MISMATCH"
                ))
                
        # Check if the sum matches a field value
        sum_field = self.params.get("sum_field")
        if sum_field and not self.should_insert_value():
            section_name, field_name = sum_field.split(".")
            # This would require access to the parsed records, which we don't have here
            # In a real implementation, we would need to store the parsed records
            # or the specific field value in the state
            pass
            
        return errors
        
    def calculate_value(self) -> Any:
        """
        Calculate the sum value.
        
        Returns:
            The sum of field values
        """
        return self.state["sum"]


class ChecksumRule(GlobalRule):
    """
    Rule that calculates a checksum of a field across all records.
    
    This rule verifies that the checksum of a field across all records matches
    a specified checksum or a checksum from another field.
    
    Extended functionality allows for:
    - Multi-column checksums (combining values from multiple fields)
    - Row-based checksums (using all fields in a record)
    - Different hashing algorithms (MD5, SHA256)
    """
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a ChecksumRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        
        # Legacy parameters
        self.field = self.params.get("field")
        self.checksum_type = self.params.get("type", "sum")
        
        # New extended parameters
        self.validation_type = self.params.get("validation_type", "column")  # 'column', 'multi_column', or 'row'
        self.columns = self.params.get("columns", [])  # List of columns for multi-column checksum
        self.algorithm = self.params.get("algorithm", "")  # Algorithm for hash-based checksums
        self.target_field = self.params.get("target_field")  # Field containing the expected checksum
        
        # Initialize state based on checksum type or algorithm
        if self.checksum_type == "md5" or self.algorithm.upper() == "MD5":
            self.state = {"checksum": hashlib.md5()}
        elif self.algorithm.upper() == "SHA256":
            self.state = {"checksum": hashlib.sha256()}
        elif self.checksum_type in ["sum", "xor", "mod10"]:
            # Numeric checksum types
            self.state = {"checksum": 0}
        else:
            # Default to numeric checksum for unknown types
            self.state = {"checksum": 0}
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only checksum records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
        
        # Handle different validation types
        if self.validation_type == "multi_column" and self.columns:
            # Process multiple columns
            self._process_multiple_columns(record)
        elif self.validation_type == "row":
            # Process entire row
            self._process_row(record)
        else:
            # Legacy single column behavior
            self._process_single_column(record)
    
    def _process_single_column(self, record: ParsedRecord) -> None:
        """Process a single column for checksum calculation."""
        # Get the field to checksum (legacy parameter)
        field_name = self.field
        if not field_name:
            return
            
        # Get the field value
        field_value = record.field_values.get(field_name)
        if not field_value:
            return
            
        # Calculate the checksum
        value = field_value.value
        self._update_checksum(value)
    
    def _process_multiple_columns(self, record: ParsedRecord) -> None:
        """Process multiple columns for checksum calculation."""
        if not self.columns:
            return
            
        # Combine values from specified columns
        values = []
        for column in self.columns:
            field_value = record.field_values.get(column)
            if not field_value:
                continue
            values.append(field_value.value)
        
        # Calculate checksum of combined values
        combined_value = ''.join(values)
        self._update_checksum(combined_value)
    
    def _process_row(self, record: ParsedRecord) -> None:
        """Process the entire row for checksum calculation."""
        # Exclude the target field if specified
        row_data = {}
        for field_name, field_value in record.field_values.items():
            if self.target_field and field_name == self.target_field:
                continue
            row_data[field_name] = field_value.value
            
        # Calculate checksum of the row data
        self._update_checksum(str(row_data))
    
    def _update_checksum(self, value: str) -> None:
        """Update the checksum based on the value and algorithm."""
        # Check if it's a hash object by checking for the update method
        if hasattr(self.state["checksum"], 'update') and callable(self.state["checksum"].update):
            # It's a hash object (MD5 or SHA256)
            self.state["checksum"].update(value.encode())
        # Handle numeric checksums
        elif self.checksum_type == "sum":
            # Sum the ASCII values of the characters
            self.state["checksum"] += sum(ord(c) for c in value)
        elif self.checksum_type == "xor":
            # XOR the ASCII values of the characters
            for c in value:
                self.state["checksum"] ^= ord(c)
        elif self.checksum_type == "mod10":
            # Modulo 10 checksum (Luhn algorithm)
            try:
                digits = [int(d) for d in value if d.isdigit()]
                self.state["checksum"] = (self.state["checksum"] + sum(digits)) % 10
            except (ValueError, TypeError):
                # Ignore non-numeric values
                pass
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            A list of validation errors, if any
        """
        errors = []
        
        # Check if the checksum matches the expected checksum
        expected_checksum = self.params.get("expected_checksum")
        if expected_checksum is not None:
            actual_checksum = self.calculate_value()
            
            if isinstance(actual_checksum, str) and isinstance(expected_checksum, str):
                # Case-insensitive comparison for hash digests
                if actual_checksum.lower() != expected_checksum.lower():
                    errors.append(ValidationError(
                        f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}",
                        rule_name=self.name,
                        error_code="CHECKSUM_MISMATCH"
                    ))
            else:
                # Numeric comparison
                if actual_checksum != expected_checksum:
                    errors.append(ValidationError(
                        f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}",
                        rule_name=self.name,
                        error_code="CHECKSUM_MISMATCH"
                    ))
                
        # Check if the checksum matches a field value
        checksum_field = self.params.get("checksum_field") or self.target_field
        if checksum_field and not self.should_insert_value():
            section_name, field_name = checksum_field.split(".")
            # This would require access to the parsed records, which we don't have here
            # In a real implementation, we would need to store the parsed records
            # or the specific field value in the state
            pass
            
        return errors
        
    def calculate_value(self) -> Any:
        """
        Calculate the checksum value.
        
        Returns:
            The calculated checksum
        """
        # Check if it's a hash object by checking for the hexdigest method
        if hasattr(self.state["checksum"], 'hexdigest') and callable(self.state["checksum"].hexdigest):
            return self.state["checksum"].hexdigest()
        return self.state["checksum"]


class UniquenessRule(GlobalRule):
    """
    Rule that validates the uniqueness of field values across records.
    
    This rule verifies that the values of specified fields are unique across
    all records in a section.
    """
    
    def __init__(self, name: str, params: Optional[dict] = None):
        """
        Initialize a UniquenessRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.state = {
            "values": set(),  # For single field uniqueness
            "composite_values": set(),  # For composite field uniqueness
            "duplicates": []  # To track duplicate records
        }
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only check records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
            
        # Get the field(s) to check for uniqueness
        fields = self.params.get("fields")
        if not fields:
            return
            
        # Check if we're validating a single field or multiple fields
        if isinstance(fields, str):
            # Single field uniqueness
            field_name = fields
            field_value = record.field_values.get(field_name)
            if not field_value:
                return
                
            value = field_value.value.strip()
            if value in self.state["values"]:
                # Record the duplicate
                self.state["duplicates"].append((record.record_number, field_name, value))
                # Mark the record as invalid
                record.is_valid = False
                field_value.errors.append(ValidationError(
                    f"Duplicate value: {value}",
                    field_name=field_name,
                    rule_name=self.name,
                    error_code="DUPLICATE_VALUE",
                    section_name=record.section.name,
                    record_number=record.record_number,
                    field_value=value
                ))
            else:
                self.state["values"].add(value)
        else:
            # Composite field uniqueness
            composite_value = []
            for field_name in fields:
                field_value = record.field_values.get(field_name)
                if not field_value:
                    return
                composite_value.append(field_value.value.strip())
                
            # Convert to tuple for hashability
            composite_tuple = tuple(composite_value)
            if composite_tuple in self.state["composite_values"]:
                # Record the duplicate
                self.state["duplicates"].append((record.record_number, fields, composite_value))
                # Mark the record as invalid
                record.is_valid = False
                for i, field_name in enumerate(fields):
                    field_value = record.field_values.get(field_name)
                    field_value.errors.append(ValidationError(
                        f"Duplicate composite value: {composite_value}",
                        field_name=field_name,
                        rule_name=self.name,
                        error_code="DUPLICATE_COMPOSITE_VALUE",
                        section_name=record.section.name,
                        record_number=record.record_number,
                        field_value=field_value.value
                    ))
            else:
                self.state["composite_values"].add(composite_tuple)
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            A list of validation errors, if any
        """
        errors = []
        
        # Report any duplicates found
        for record_number, field_name, value in self.state["duplicates"]:
            if isinstance(field_name, str):
                errors.append(ValidationError(
                    f"Duplicate value in record {record_number}: {value}",
                    field_name=field_name,
                    rule_name=self.name,
                    error_code="DUPLICATE_VALUE"
                ))
            else:
                errors.append(ValidationError(
                    f"Duplicate composite value in record {record_number}: {value}",
                    field_name=",".join(field_name),
                    rule_name=self.name,
                    error_code="DUPLICATE_COMPOSITE_VALUE"
                ))
                
        return errors 