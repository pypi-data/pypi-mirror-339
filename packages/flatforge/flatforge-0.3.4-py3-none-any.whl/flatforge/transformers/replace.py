"""
Replace transformer for FlatForge.

This module contains the ReplaceRule for replacing text in field values.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class ReplaceRule(TransformerRule):
    """A transformer that replaces text in field values.

    Example:
        Input: "abc123abc"
        Output: "XYZ123XYZ" (for old="abc", new="XYZ")
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary containing:
                - old (str): Text to replace
                - new (str): Text to replace with
        """
        super().__init__(name, config)
        self.old = config.get("old")
        self.new = config.get("new", "")

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a field value by replacing text.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The transformed value with text replaced.
        """
        value = field_value.value
        if not value or not self.old:
            return value

        return value.replace(self.old, self.new) 