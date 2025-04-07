"""
Transformation rules for FlatForge.

This module contains the transformation rules for transforming field values.
"""
import re
import datetime
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.rules.base import TransformerRule


class TrimRule(TransformerRule):
    """Rule that trims whitespace from a field value."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Trim whitespace from a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The trimmed value
        """
        value = field_value.value
        trim_type = self.params.get("type", "both")
        
        if trim_type == "left":
            return value.lstrip()
        elif trim_type == "right":
            return value.rstrip()
        else:  # both
            return value.strip()


class CaseRule(TransformerRule):
    """Rule that changes the case of a field value."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Change the case of a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The transformed value
        """
        value = field_value.value
        case_type = self.params.get("type", "upper")
        
        if case_type == "upper":
            return value.upper()
        elif case_type == "lower":
            return value.lower()
        elif case_type == "title":
            return value.title()
        elif case_type == "camel":
            words = value.split()
            if not words:
                return ""
            result = words[0].lower()
            for word in words[1:]:
                if word:
                    result += word[0].upper() + word[1:].lower()
            return result
        else:
            return value


class PadRule(TransformerRule):
    """Rule that pads a field value to a specified length."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Pad a field value to a specified length.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The padded value
        """
        value = field_value.value
        length = self.params.get("length", field_value.field.length)
        if not length:
            raise ValueError("Pad rule requires a 'length' parameter or field length")
            
        pad_char = self.params.get("char", " ")
        pad_side = self.params.get("side", "left")
        
        if len(value) >= length:
            return value
            
        if pad_side == "left":
            return pad_char * (length - len(value)) + value
        else:  # right
            return value + pad_char * (length - len(value))


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


class SubstringRule(TransformerRule):
    """Rule that extracts a substring from a field value."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Extract a substring from a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The extracted substring
        """
        value = field_value.value
        start = self.params.get("start", 0)
        end = self.params.get("end", None)
        
        return value[start:end]


class ReplaceRule(TransformerRule):
    """Rule that replaces text in a field value."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Replace text in a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The value with replacements
        """
        value = field_value.value
        old = self.params.get("old", "")
        new = self.params.get("new", "")
        
        if not old:
            return value
            
        return value.replace(old, new)


class ValueResolverTransformationRule(TransformerRule):
    """Transforms a value from source field to target field based on a mapping file."""
    
    def __init__(self, config):
        super().__init__(config)
        self.source_field = config.get('source_field')
        self.target_field = config.get('target_field')
        self.mapping_file = config.get('mapping_file')
        self.default_value = config.get('default_value', '')
        self._mapping_cache = None
        
    def transform(self, record):
        if not self.source_field or not self.target_field or not self.mapping_file:
            return record, False, "Missing required parameters"
            
        # Load mapping if not loaded
        if self._mapping_cache is None:
            self._load_mapping()
            
        source_value = record.get(self.source_field, '')
        target_value = self._mapping_cache.get(source_value, self.default_value)
        
        # Set the resolved value
        record[self.target_field] = target_value
        return record, True, None
        
    def _load_mapping(self):
        """Load the mapping file."""
        import json
        import os
        
        try:
            if not os.path.exists(self.mapping_file):
                self._mapping_cache = {}
                return
                
            with open(self.mapping_file, 'r') as f:
                self._mapping_cache = json.load(f)
        except Exception as e:
            self._mapping_cache = {}
            # Log error or handle appropriately


class MaskTransformationRule(TransformerRule):
    """Transforms a value by masking parts of it."""
    
    def __init__(self, config):
        super().__init__(config)
        self.source_field = config.get('source_field')
        self.target_field = config.get('target_field', self.source_field)  # Default to source field
        self.mask_char = config.get('mask_char', '*')
        
        # Support both styles of configuration
        self.start_index = config.get('start_index')
        self.mask_length = config.get('mask_length')
        self.keep_first = config.get('keep_first')
        self.keep_last = config.get('keep_last')
        
    def transform(self, record):
        if not self.source_field or self.source_field not in record:
            return record, False, f"Source field '{self.source_field}' not found"
            
        value = str(record[self.source_field])
        masked_value = self._mask_value(value)
        
        record[self.target_field] = masked_value
        return record, True, None
        
    def _mask_value(self, value):
        """Apply masking to the value."""
        if len(value) == 0:
            return value
            
        # If using keep_first/keep_last style
        if self.keep_first is not None and self.keep_last is not None:
            keep_first = int(self.keep_first)
            keep_last = int(self.keep_last)
            
            if keep_first + keep_last >= len(value):
                return value  # Not enough characters to mask
                
            prefix = value[:keep_first]
            suffix = value[-keep_last:] if keep_last > 0 else ""
            mask_length = len(value) - keep_first - len(suffix)
            masked = self.mask_char * mask_length
            
            return prefix + masked + suffix
            
        # If using start_index/mask_length style
        elif self.start_index is not None and self.mask_length is not None:
            start = int(self.start_index)
            length = int(self.mask_length)
            
            if start >= len(value) or length <= 0:
                return value  # Nothing to mask
                
            # Adjust length if it goes beyond the string
            if start + length > len(value):
                length = len(value) - start
                
            prefix = value[:start]
            suffix = value[start+length:] if start + length < len(value) else ""
            masked = self.mask_char * length
            
            return prefix + masked + suffix
            
        # Default behavior if parameters are missing
        else:
            # Mask all but the last 4 characters
            if len(value) <= 4:
                return value
            return self.mask_char * (len(value) - 4) + value[-4:]


class GenerateGuidTransformationRule(TransformerRule):
    """Generates a GUID/UUID and stores it in the target field."""
    
    def __init__(self, config):
        super().__init__(config)
        self.target_field = config.get('target_field')
        self.version = config.get('version', 4)  # Default to version 4 (random)
        
    def transform(self, record):
        if not self.target_field:
            return record, False, "Target field not specified"
            
        # Generate UUID based on version
        import uuid
        
        if self.version == 1:
            # Time-based UUID
            generated_uuid = str(uuid.uuid1())
        elif self.version == 3:
            # Name-based UUID with MD5
            # This would need additional parameters like namespace and name
            # For simplicity, we'll use a default namespace and the record as name
            generated_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(record)))
        elif self.version == 5:
            # Name-based UUID with SHA-1
            generated_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(record)))
        else:
            # Default to version 4 (random)
            generated_uuid = str(uuid.uuid4())
            
        record[self.target_field] = generated_uuid
        return record, True, None


class TransformationRuleFactory:
    @staticmethod
    def create_rule(rule_type, config):
        if rule_type == 'trim':
            return TrimRule(config)
        elif rule_type == 'case':
            return CaseRule(config)
        elif rule_type == 'pad':
            return PadRule(config)
        elif rule_type == 'date_format':
            return DateFormatRule(config)
        elif rule_type == 'substring':
            return SubstringRule(config)
        elif rule_type == 'replace':
            return ReplaceRule(config)
        elif rule_type == 'value_resolver':
            return ValueResolverTransformationRule(config)
        elif rule_type == 'mask':
            return MaskTransformationRule(config)
        elif rule_type == 'generate_guid':
            return GenerateGuidTransformationRule(config)
        else:
            raise ValueError(f"Unknown rule type: {rule_type}") 