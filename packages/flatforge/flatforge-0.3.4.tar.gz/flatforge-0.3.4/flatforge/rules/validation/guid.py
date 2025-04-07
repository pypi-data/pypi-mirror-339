"""
GUID validation rule for FlatForge.

This module contains the GuidRule class that validates GUID/UUID formats.
"""
import uuid
import re
from typing import Dict, List, Optional, Any, Tuple, Union, overload

from flatforge.core import ValidationError, FieldValue, ParsedRecord, Field
from flatforge.rules.base import ValidationRule


class GuidRule(ValidationRule):
    """Rule that validates GUID/UUID formats."""
    
    def __init__(self, name: str, params: Optional[Dict[str, Any]] = None):
        """
        Initialize a GuidRule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule including:
                - field: The name of the field to validate
                - version: Optional UUID version to validate against
                - strip_spaces: Whether to strip spaces from the value
                - strip_hyphens: Whether to strip hyphens from the value
                - error_message: Custom error message to use
        """
        super().__init__(name, params or {})
        self.version = self.params.get("version")
        self.strip_spaces = self.params.get("strip_spaces", True)
        self.strip_hyphens = self.params.get("strip_hyphens", True)
        self.error_message = self.params.get("error_message", "Invalid GUID format")
        
    def _clean_guid(self, value: str) -> str:
        """
        Clean a GUID string by removing spaces, braces, and other formatting.
        
        Args:
            value: The GUID string to clean
            
        Returns:
            str: The cleaned GUID string
        """
        if not value:
            return ""
            
        guid = str(value).strip()
        
        # Remove URN prefix if present
        if guid.startswith("urn:uuid:"):
            guid = guid[9:]
            
        # Remove braces and parentheses
        guid = re.sub(r"[{}\(\)]", "", guid)
        
        # Remove spaces if configured
        if self.strip_spaces:
            guid = guid.replace(" ", "")
            
        # Remove hyphens if configured
        if self.strip_hyphens:
            guid = guid.replace("-", "")
            
        return guid
    
    @overload
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None: ...
    
    @overload
    def validate(self, record: Dict[str, Any]) -> Tuple[bool, Optional[str]]: ...
    
    def validate(self, field_value_or_record: Union[FieldValue, Dict[str, Any], ParsedRecord], record: Optional[ParsedRecord] = None) -> Optional[Tuple[bool, Optional[str]]]:
        """
        Validate a GUID/UUID field.
        
        This method supports both the new API (field_value, record) and
        the old API (record) for backward compatibility.
        
        Args:
            field_value_or_record: Either a FieldValue object, a dictionary record, or a ParsedRecord
            record: The record containing the field value (optional when field_value_or_record is a dict)
            
        Returns:
            Optional[Tuple[bool, Optional[str]]]: A tuple with (is_valid, error_message) when used with old API
            
        Raises:
            ValidationError: If the GUID/UUID is invalid (when used with new API)
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
                "Invalid GUID/UUID format",
                field_name=field_value.field.name,
                rule_name=self.name,
                value=value
            )
        
        # Clean the GUID
        cleaned_guid = self._clean_guid(value)
        
        if not cleaned_guid:
            raise ValidationError(
                "Invalid GUID/UUID format",
                field_name=field_value.field.name,
                rule_name=self.name,
                value=value
            )
            
        try:
            # Add hyphens back in standard positions if they were removed
            if self.strip_hyphens and len(cleaned_guid) == 32:
                cleaned_guid = f"{cleaned_guid[:8]}-{cleaned_guid[8:12]}-{cleaned_guid[12:16]}-{cleaned_guid[16:20]}-{cleaned_guid[20:]}"
                
            guid = uuid.UUID(cleaned_guid)
            
            # Check the UUID version if specified
            if self.version is not None and guid.version != self.version:
                raise ValidationError(
                    f"Field must be a UUID version {self.version}",
                    field_name=field_value.field.name,
                    rule_name=self.name,
                    value=value
                )
        except ValueError:
            raise ValidationError(
                self.error_message,
                field_name=field_value.field.name,
                rule_name=self.name,
                value=value
            )
            
    # Backward compatibility method
    def validate_dict(self, record: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate a GUID/UUID in a dictionary record.
        
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