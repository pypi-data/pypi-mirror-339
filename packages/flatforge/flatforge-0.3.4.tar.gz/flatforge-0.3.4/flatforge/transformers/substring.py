"""
Substring transformer for FlatForge.

This module contains the SubstringRule for extracting substrings from field values.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class SubstringRule(TransformerRule):
    """A transformer that extracts a substring from a field value.

    Example:
        Input: "hello world"
        Output: "llo " (for start=2, end=6)
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary containing:
                - start (int): Starting index (inclusive)
                - end (int): Ending index (exclusive)
        """
        super().__init__(name, config)
        self.start = config.get("start")
        self.end = config.get("end")

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a field value by extracting a substring.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The extracted substring.
        """
        value = field_value.value
        if not value:
            return value

        if self.start is None:
            return value

        if self.end is None:
            return value[self.start:]
        return value[self.start:self.end] 