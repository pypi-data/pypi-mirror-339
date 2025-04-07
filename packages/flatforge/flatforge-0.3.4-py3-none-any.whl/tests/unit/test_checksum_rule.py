"""
Unit tests for the ChecksumRule class.
"""
import unittest
from flatforge.rules.global_rules import ChecksumRule
from flatforge.core import ParsedRecord, Section, FieldValue, Field, SectionType, Record

class TestChecksumRule(unittest.TestCase):
    def setUp(self):
        # Create field definitions
        self.field1 = Field(
            name="field1",
            position=0,
            length=None,
            rules=[]
        )
        self.field2 = Field(
            name="field2",
            position=1,
            length=None,
            rules=[]
        )
        self.checksum_field = Field(
            name="checksum",
            position=2,
            length=None,
            rules=[]
        )
        
        # Create record format
        self.record = Record(
            name="test_record",
            fields=[self.field1, self.field2, self.checksum_field]
        )
        
        # Create a test section
        self.section = Section(
            name="test_section",
            type=SectionType.BODY,
            record=self.record,
            min_records=1,
            max_records=None
        )
        
        # Create test records
        self.records = [
            ParsedRecord(
                section=self.section,
                record_number=1,
                field_values={
                    "field1": FieldValue(field=self.field1, value="123"),
                    "field2": FieldValue(field=self.field2, value="456"),
                    "checksum": FieldValue(field=self.checksum_field, value="")
                },
                raw_data="123,456,"
            ),
            ParsedRecord(
                section=self.section,
                record_number=2,
                field_values={
                    "field1": FieldValue(field=self.field1, value="789"),
                    "field2": FieldValue(field=self.field2, value="012"),
                    "checksum": FieldValue(field=self.checksum_field, value="")
                },
                raw_data="789,012,"
            )
        ]
    
    def test_validation_mode(self):
        """Test checksum validation mode."""
        rule = ChecksumRule("test_rule", {
            "mode": "validate",
            "validation_type": "multi_column",
            "columns": ["field1", "field2"],
            "algorithm": "SHA256",
            "expected_checksum": "a1b2c3d4"  # Example checksum
        })
        
        # Process records
        for record in self.records:
            rule.process_record(record)
        
        # Finalize and check for validation errors
        errors = rule.finalize()
        self.assertIsInstance(errors, list)
        self.assertGreater(len(errors), 0)  # Should have errors since checksum won't match
    
    def test_population_mode(self):
        """Test checksum population mode."""
        rule = ChecksumRule("test_rule", {
            "mode": "populate",
            "validation_type": "multi_column",
            "columns": ["field1", "field2"],
            "algorithm": "SHA256"
        })
        
        # Process records
        for record in self.records:
            rule.process_record(record)
        
        # Finalize to calculate checksum
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Get calculated checksum
        checksum = rule.get_calculated_checksum()
        self.assertIsNotNone(checksum)
        self.assertIsInstance(checksum, str)
        
        # Verify the checksum is a valid SHA256 hash (64 characters)
        self.assertEqual(len(checksum), 64)
    
    def test_numeric_checksum_population(self):
        """Test numeric checksum population mode."""
        rule = ChecksumRule("test_rule", {
            "mode": "populate",
            "validation_type": "multi_column",
            "columns": ["field1", "field2"],
            "type": "sum"  # Using sum algorithm for numeric checksum
        })
        
        # Process records
        for record in self.records:
            rule.process_record(record)
        
        # Finalize to calculate checksum
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Get calculated checksum
        checksum = rule.get_calculated_checksum()
        print(f"NUMERIC CHECKSUM: {checksum}, TYPE: {type(checksum)}")
        self.assertIsNotNone(checksum)
        self.assertIsInstance(checksum, int)
        
        # Verify the checksum is the sum of ASCII values
        expected_sum = sum(ord(c) for c in "123456") + sum(ord(c) for c in "789012")
        self.assertEqual(checksum, expected_sum)
    
    def test_invalid_mode(self):
        """Test behavior with invalid mode."""
        rule = ChecksumRule("test_rule", {
            "mode": "invalid_mode",  # Invalid mode
            "validation_type": "multi_column",
            "columns": ["field1", "field2"],
            "algorithm": "SHA256"
        })
        
        # Process records
        for record in self.records:
            rule.process_record(record)
        
        # Finalize should default to validation mode
        errors = rule.finalize()
        self.assertIsInstance(errors, list)
        
        # No checksum should be available
        checksum = rule.get_calculated_checksum()
        self.assertIsNone(checksum)
    
    def test_mod5_checksum_population(self):
        """Test mod5 checksum population mode."""
        rule = ChecksumRule("test_rule", {
            "mode": "populate",
            "validation_type": "multi_column",
            "columns": ["field1", "field2"],
            "type": "mod5"  # Using mod5 algorithm
        })
        
        print(f"Initial rule.type: {rule.type}")
        
        # Process records
        for record in self.records:
            rule.process_record(record)
        
        # Finalize to calculate checksum
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Get calculated checksum
        checksum = rule.get_calculated_checksum()
        print(f"MOD5 CHECKSUM: {checksum}, TYPE: {type(checksum)}")
        self.assertIsNotNone(checksum)
        self.assertIsInstance(checksum, int)
        
        # Verify the checksum is modulo 5
        self.assertLess(checksum, 5)
        
        # Verify the checksum calculation
        # For "123456" + "789012":
        # Sum of digits = (1+2+3+4+5+6) + (7+8+9+0+1+2) = 21 + 27 = 48
        # 48 % 5 = 3
        self.assertEqual(checksum, 3)
    
    def test_mod5_validation(self):
        """Test mod5 checksum validation mode."""
        rule = ChecksumRule("test_rule", {
            "mode": "validate",
            "validation_type": "multi_column",
            "columns": ["field1", "field2"],
            "type": "mod5",
            "expected_checksum": 3  # Expected mod5 checksum for our test data (as integer)
        })
        
        # Process records
        for record in self.records:
            rule.process_record(record)
        
        # Print diagnostic information
        print(f"MOD5 VALIDATION rule.type: {rule.type}")
        print(f"MOD5 VALIDATION rule.state['checksum']: {rule.state['checksum']}")
        print(f"MOD5 VALIDATION rule.expected_checksum: {rule.expected_checksum}")
        
        # Finalize and check for validation errors
        errors = rule.finalize()
        if errors:
            print(f"MOD5 VALIDATION errors: {errors}")
        self.assertEqual(len(errors), 0)  # Should match expected checksum
    
    def test_mod5_validation_failure(self):
        """Test mod5 checksum validation mode with incorrect expected value."""
        rule = ChecksumRule("test_rule", {
            "mode": "validate",
            "validation_type": "multi_column",
            "columns": ["field1", "field2"],
            "type": "mod5",
            "expected_checksum": "4"  # Incorrect expected checksum
        })
        
        # Process records
        for record in self.records:
            rule.process_record(record)
        
        # Finalize and check for validation errors
        errors = rule.finalize()
        self.assertGreater(len(errors), 0)  # Should have errors since checksum won't match

if __name__ == '__main__':
    unittest.main() 