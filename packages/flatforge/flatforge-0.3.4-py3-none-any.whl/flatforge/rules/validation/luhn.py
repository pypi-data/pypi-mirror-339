"""
Luhn validation rule for FlatForge.

This module contains the LuhnRule class that validates numbers using the Luhn algorithm.
"""
from typing import Dict, List, Optional, Any, Tuple, Union, overload
import re

from flatforge.core import ValidationError, FieldValue, ParsedRecord, Field
from flatforge.rules.base import ValidationRule


class LuhnRule(ValidationRule):
    """Rule that validates numbers using the Luhn algorithm."""
    
    def __init__(self, name: str, params: Optional[Dict[str, Any]] = None):
        """
        Initialize a LuhnRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule including:
                - field: The name of the field to validate
                - strip_spaces: Whether to strip spaces from the value
                - strip_hyphens: Whether to strip hyphens from the value
                - error_message: Custom error message to use
        """
        super().__init__(name, params or {})
        self.field = self.params.get('field', '')
        self.strip_spaces = self.params.get('strip_spaces', True)
        self.strip_hyphens = self.params.get('strip_hyphens', True)
        self.error_message = self.params.get('error_message', "Invalid credit card number")
    
    def _is_valid_luhn(self, number: str) -> bool:
        """
        Check if a number is valid according to the Luhn algorithm.
        
        Args:
            number: The number to check
            
        Returns:
            bool: True if the number is valid, False otherwise
        """
        digits = [int(d) for d in str(number)]
        checksum = 0
        is_even = len(digits) % 2 == 0
        
        for i, digit in enumerate(digits):
            if is_even:
                if i % 2 == 0:
                    doubled = digit * 2
                    checksum += doubled if doubled < 10 else doubled - 9
                else:
                    checksum += digit
            else:
                if i % 2 == 1:
                    doubled = digit * 2
                    checksum += doubled if doubled < 10 else doubled - 9
                else:
                    checksum += digit
                    
        return checksum % 10 == 0
    
    @overload
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None: ...
    
    @overload
    def validate(self, record: Dict[str, Any]) -> Tuple[bool, Optional[str]]: ...
    
    def validate(self, field_value_or_record: Union[FieldValue, Dict[str, Any], ParsedRecord], record: Optional[ParsedRecord] = None) -> Optional[Tuple[bool, Optional[str]]]:
        """
        Validate a credit card number using the Luhn algorithm.
        
        This method supports both the new API (field_value, record) and
        the old API (record) for backward compatibility.
        
        Args:
            field_value_or_record: Either a FieldValue object, a dictionary record, or a ParsedRecord
            record: The record containing the field value (optional when field_value_or_record is a dict)
            
        Returns:
            Optional[Tuple[bool, Optional[str]]]: A tuple with (is_valid, error_message) when used with old API
            
        Raises:
            ValidationError: If the credit card number is invalid (when used with new API)
        """
        # If the first argument is a dictionary, we're using the old API (dict style)
        if isinstance(field_value_or_record, dict):
            return self.validate_dict(field_value_or_record)
        
        # If the first argument is a ParsedRecord, we're using a different test API
        if isinstance(field_value_or_record, ParsedRecord):
            parsed_record = field_value_or_record
            field_name = self.params.get('field', '')
            
            # Check if the field exists in the record
            if field_name not in parsed_record.field_values:
                return False, f"Field {field_name} not found in record"
            
            # Extract the field value and validate it
            field_value = parsed_record.field_values[field_name]
            try:
                self.validate(field_value, parsed_record)
                return True, None
            except ValidationError as e:
                return False, str(e)
        
        # Otherwise, we're using the new API
        field_value = field_value_or_record
        value = field_value.value
        
        # Skip empty values (use RequiredRule to enforce non-empty)
        if not value.strip():
            raise ValidationError(
                "Invalid credit card number format",
                field_name=field_value.field.name,
                rule_name=self.name,
                value=value
            )
        
        # Remove spaces and hyphens if configured
        card_number = value
        if self.strip_spaces:
            card_number = card_number.replace(" ", "")
        if self.strip_hyphens:
            card_number = card_number.replace("-", "")
        
        # Check if card_number contains only digits after processing
        if not card_number.isdigit():
            raise ValidationError(
                "Credit card number must contain only digits" + 
                (", spaces," if self.strip_spaces else "") + 
                (" or hyphens" if self.strip_hyphens else ""),
                field_name=field_value.field.name,
                rule_name=self.name,
                value=value
            )
        
        # Check if card_number has a valid length
        if len(card_number) < 13 or len(card_number) > 19:
            raise ValidationError(
                "Credit card number must be between 13 and 19 digits",
                field_name=field_value.field.name,
                rule_name=self.name,
                value=value
            )
        
        # Apply Luhn algorithm
        if not self._is_valid_luhn(card_number):
            raise ValidationError(
                self.error_message or "Invalid credit card number (failed Luhn check)",
                field_name=field_value.field.name,
                rule_name=self.name,
                value=value
            )
            
    # Backward compatibility method
    def validate_dict(self, record: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate a credit card number in a dictionary record.
        
        This method is for backward compatibility with older test code that expected
        a validate method that accepts a single record argument and returns a tuple
        with (success, error_message).
        
        Args:
            record: The dictionary record containing the field to validate
            
        Returns:
            Tuple[bool, Optional[str]]: A tuple with (is_valid, error_message)
        """
        column = self.params.get('column', self.params.get('field', ''))
        if not column or column not in record:
            return False, f"Field {column} not found in record"
            
        value = record[column]
        
        # Create dummy field and field_value for validation
        field = Field(name=column, position=0)
        field_value = FieldValue(field=field, value=str(value))
        
        try:
            # Use the standard validate method with field_value
            self.validate(field_value, None)
            return True, None
        except ValidationError as e:
            return False, str(e) 