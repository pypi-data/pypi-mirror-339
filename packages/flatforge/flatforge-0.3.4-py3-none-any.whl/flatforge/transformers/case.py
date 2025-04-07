"""
Case transformer for FlatForge.

This module contains the CaseRule for transforming text case.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class CaseRule(TransformerRule):
    """A transformer that changes the case of text.

    Example:
        Input: "hello world"
        Output: "HELLO WORLD" (for type="upper")
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary containing:
                - type (str): Case type ("upper", "lower", "title", "camel", default: "upper")
        """
        super().__init__(name, config)
        self.type = config.get("type", "upper")

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a field value by changing its case.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The transformed value with the specified case.
        """
        value = field_value.value
        if not value:
            return value

        if self.type == "upper":
            return value.upper()
        elif self.type == "lower":
            return value.lower()
        elif self.type == "title":
            return value.title()
        elif self.type == "camel":
            words = value.split()
            return words[0].lower() + "".join(word.title() for word in words[1:])
        return value 