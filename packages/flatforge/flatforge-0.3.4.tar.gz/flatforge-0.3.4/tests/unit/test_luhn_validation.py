import unittest
from flatforge.rules.validation import LuhnValidationRule

class TestLuhnValidation(unittest.TestCase):
    def test_valid_card_number(self):
        """Test validation of a valid card number."""
        config = {'column': 'card_number'}
        rule = LuhnValidationRule(config)
        
        # Valid test card numbers
        valid_numbers = [
            '4111111111111111',  # Visa
            '5500000000000004',  # Mastercard
            '340000000000009',   # Amex
            '6011000000000004'   # Discover
        ]
        
        for number in valid_numbers:
            record = {'card_number': number}
            is_valid, error = rule.validate(record)
            self.assertTrue(is_valid, f"Failed for {number}")
            self.assertIsNone(error)
            
    def test_invalid_card_number(self):
        """Test validation of an invalid card number."""
        config = {'column': 'card_number'}
        rule = LuhnValidationRule(config)
        
        # Invalid card numbers (changed last digit)
        invalid_numbers = [
            '4111111111111112',
            '5500000000000005',
            '340000000000001',
            '6011000000000003'
        ]
        
        for number in invalid_numbers:
            record = {'card_number': number}
            is_valid, error = rule.validate(record)
            self.assertFalse(is_valid, f"Should fail for {number}")
            self.assertIsNotNone(error)
            
    def test_formatting_options(self):
        """Test card number with spaces and hyphens."""
        # Card with spaces and hyphens
        formatted_number = '4111-1111 1111-1111'
        
        # Test with stripping enabled (default)
        config = {'column': 'card_number'}
        rule = LuhnValidationRule(config)
        
        record = {'card_number': formatted_number}
        is_valid, error = rule.validate(record)
        self.assertTrue(is_valid)
        
        # Test with stripping disabled
        config = {
            'column': 'card_number',
            'strip_spaces': False,
            'strip_hyphens': False
        }
        rule = LuhnValidationRule(config)
        
        record = {'card_number': formatted_number}
        is_valid, error = rule.validate(record)
        self.assertFalse(is_valid)  # Should fail with formatting 