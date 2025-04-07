import unittest
import hashlib
from flatforge.rules.global_rules import ChecksumRule
from flatforge.core import ParsedRecord, Field, FieldValue, Section, SectionType, Record

class TestChecksumValidation(unittest.TestCase):
    def setUp(self):
        """Set up common test fixtures."""
        # Create a dummy record for the section
        fields = [Field(name="test_field", position=0, length=10)]
        dummy_record = Record(name="TestRecord", fields=fields)
        
        # Create a section with the required record parameter
        # Include both start_line and end_line for backward compatibility
        self.section = Section(
            name="TestSection", 
            type=SectionType.BODY,
            record=dummy_record,
            start_line=1,
            end_line=100
        )
        
    def create_parsed_record(self, field_values):
        """Helper method to create a ParsedRecord with given field values."""
        # Create field value objects
        field_value_objects = {}
        raw_data = ""
        
        for field_name, value in field_values.items():
            field = Field(name=field_name, position=0, length=len(str(value)))
            field_value = FieldValue(field=field, value=str(value))
            field_value_objects[field_name] = field_value
            raw_data += str(value)
        
        record = ParsedRecord(
            section=self.section, 
            record_number=1,
            field_values=field_value_objects,
            raw_data=raw_data
        )
        return record
        
    def test_single_column_checksum_md5(self):
        """Test single-column MD5 checksum."""
        params = {
            'field': 'data_field',
            'checksum_field': 'checksum_field',
            'type': 'md5'
        }
        rule = ChecksumRule(name="test_md5_checksum", params=params)
        
        # Create test record with data for MD5 checksum
        test_value = "test_data"
        record = self.create_parsed_record({
            'data_field': test_value,
            'checksum_field': ''
        })
        
        # Process the record
        rule.process_record(record)
        
        # Get the calculated checksum
        expected_checksum = hashlib.md5(test_value.encode()).hexdigest()
        actual_checksum = rule.calculate_value()
        
        self.assertEqual(expected_checksum, actual_checksum)
    
    def test_single_column_checksum_sum(self):
        """Test single-column sum checksum."""
        params = {
            'field': 'data_field',
            'checksum_field': 'checksum_field',
            'type': 'sum'
        }
        rule = ChecksumRule(name="test_sum_checksum", params=params)
        
        # Create test record
        test_value = "ABC"  # ASCII values: A=65, B=66, C=67
        record = self.create_parsed_record({
            'data_field': test_value,
            'checksum_field': ''
        })
        
        # Process the record
        rule.process_record(record)
        
        # Calculate expected sum: 65 + 66 + 67 = 198
        expected_checksum = 65 + 66 + 67
        actual_checksum = rule.calculate_value()
        
        self.assertEqual(expected_checksum, actual_checksum)
    
    def test_single_column_checksum_xor(self):
        """Test single-column XOR checksum."""
        params = {
            'field': 'data_field',
            'checksum_field': 'checksum_field',
            'type': 'xor'
        }
        rule = ChecksumRule(name="test_xor_checksum", params=params)
        
        # Create test record
        test_value = "ABC"  # ASCII values: A=65, B=66, C=67
        record = self.create_parsed_record({
            'data_field': test_value,
            'checksum_field': ''
        })
        
        # Process the record
        rule.process_record(record)
        
        # Calculate expected XOR: 65 ^ 66 ^ 67 = 68
        expected_checksum = 65 ^ 66 ^ 67
        actual_checksum = rule.calculate_value()
        
        self.assertEqual(expected_checksum, actual_checksum)
    
    def test_single_column_checksum_mod10(self):
        """Test single-column mod10 checksum."""
        params = {
            'field': 'data_field',
            'checksum_field': 'checksum_field',
            'type': 'mod10'
        }
        rule = ChecksumRule(name="test_mod10_checksum", params=params)
        
        # Create test record
        test_value = "12345"  # Sum of digits: 1+2+3+4+5 = 15, 15 % 10 = 5
        record = self.create_parsed_record({
            'data_field': test_value,
            'checksum_field': ''
        })
        
        # Process the record
        rule.process_record(record)
        
        # Expected modulo 10 checksum: (1+2+3+4+5) % 10 = 5
        expected_checksum = 5
        actual_checksum = rule.calculate_value()
        
        self.assertEqual(expected_checksum, actual_checksum)
    
    def test_single_column_checksum_sha256(self):
        """Test single-column SHA256 checksum using the algorithm parameter."""
        params = {
            'field': 'data_field',
            'checksum_field': 'checksum_field',
            'algorithm': 'SHA256'
        }
        rule = ChecksumRule(name="test_sha256_checksum", params=params)
        
        # Create test record
        test_value = "test_data"
        record = self.create_parsed_record({
            'data_field': test_value,
            'checksum_field': ''
        })
        
        # Process the record
        rule.process_record(record)
        
        # Get the calculated checksum
        expected_checksum = hashlib.sha256(test_value.encode()).hexdigest()
        actual_checksum = rule.calculate_value()
        
        self.assertEqual(expected_checksum, actual_checksum)
        
    def test_multi_column_checksum(self):
        """Test checksum validation across multiple columns."""
        params = {
            'validation_type': 'multi_column',
            'columns': ['field1', 'field2'],
            'target_field': 'checksum_field',
            'algorithm': 'MD5'
        }
        rule = ChecksumRule(name="test_multi_column_checksum", params=params)
        
        # Create test record
        record = self.create_parsed_record({
            'field1': 'value1',
            'field2': 'value2',
            'checksum_field': ''
        })
        
        # Process the record
        rule.process_record(record)
        
        # Calculate expected checksum
        combined_value = "value1value2"
        expected_checksum = hashlib.md5(combined_value.encode()).hexdigest()
        actual_checksum = rule.calculate_value()
        
        self.assertEqual(expected_checksum, actual_checksum)
        
    def test_row_checksum(self):
        """Test checksum validation for entire row."""
        params = {
            'validation_type': 'row',
            'target_field': 'row_checksum',
            'algorithm': 'SHA256'
        }
        rule = ChecksumRule(name="test_row_checksum", params=params)
        
        # Create test record
        record = self.create_parsed_record({
            'field1': 'value1',
            'field2': 'value2',
            'field3': '123',
            'row_checksum': ''
        })
        
        # Process the record
        rule.process_record(record)
        
        # Since we're testing row checksum, we need to manually calculate the expected result
        # This should match the logic in the _process_row method
        row_data = "{'field1': 'value1', 'field2': 'value2', 'field3': '123'}"
        expected_checksum = hashlib.sha256(row_data.encode()).hexdigest()
        actual_checksum = rule.calculate_value()
        
        self.assertEqual(expected_checksum, actual_checksum)
        
    def test_checksum_validation_with_expected_value(self):
        """Test validation of a checksum against an expected value."""
        params = {
            'field': 'data_field',
            'type': 'md5',
            'expected_checksum': hashlib.md5("test_data".encode()).hexdigest()
        }
        rule = ChecksumRule(name="test_checksum_validation", params=params)
        
        # Create test record
        record = self.create_parsed_record({
            'data_field': 'test_data'
        })
        
        # Process the record
        rule.process_record(record)
        
        # Finalize and check for errors
        errors = rule.finalize()
        self.assertEqual(0, len(errors))
        
    def test_checksum_validation_error(self):
        """Test validation error when checksum doesn't match."""
        params = {
            'field': 'data_field',
            'type': 'md5',
            'expected_checksum': 'wrong_checksum'
        }
        rule = ChecksumRule(name="test_checksum_validation_error", params=params)
        
        # Create test record
        record = self.create_parsed_record({
            'data_field': 'test_data'
        })
        
        # Process the record
        rule.process_record(record)
        
        # Finalize and check for errors
        errors = rule.finalize()
        self.assertEqual(1, len(errors))
        self.assertEqual("CHECKSUM_MISMATCH", errors[0].error_code) 