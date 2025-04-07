"""
Configuration validator module for FlatForge.

This module contains the main configuration validator class that combines
schema validation and domain-specific validation.
"""
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

from flatforge.validators.schema import SchemaValidator
from flatforge.validators.domain import DomainValidator


class ConfigValidator:
    """
    Main configuration validator for FlatForge.
    
    This class validates a configuration using both schema validation and
    domain-specific validation.
    """
    
    @classmethod
    def from_file(cls, config_file: Union[str, Path], schema_file: Optional[str] = None) -> 'ConfigValidator':
        """
        Create a configuration validator from a file.
        
        Args:
            config_file: Path to the configuration file
            schema_file: Optional path to a custom JSON schema file
            
        Returns:
            A ConfigValidator instance
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported or the file content is invalid
        """
        config_file = Path(config_file)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        # Load the configuration based on file extension
        with open(config_file, "r") as f:
            if config_file.suffix.lower() in ('.yaml', '.yml'):
                try:
                    config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    raise ValueError(f"Invalid YAML: {str(e)}")
            elif config_file.suffix.lower() == '.json':
                try:
                    config = json.load(f)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON: {str(e)}")
            else:
                raise ValueError(f"Unsupported file format: {config_file.suffix}")
            
        return cls(config, schema_path=schema_file)
    
    def __init__(self, config: Dict[str, Any], schema_path: Optional[str] = None):
        """
        Initialize a configuration validator.
        
        Args:
            config: The configuration to validate
            schema_path: Optional path to a custom JSON schema file
        """
        self.config = config
        self.schema_validator = SchemaValidator(schema_path)
        self.domain_validator = DomainValidator(config)
        self.errors: List[str] = []
    
    def validate(self) -> bool:
        """
        Validate the configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # Clear any previous errors
        self.errors = []
        
        # Schema validation
        schema_errors = self.schema_validator.validate(self.config)
        self.errors.extend(schema_errors)
        
        # Skip domain validation if schema validation failed
        if not schema_errors:
            domain_errors = self.domain_validator.validate()
            self.errors.extend(domain_errors)
        
        return len(self.errors) == 0 