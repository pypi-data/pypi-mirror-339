"""
GUID transformer for FlatForge.

This module contains the GenerateGuidTransformationRule for generating GUIDs.
"""
import uuid
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class GenerateGuidTransformationRule(TransformerRule):
    """A transformer that generates a GUID (UUID).

    Example:
        Input: ""
        Output: "550e8400-e29b-41d4-a716-446655440000"
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary containing:
                - version (int): UUID version (1 or 4, default: 4)
        """
        super().__init__(name, config)
        self.version = config.get("version", 4)

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a field value by generating a GUID.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The generated GUID.
        """
        if self.version == 1:
            return str(uuid.uuid1())
        return str(uuid.uuid4()) 