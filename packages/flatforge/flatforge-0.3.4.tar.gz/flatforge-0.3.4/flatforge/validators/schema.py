"""
Schema validator module for FlatForge.

This module contains the schema validator class used to validate 
configuration files against a JSON schema.
"""
from pathlib import Path
import json
import jsonschema
from typing import Dict, List, Any, Optional


class SchemaValidator:
    """
    Schema validator for FlatForge configuration files.
    
    This class validates a configuration against a JSON schema.
    """
    
    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize a schema validator.
        
        Args:
            schema_path: Path to a custom JSON schema file.
                         If not provided, the default schema is used.
        """
        if schema_path is None:
            schema_path = Path(__file__).parent / "schemas" / "config_schema.json"
        
        with open(schema_path, "r") as f:
            self.schema = json.load(f)
    
    def validate(self, config: Dict[str, Any]) -> List[str]:
        """
        Validate a configuration against the JSON schema.
        
        Args:
            config: The configuration to validate
            
        Returns:
            A list of error messages, or an empty list if validation succeeds
        """
        errors = []
        try:
            jsonschema.validate(config, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            # Format the error message nicely
            path = ".".join(str(p) for p in e.path) if e.path else "root"
            errors.append(f"Schema error at {path}: {e.message}")
        except Exception as e:
            # Catch any other validation errors
            errors.append(f"Schema validation error: {str(e)}")
            
        return errors
