"""
Value resolver transformer for FlatForge.

This module contains the ValueResolverTransformationRule for resolving values from a mapping file.
"""
import json
import csv
from typing import Dict, List, Optional, Any, Union
import os

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class ValueResolverTransformationRule(TransformerRule):
    """A transformer that resolves values from a mapping file.

    Example:
        Input: "A"
        Output: "Active" (if "A" maps to "Active" in the mapping file)
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary containing:
                - mapping_file (str): Path to the JSON or CSV mapping file
                - source_field (str): Name of the field to get the value from
                - default_value (str, optional): Default value if no mapping found
                - key_column (str, optional): Column name for the key in the mapping file
                - value_column (str, optional): Column name for the value in the mapping file
        """
        super().__init__(name, config)
        self.mapping_file = config.get("mapping_file")
        self.source_field = config.get("source_field")
        self.target_field = config.get("target_field", self.source_field)
        self.default_value = config.get("default_value")
        self.key_column = config.get('key_column', self.source_field)
        self.value_column = config.get('value_column', 'value')
        self._mapping = None
        
        if not self.mapping_file:
            raise ValueError("mapping_file must be specified")
        
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """Transform a field value by resolving it from the mapping file.

        Args:
            field_value (FieldValue): The field value to transform.
            record (ParsedRecord): The record containing all field values.

        Returns:
            str: The resolved value from the mapping file.
        """
        if not self.mapping_file:
            return field_value.value

        try:
            if self._mapping is None:
                self._load_mapping_from_file()

            source_value = field_value.value
            return self._mapping.get(source_value, self.default_value or source_value)
        except Exception:
            # If there's any error, return the original value
            return field_value.value
    
    def _load_mapping_from_file(self) -> None:
        """Load the mapping from the specified file."""
        _, ext = os.path.splitext(self.mapping_file)
        if ext.lower() == '.json':
            with open(self.mapping_file, 'r') as f:
                self._mapping = json.load(f)
        else:  # Assume CSV
            with open(self.mapping_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                self._mapping = {row.get(self.key_column): row.get(self.value_column) for row in reader}
        
    def _load_mapping(self) -> Dict[str, str]:
        """
        Load the mapping file.
        
        Returns:
            The mapping dictionary
        """
        mapping = {}
        try:
            with open(self.mapping_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = row.get(self.key_column)
                    value = row.get(self.value_column)
                    if key is not None and value is not None:
                        mapping[key] = value
        except (FileNotFoundError, KeyError) as e:
            raise ValueError(f"Error loading mapping file: {str(e)}")
        return mapping
        
    # Backward compatibility method for dictionary-style records
    def transform_dict(self, record: Dict[str, Any]) -> None:
        """
        Transform a dictionary record by resolving values from the mapping file.
        
        This method is provided for backward compatibility with code that uses
        dictionary-style records instead of ParsedRecord objects.
        
        Args:
            record: The dictionary record to transform
        """
        if not self.mapping_file or self.source_field not in record:
            return
            
        try:
            if self._mapping is None:
                self._load_mapping_from_file()
                        
            source_value = record[self.source_field]
            resolved_value = self._mapping.get(source_value, self.default_value or source_value)
            record[self.target_field] = resolved_value
        except Exception:
            # If there's any error, leave the record unchanged
            pass 