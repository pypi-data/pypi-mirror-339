"""
Trim transformer for FlatForge.

This module contains the TrimRule for trimming whitespace from field values.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class TrimRule(TransformerRule):
    """A transformer that trims whitespace from field values.

    Example:
        Input: "  hello  "
        Output: "hello" (for type="both")
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary containing:
                - type (str): Trim type ("left", "right", "both", default: "both")
        """
        super().__init__(name, config)
        self.type = config.get("type", "both")

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a field value by trimming whitespace.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The trimmed value.
        """
        value = field_value.value
        if not value:
            return value

        if self.type == "left":
            return value.lstrip()
        elif self.type == "right":
            return value.rstrip()
        return value.strip() 