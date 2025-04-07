import unittest
import json
import tempfile
import os
import yaml
from pathlib import Path
from typing import Dict, Any

from flatforge.validators import SchemaValidator, DomainValidator, ConfigValidator


class TestSchemaValidator(unittest.TestCase):
    """Test the SchemaValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Valid configuration
        self.valid_config = {
            "name": "Test Config",
            "type": "delimited",
            "delimiter": ",",
            "sections": [
                {
                    "name": "body",
                    "type": "body",
                    "record": {
                        "name": "body_record",
                        "fields": [
                            {
                                "name": "field1",
                                "position": 0
                            }
                        ]
                    }
                }
            ]
        }
        
        # Create a temporary schema file for testing
        fd, self.temp_schema_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        self.temp_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["name", "type"],
            "properties": {
                "name": {"type": "string"},
                "type": {"type": "string", "enum": ["custom_type"]}
            }
        }
        with open(self.temp_schema_path, 'w') as f:
            json.dump(self.temp_schema, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        try:
            if os.path.exists(self.temp_schema_path):
                os.unlink(self.temp_schema_path)
        except Exception as e:
            print(f"Error cleaning up temp file: {e}")
    
    def test_validate_valid_config(self):
        """Test validation of a valid configuration."""
        validator = SchemaValidator()
        errors = validator.validate(self.valid_config)
        self.assertEqual(len(errors), 0, "Valid configuration should not have errors")
    
    def test_validate_missing_required_property(self):
        """Test validation of a configuration with a missing required property."""
        # Remove 'name' which is required
        invalid_config = self.valid_config.copy()
        del invalid_config["name"]
        
        validator = SchemaValidator()
        errors = validator.validate(invalid_config)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("'name' is a required property" in err for err in errors))
    
    def test_validate_invalid_enum_value(self):
        """Test validation of a configuration with an invalid enum value."""
        # Use an invalid value for 'type'
        invalid_config = self.valid_config.copy()
        invalid_config["type"] = "invalid_type"
        
        validator = SchemaValidator()
        errors = validator.validate(invalid_config)
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("'invalid_type' is not one of" in err for err in errors))
    
    def test_validate_with_custom_schema(self):
        """Test validation with a custom schema."""
        # This config is valid against our custom schema but not the default schema
        config = {
            "name": "Test Config",
            "type": "custom_type"
        }
        
        validator = SchemaValidator(self.temp_schema_path)
        errors = validator.validate(config)
        self.assertEqual(len(errors), 0, "Should be valid against custom schema")
        
        # But it should fail against the default schema
        default_validator = SchemaValidator()
        errors = default_validator.validate(config)
        self.assertGreaterEqual(len(errors), 1)


class TestDomainValidator(unittest.TestCase):
    """Test the DomainValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Base valid configuration
        self.base_config = {
            "name": "Test Config",
            "type": "fixed_length",
            "sections": [
                {
                    "name": "body",
                    "type": "body",
                    "record": {
                        "name": "body_record",
                        "fields": [
                            {
                                "name": "field1",
                                "position": 0,
                                "length": 5
                            },
                            {
                                "name": "field2",
                                "position": 5,
                                "length": 5
                            }
                        ]
                    }
                }
            ]
        }
    
    def test_validate_valid_config(self):
        """Test validation of a valid configuration."""
        validator = DomainValidator(self.base_config)
        errors = validator.validate()
        self.assertEqual(len(errors), 0, "Valid configuration should not have errors")
    
    def test_validate_field_positions(self):
        """Test validation of field positions in fixed-length format."""
        # Create a configuration with overlapping fields
        config = self.base_config.copy()
        config["sections"][0]["record"]["fields"].append({
            "name": "field3",
            "position": 3,  # Overlaps with field1
            "length": 5
        })
        
        validator = DomainValidator(config)
        errors = validator.validate()
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("overlaps with" in err for err in errors))
    
    def test_validate_section_constraints(self):
        """Test validation of section constraints."""
        # Create a configuration with min_records > max_records
        config = self.base_config.copy()
        config["sections"][0]["min_records"] = 5
        config["sections"][0]["max_records"] = 3
        
        validator = DomainValidator(config)
        errors = validator.validate()
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("min_records (5) > max_records (3)" in err for err in errors))
    
    def test_validate_duplicate_field_names(self):
        """Test validation of duplicate field names."""
        # Create a configuration with duplicate field names
        config = self.base_config.copy()
        config["sections"][0]["record"]["fields"].append({
            "name": "field1",  # Duplicate name
            "position": 10,
            "length": 5
        })
        
        validator = DomainValidator(config)
        errors = validator.validate()
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("Duplicate field name" in err for err in errors))
    
    def test_validate_rule_references(self):
        """Test validation of rule references."""
        # Create a configuration with an invalid rule type
        config = self.base_config.copy()
        config["sections"][0]["record"]["fields"][0]["rules"] = [
            {"type": "invalid_rule"}
        ]
        
        validator = DomainValidator(config)
        errors = validator.validate()
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("Invalid rule type" in err for err in errors))
    
    def test_validate_string_length_rule(self):
        """Test validation of string_length rule parameters."""
        # Create a configuration with min_length > max_length
        config = self.base_config.copy()
        config["sections"][0]["record"]["fields"][0]["rules"] = [
            {
                "type": "string_length", 
                "params": {
                    "min_length": 10,
                    "max_length": 5
                }
            }
        ]
        
        validator = DomainValidator(config)
        errors = validator.validate()
        self.assertGreaterEqual(len(errors), 1)
        self.assertTrue(any("min_length (10) > max_length (5)" in err for err in errors))
    
    def test_validate_global_rules(self):
        """Test validation of global rules."""
        # Create a configuration with a global rule referencing a non-existent field
        config = self.base_config.copy()
        config["global_rules"] = [
            {
                "type": "sum",
                "params": {
                    "section": "body",
                    "field": "amount",
                    "target_field": "footer.total"
                }
            }
        ]
        
        validator = DomainValidator(config)
        errors = validator.validate()
        self.assertGreaterEqual(len(errors), 1)
        # We should have both a missing section error and a non-existent field error


class TestConfigValidator(unittest.TestCase):
    """Test the ConfigValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary config files for testing
        fd, self.valid_config_path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        
        fd, self.invalid_config_path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        
        fd, self.temp_schema_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        
        # Valid configuration
        self.valid_config = {
            "name": "Test Config",
            "type": "delimited",
            "delimiter": ",",
            "sections": [
                {
                    "name": "body",
                    "type": "body",
                    "record": {
                        "name": "body_record",
                        "fields": [
                            {
                                "name": "field1",
                                "position": 0
                            }
                        ]
                    }
                }
            ]
        }
        
        # Invalid configuration (invalid type)
        self.invalid_config = {
            "name": "Test Config",
            "type": "invalid_type",
            "sections": []
        }
        
        # Save configurations to files
        with open(self.valid_config_path, 'w') as f:
            yaml.dump(self.valid_config, f)
        
        with open(self.invalid_config_path, 'w') as f:
            yaml.dump(self.invalid_config, f)
        
        # Custom schema
        self.custom_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["name", "type"],
            "properties": {
                "name": {"type": "string"},
                "type": {"type": "string", "enum": ["custom_type"]}
            }
        }
        
        with open(self.temp_schema_path, 'w') as f:
            json.dump(self.custom_schema, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        try:
            for path in [self.valid_config_path, self.invalid_config_path, self.temp_schema_path]:
                if os.path.exists(path):
                    os.unlink(path)
        except Exception as e:
            print(f"Error cleaning up temp file: {e}")
    
    def test_from_file_yaml(self):
        """Test loading a configuration from a YAML file."""
        validator = ConfigValidator.from_file(self.valid_config_path)
        self.assertEqual(validator.config, self.valid_config)
    
    def test_from_file_json(self):
        """Test loading a configuration from a JSON file."""
        # Create a JSON file
        fd, json_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        
        try:
            with open(json_path, 'w') as f:
                json.dump(self.valid_config, f)
            
            validator = ConfigValidator.from_file(json_path)
            self.assertEqual(validator.config, self.valid_config)
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)
    
    def test_from_file_not_found(self):
        """Test loading a configuration from a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            ConfigValidator.from_file("non_existent_file.yaml")
    
    def test_from_file_invalid_format(self):
        """Test loading a configuration from a file with an unsupported format."""
        # Create a file with an unsupported extension
        fd, invalid_format_path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        
        try:
            with open(invalid_format_path, 'w') as f:
                f.write("not a valid config")
            
            with self.assertRaises(ValueError):
                ConfigValidator.from_file(invalid_format_path)
        finally:
            if os.path.exists(invalid_format_path):
                os.unlink(invalid_format_path)
    
    def test_validate_valid_config(self):
        """Test validation of a valid configuration."""
        validator = ConfigValidator(self.valid_config)
        is_valid = validator.validate()
        self.assertTrue(is_valid)
        self.assertEqual(len(validator.errors), 0)
    
    def test_validate_invalid_config(self):
        """Test validation of an invalid configuration."""
        validator = ConfigValidator(self.invalid_config)
        is_valid = validator.validate()
        self.assertFalse(is_valid)
        self.assertGreaterEqual(len(validator.errors), 1)
    
    def test_validate_with_custom_schema(self):
        """Test validation with a custom schema."""
        # Test just the schema validation, not domain validation
        # Create a fresh custom schema file
        if os.path.exists(self.temp_schema_path):
            os.unlink(self.temp_schema_path)
            
        # Define a custom schema for testing
        custom_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["name", "type"],
            "properties": {
                "name": {"type": "string"},
                "type": {"type": "string", "enum": ["custom_type"]}
            }
        }
        
        # Write schema to file
        with open(self.temp_schema_path, 'w') as f:
            json.dump(custom_schema, f)
        
        # Create a simple config that matches the custom schema
        config = {
            "name": "Test Config",
            "type": "custom_type"
        }
        
        # Test with SchemaValidator directly
        schema_validator = SchemaValidator(self.temp_schema_path)
        errors = schema_validator.validate(config)
        self.assertEqual(len(errors), 0, "Schema validation should pass with custom schema")
        
        # Test with default schema - this should fail since custom_type is not allowed
        default_validator = SchemaValidator()
        errors = default_validator.validate(config)
        self.assertGreaterEqual(len(errors), 1, "Default schema should reject custom_type")
        
        # Now test that ConfigValidator's schema validation uses the custom schema correctly
        # But use a complete config that will pass domain validation
        complete_config = {
            "name": "Complete Config",
            "type": "custom_type",
            "sections": [
                {
                    "name": "body",
                    "type": "body",
                    "record": {
                        "name": "record",
                        "fields": [
                            {
                                "name": "field1",
                                "position": 0
                            }
                        ]
                    }
                }
            ]
        }
        
        # Update the schema to be more permissive for complete testing
        complete_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["name", "type"],
            "properties": {
                "name": {"type": "string"},
                "type": {"type": "string"},
                "sections": {"type": "array"}
            }
        }
        
        with open(self.temp_schema_path, 'w') as f:
            json.dump(complete_schema, f)
            
        # Now test with ConfigValidator
        validator = ConfigValidator(complete_config, schema_path=self.temp_schema_path)
        is_valid = validator.validate()
        if not is_valid:
            print(f"ConfigValidator errors: {validator.errors}")
            
        self.assertTrue(is_valid, "Validation should pass with custom schema and complete config")


if __name__ == '__main__':
    unittest.main() 