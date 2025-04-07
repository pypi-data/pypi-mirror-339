import unittest
import re
from flatforge.rules.validation import GuidValidationRule
from flatforge.rules.transformation import GenerateGuidTransformationRule

class TestGuidValidation(unittest.TestCase):
    def test_valid_guid(self):
        """Test validation of valid GUIDs."""
        config = {'column': 'transaction_id'}
        rule = GuidValidationRule(config)
        
        valid_guids = [
            '123e4567-e89b-12d3-a456-426614174000',
            'A987FBC9-4BED-3078-CF07-9141BA07C9F3',
            '00000000-0000-0000-0000-000000000000'
        ]
        
        for guid in valid_guids:
            record = {'transaction_id': guid}
            is_valid, error = rule.validate(record)
            self.assertTrue(is_valid, f"Failed for {guid}")
            self.assertIsNone(error)
            
    def test_invalid_guid(self):
        """Test validation of invalid GUIDs."""
        config = {'column': 'transaction_id'}
        rule = GuidValidationRule(config)
        
        invalid_guids = [
            '123e4567-e89b-12d3-a456',  # Too short
            '123e4567-e89b-12d3-a456-426614174000-extra',  # Too long
            '123e4567-e89b-12d3-a456-42661417400G',  # Invalid character
            '123e4567-e89b-12d3-a456_426614174000'   # Wrong format
        ]
        
        for guid in invalid_guids:
            record = {'transaction_id': guid}
            is_valid, error = rule.validate(record)
            self.assertFalse(is_valid, f"Should fail for {guid}")
            self.assertIsNotNone(error)
            
    def test_version_validation(self):
        """Test validation of UUID version."""
        # Version 4 UUID
        v4_uuid = '123e4567-e89b-42d3-a456-426614174000'  # 4 in version position
        
        # Test with correct version
        config = {
            'column': 'transaction_id',
            'version': 4
        }
        rule = GuidValidationRule(config)
        record = {'transaction_id': v4_uuid}
        is_valid, error = rule.validate(record)
        self.assertTrue(is_valid)
        
        # Test with incorrect version
        config = {
            'column': 'transaction_id',
            'version': 1
        }
        rule = GuidValidationRule(config)
        record = {'transaction_id': v4_uuid}
        is_valid, error = rule.validate(record)
        self.assertFalse(is_valid)

class TestGuidGeneration(unittest.TestCase):
    def test_generate_uuid4(self):
        """Test generation of version 4 UUID."""
        config = {
            'target_field': 'transaction_id',
            'version': 4
        }
        rule = GenerateGuidTransformationRule(config)
        
        record = {}
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertIn('transaction_id', transformed)
        
        # Verify format of generated UUID
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        self.assertTrue(re.match(uuid_pattern, transformed['transaction_id'], re.IGNORECASE))
        
    def test_generate_uuid1(self):
        """Test generation of version 1 UUID."""
        config = {
            'target_field': 'transaction_id',
            'version': 1
        }
        rule = GenerateGuidTransformationRule(config)
        
        record = {}
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)
        
        # Verify format of generated UUID (version 1)
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        self.assertTrue(re.match(uuid_pattern, transformed['transaction_id'], re.IGNORECASE)) 