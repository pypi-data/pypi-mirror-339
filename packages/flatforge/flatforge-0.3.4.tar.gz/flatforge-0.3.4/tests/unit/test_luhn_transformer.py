"""
Test the Luhn transformer.
"""
import unittest
from flatforge.core import FieldValue, Field, ParsedRecord, Section, Record, SectionType
from flatforge.transformers.luhn import LuhnTransformer


class TestLuhnTransformer(unittest.TestCase):
    """Test cases for the Luhn transformer."""

    def setUp(self):
        """Set up test cases."""
        self.transformer = LuhnTransformer("luhn", {})
        self.field = Field("test_field", 0, length=10)
        self.record = Record("test_record", [self.field])
        self.section = Section("test_section", SectionType.BODY, self.record)
        self.field_value = FieldValue(self.field, "")
        self.record = ParsedRecord(
            section=self.section,
            record_number=1,
            field_values={"test_field": self.field_value},
            raw_data=""
        )

    def test_empty_string(self):
        """Test transformation of an empty string."""
        self.field_value.value = ""
        self.transformer.apply(self.field_value, self.record)
        self.assertEqual(self.field_value.transformed_value, "")

    def test_non_numeric_string(self):
        """Test transformation of a non-numeric string."""
        self.field_value.value = "abc"
        self.transformer.apply(self.field_value, self.record)
        self.assertEqual(self.field_value.transformed_value, "abc")

    def test_numeric_string(self):
        """Test transformation of a numeric string."""
        self.field_value.value = "123"
        self.transformer.apply(self.field_value, self.record)
        self.assertEqual(self.field_value.transformed_value, "1232")

    def test_single_digit(self):
        """Test transformation of a single digit."""
        self.field_value.value = "5"
        self.transformer.apply(self.field_value, self.record)
        self.assertEqual(self.field_value.transformed_value, "55")

    def test_valid_card_number(self):
        """Test transformation of a valid card number."""
        self.field_value.value = "4532015112830366"
        self.transformer.apply(self.field_value, self.record)
        self.assertEqual(self.field_value.transformed_value, "4532015112830366")

    def test_verify_luhn(self):
        """Test that the transformed number is a valid Luhn number."""
        self.field_value.value = "4532015112830366"
        self.transformer.apply(self.field_value, self.record)
        # Calculate checksum according to Luhn algorithm
        digits = [int(d) for d in self.field_value.transformed_value]
        checksum = sum(digits[-1::-2]) + sum(sum(divmod(2 * d, 10)) for d in digits[-2::-2])
        self.assertEqual(checksum % 10, 0)

    def test_with_dashes(self):
        """Test transformation of a number with dashes."""
        self.field_value.value = "4532-0151-1283-0366"
        self.transformer.apply(self.field_value, self.record)
        self.assertEqual(self.field_value.transformed_value, "4532-0151-1283-0366")

    def test_with_spaces(self):
        """Test transformation of a number with spaces."""
        self.field_value.value = "4532 0151 1283 0366"
        self.transformer.apply(self.field_value, self.record)
        self.assertEqual(self.field_value.transformed_value, "4532 0151 1283 0366")


if __name__ == '__main__':
    unittest.main() 