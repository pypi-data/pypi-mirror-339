import unittest
import uuid
from flatforge.rules.validation import GuidValidationRule
from flatforge.core import FieldValue, Field, ParsedRecord, Section, Record, SectionType

class TestGuidValidation(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.field = Field("guid", 0, length=36)
        self.record = Record("test_record", [self.field])
        self.section = Section("test_section", SectionType.BODY, self.record)

    def test_valid_guids(self):
        """Test validation of valid GUIDs."""
        config = {
            'field': 'guid',
            'strip_spaces': True,
            'strip_hyphens': True,
            'error_message': "Invalid GUID format"
        }
        rule = GuidValidationRule("guid", config)
        
        # Valid GUIDs in different formats
        valid_guids = [
            str(uuid.uuid4()),  # Standard format
            str(uuid.uuid4()).replace('-', ''),  # No hyphens
            str(uuid.uuid4()).upper(),  # Uppercase
            str(uuid.uuid4()).replace('-', ' '),  # Spaces instead of hyphens
            '{' + str(uuid.uuid4()) + '}',  # Curly braces
            '(' + str(uuid.uuid4()) + ')',  # Parentheses
            'urn:uuid:' + str(uuid.uuid4())  # URN format
        ]
        
        for guid in valid_guids:
            field_value = FieldValue(self.field, guid)
            record = ParsedRecord(
                section=self.section,
                record_number=1,
                field_values={"guid": field_value},
                raw_data=""
            )
            is_valid, error = rule.validate(record)
            self.assertTrue(is_valid, f"Failed for {guid}: {error}")
            
    def test_invalid_guids(self):
        """Test validation of invalid GUIDs."""
        config = {
            'field': 'guid',
            'strip_spaces': True,
            'strip_hyphens': True,
            'error_message': "Invalid GUID format"
        }
        rule = GuidValidationRule("guid", config)
        
        # Invalid GUIDs
        invalid_guids = [
            'not-a-guid',  # Invalid format
            '12345678-1234-1234-1234-1234567890123',  # Too long
            '12345678-1234-1234-1234-12345678901',  # Too short
            '12345678-1234-1234-1234-12345678901g',  # Invalid character
            '12345678-1234-1234-1234-12345678901-',  # Extra hyphen
            '12345678-1234-1234-1234-12345678901 ',  # Extra space
            '12345678-1234-1234-1234-12345678901}',  # Unmatched brace
            '12345678-1234-1234-1234-12345678901)',  # Unmatched parenthesis
            'urn:uuid:12345678-1234-1234-1234-12345678901g'  # Invalid URN
        ]
        
        for guid in invalid_guids:
            field_value = FieldValue(self.field, guid)
            record = ParsedRecord(
                section=self.section,
                record_number=1,
                field_values={"guid": field_value},
                raw_data=""
            )
            is_valid, error = rule.validate(record)
            self.assertFalse(is_valid, f"Should fail for {guid}")
            self.assertIn("Invalid GUID format", error)
            
    def test_missing_column(self):
        """Test handling of missing column."""
        config = {
            'field': 'guid',
            'strip_spaces': True,
            'strip_hyphens': True,
            'error_message': "Invalid GUID format"
        }
        rule = GuidValidationRule("guid", config)
        
        other_field = Field("other_field", 0, length=36)
        field_value = FieldValue(other_field, "value")
        record = ParsedRecord(
            section=self.section,
            record_number=1,
            field_values={"other_field": field_value},
            raw_data=""
        )
        is_valid, error = rule.validate(record)
        self.assertFalse(is_valid)
        self.assertIn("Field guid not found", error)
        
    def test_empty_value(self):
        """Test handling of empty value."""
        config = {
            'field': 'guid',
            'strip_spaces': True,
            'strip_hyphens': True,
            'error_message': "Invalid GUID format"
        }
        rule = GuidValidationRule("guid", config)
        
        field_value = FieldValue(self.field, "")
        record = ParsedRecord(
            section=self.section,
            record_number=1,
            field_values={"guid": field_value},
            raw_data=""
        )
        is_valid, error = rule.validate(record)
        self.assertFalse(is_valid)
        self.assertIn("Invalid GUID/UUID format", error) 