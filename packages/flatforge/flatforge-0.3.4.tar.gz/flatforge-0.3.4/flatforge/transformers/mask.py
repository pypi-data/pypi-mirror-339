"""
Mask transformer for FlatForge.

This module contains the MaskTransformationRule for masking sensitive data in field values.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class MaskTransformationRule(TransformerRule):
    """A transformer that masks sensitive data in field values.

    Example:
        Input: "4111111111111111"
        Output: "411111******1111"
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary containing:
                - start_index (int): Starting index for masking (optional)
                - mask_length (int): Number of characters to mask (optional)
                - keep_first (int): Number of characters to keep at the start (optional)
                - keep_last (int): Number of characters to keep at the end (optional)
                - mask_char (str): Character to use for masking (default: "*")
                - mask_pattern (str): Regex pattern for masking (optional)
        """
        super().__init__(name, config)
        self.start_index = config.get("start_index")
        self.mask_length = config.get("mask_length")
        self.keep_first = config.get("keep_first")
        self.keep_last = config.get("keep_last")
        self.mask_char = config.get("mask_char", "*")
        self.mask_pattern = config.get("mask_pattern")

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a field value by masking sensitive data.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The transformed value with sensitive data masked.
        """
        value = field_value.value
        if not value:
            return value

        if self.mask_pattern:
            import re
            return re.sub(self.mask_pattern, self.mask_char, value)

        if self.keep_first is not None and self.keep_last is not None:
            if len(value) <= self.keep_first + self.keep_last:
                return value
            return value[:self.keep_first] + self.mask_char * (len(value) - self.keep_first - self.keep_last) + value[-self.keep_last:]

        if self.start_index is not None and self.mask_length is not None:
            if self.start_index >= len(value):
                return value
            if self.start_index + self.mask_length <= len(value):
                return value[:self.start_index] + self.mask_char * self.mask_length + value[self.start_index + self.mask_length:]
            return value

        return value 