import unittest
import os
import json
import tempfile
from flatforge.rules.transformation import ValueResolverTransformationRule

class TestValueResolver(unittest.TestCase):
    def setUp(self):
        """Create a temporary mapping file for testing."""
        self.mapping = {
            "A": "Active",
            "I": "Inactive",
            "P": "Pending",
            "C": "Completed"
        }
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        json.dump(self.mapping, self.temp_file)
        self.temp_file.close()
        
    def tearDown(self):
        """Remove temporary file."""
        os.unlink(self.temp_file.name)
        
    def test_basic_resolution(self):
        """Test basic value resolution."""
        config = {
            'source_field': 'status_code',
            'target_field': 'status_name',
            'mapping_file': self.temp_file.name
        }
        rule = ValueResolverTransformationRule(config)
        
        record = {'status_code': 'A'}
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(transformed['status_name'], 'Active')
        
    def test_default_value(self):
        """Test default value when mapping not found."""
        config = {
            'source_field': 'status_code',
            'target_field': 'status_name',
            'mapping_file': self.temp_file.name,
            'default_value': 'Unknown'
        }
        rule = ValueResolverTransformationRule(config)
        
        record = {'status_code': 'X'}  # X is not in mapping
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)
        self.assertEqual(transformed['status_name'], 'Unknown')
        
    def test_missing_source_field(self):
        """Test behavior when source field is missing."""
        config = {
            'source_field': 'status_code',
            'target_field': 'status_name',
            'mapping_file': self.temp_file.name
        }
        rule = ValueResolverTransformationRule(config)
        
        record = {'other_field': 'value'}  # No status_code
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)  # Should still succeed with empty value
        self.assertEqual(transformed['status_name'], '')  # Empty default
        
    def test_nonexistent_mapping_file(self):
        """Test behavior with nonexistent mapping file."""
        config = {
            'source_field': 'status_code',
            'target_field': 'status_name',
            'mapping_file': 'nonexistent_file.json',
            'default_value': 'File Error'
        }
        rule = ValueResolverTransformationRule(config)
        
        record = {'status_code': 'A'}
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)  # Should still succeed with default
        self.assertEqual(transformed['status_name'], 'File Error') 