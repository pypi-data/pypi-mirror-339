"""
Base transformer for FlatForge.

This module contains the base transformer class that all transformers inherit from.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord, ValidationError
from flatforge.rules.base import Rule


class TransformerRule(Rule):
    """Base class for all transformers."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize the transformer.
        
        Args:
            name: The name of the transformer
            config: The transformer configuration
        """
        super().__init__(name, config)
        self.fields = config.get('fields', [])
        
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Transform a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The transformed value
        """
        raise NotImplementedError("Subclasses must implement transform()")

    def apply(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Apply the transformer rule to a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
        """
        try:
            field_value.transformed_value = self.transform(field_value, record)
        except Exception as e:
            error = ValidationError(
                f"Transformation failed: {str(e)}",
                field_name=field_value.field.name,
                rule_name=self.name,
                section_name=record.section.name,
                record_number=record.record_number,
                field_value=field_value.value
            )
            field_value.errors.append(error)
            record.is_valid = False


# Register transformer rules
TRANSFORMER_RULES = {
    'trim': 'flatforge.transformers.trim.TrimRule',
    'case': 'flatforge.transformers.case.CaseRule',
    'pad': 'flatforge.transformers.pad.PadRule',
    'date_format': 'flatforge.transformers.date_format.DateFormatRule',
    'substring': 'flatforge.transformers.substring.SubstringRule',
    'replace': 'flatforge.transformers.replace.ReplaceRule',
    'value_resolver': 'flatforge.transformers.value_resolver.ValueResolverTransformationRule',
    'mask': 'flatforge.transformers.mask.MaskTransformationRule',
    'guid': 'flatforge.transformers.guid.GenerateGuidTransformationRule',
    'luhn': 'flatforge.transformers.luhn.LuhnTransformer',
} 