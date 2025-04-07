"""
Pad transformer for FlatForge.

This module contains the PadRule for padding field values.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class PadRule(TransformerRule):
    """A transformer that pads field values to a specified length.

    Example:
        Input: "123"
        Output: "00123" (for length=5, char="0", side="left")
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary containing:
                - length (int): Target length for the padded string
                - char (str): Character to use for padding (default: " ")
                - side (str): Side to pad ("left" or "right", default: "left")
        """
        super().__init__(name, config)
        self.length = config.get("length")
        self.char = config.get("char", " ")
        self.side = config.get("side", "left")
        if len(self.char) != 1:
            raise ValueError("Padding character must be a single character")
        if self.side not in ["left", "right"]:
            raise ValueError("Side must be either 'left' or 'right'")

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a field value by padding it to the specified length.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The padded value.
        """
        value = field_value.value
        if not value or not self.length:
            return value

        padding_length = self.length - len(value)
        if padding_length <= 0:
            return value

        padding = self.char * padding_length
        if self.side == "right":
            return value + padding
        return padding + value 