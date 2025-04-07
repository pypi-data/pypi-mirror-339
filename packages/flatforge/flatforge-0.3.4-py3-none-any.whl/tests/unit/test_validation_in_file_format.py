import unittest
import tempfile
import os
import yaml

from flatforge.core import FileFormat, ConfigError


class TestFileFormatWithValidation(unittest.TestCase):
    """Test the FileFormat.from_yaml method with validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary valid config file for testing
        fd, self.valid_config_path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        
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
        with open(self.valid_config_path, 'w') as f:
            yaml.dump(self.valid_config, f)
        
        # Create a temporary invalid config file for testing
        # Use a valid file type but with invalid structure 
        fd, self.invalid_config_path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        
        self.invalid_config = {
            "name": "Invalid Config",
            "type": "fixed_length",  # Valid type but missing required fields
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
                                # Missing required 'length' field for fixed_length format
                            }
                        ]
                    }
                }
            ]
        }
        with open(self.invalid_config_path, 'w') as f:
            yaml.dump(self.invalid_config, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        try:
            for path in [self.valid_config_path, self.invalid_config_path]:
                if os.path.exists(path):
                    os.unlink(path)
        except Exception as e:
            print(f"Error cleaning up temp file: {e}")
    
    def test_from_yaml_without_validation(self):
        """Test loading a configuration without validation."""
        # This should succeed even for a structurally invalid config because validation is off by default
        file_format = FileFormat.from_yaml(self.invalid_config_path)
        self.assertEqual(file_format.name, "Invalid Config")
        self.assertEqual(file_format.type.value, "fixed_length")
    
    def test_from_yaml_with_validation_valid(self):
        """Test loading a valid configuration with validation."""
        # This should succeed because the config is valid
        file_format = FileFormat.from_yaml(self.valid_config_path, validate=True)
        self.assertEqual(file_format.name, "Test Config")
        self.assertEqual(file_format.type.value, "delimited")
    
    def test_from_yaml_with_validation_invalid(self):
        """Test loading an invalid configuration with validation."""
        # This should fail because the config is invalid and validation is enabled
        with self.assertRaises(ConfigError):
            FileFormat.from_yaml(self.invalid_config_path, validate=True)


if __name__ == '__main__':
    unittest.main() 