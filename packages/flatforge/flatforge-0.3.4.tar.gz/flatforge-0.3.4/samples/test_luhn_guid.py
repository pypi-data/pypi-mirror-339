#!/usr/bin/env python3
"""Test script for FlatForge Luhn and GUID validation rules."""

import os
import sys
from datetime import datetime

from flatforge.core.models import Field, FieldValue, ParsedRecord, Record, Section, SectionType
from flatforge.rules.validation.luhn import LuhnRule
from flatforge.rules.validation.guid import GuidRule
from flatforge.core import ValidationError

def print_separator(title):
    """Print a formatted separator with title."""
    print("\n" + "="*80)
    print(f"{title:^80}")
    print("="*80 + "\n")

def test_luhn_rule():
    """Test credit card validation using Luhn algorithm."""
    print_separator("Testing Luhn Rule")
    
    # Create a dummy field
    field = Field(name="card_number", position=0)
    
    # Create a dummy record and section
    record_def = Record(name="test_record", fields=[field])
    section = Section(name="test_section", type=SectionType.BODY, record=record_def)
    
    # Test configuration
    params = {
        'field': 'card_number',
        'strip_spaces': True,
        'strip_hyphens': True,
        'error_message': "Invalid credit card number"
    }
    
    # Create test rule
    rule = LuhnRule("luhn_rule", params)
    
    # Test valid card numbers
    valid_cards = [
        '4532 7153 3790 8241',  # Visa
        '5412 7512 3456 7890',  # Mastercard
        '3782 8224 6310 005',   # American Express
        '6011 0000 0000 0004',  # Discover
        '3530 1113 3330 0000',  # JCB
        '6759 4111 1111 1111'   # Maestro
    ]
    
    print("Testing valid card numbers:")
    for card in valid_cards:
        field_value = FieldValue(field=field, value=card)
        record = ParsedRecord(
            section=section,
            record_number=1,
            field_values={'card_number': field_value},
            raw_data=card
        )
        
        try:
            rule.validate(field_value, record)
            print(f"Card: {card:30} Valid: True")
        except ValidationError as e:
            print(f"Card: {card:30} Valid: False Error: {str(e)}")
        
    # Test invalid card numbers
    invalid_cards = [
        '4532 7153 3790 8242',  # Changed last digit
        '5412 7512 3456 7891',  # Changed last digit
        '3782 8224 6310 006',   # Changed last digit
        '6011 0000 0000 0005',  # Changed last digit
        '3530 1113 3330 0001',  # Changed last digit
        '6759 4111 1111 1112'   # Changed last digit
    ]
    
    print("\nTesting invalid card numbers:")
    for card in invalid_cards:
        field_value = FieldValue(field=field, value=card)
        record = ParsedRecord(
            section=section,
            record_number=1,
            field_values={'card_number': field_value},
            raw_data=card
        )
        
        try:
            rule.validate(field_value, record)
            print(f"Card: {card:30} Valid: True")
        except ValidationError as e:
            print(f"Card: {card:30} Valid: False Error: {str(e)}")

def test_guid_rule():
    """Test GUID validation."""
    print_separator("Testing GUID Rule")
    
    # Create a dummy field
    field = Field(name="guid", position=0)
    
    # Create a dummy record and section
    record_def = Record(name="test_record", fields=[field])
    section = Section(name="test_section", type=SectionType.BODY, record=record_def)
    
    # Test configuration
    params = {
        'field': 'guid',
        'strip_spaces': True,
        'strip_hyphens': True,
        'error_message': "Invalid GUID format"
    }
    
    # Create test rule
    rule = GuidRule("guid_rule", params)
    
    # Test valid GUIDs
    valid_guids = [
        '123e4567-e89b-12d3-a456-426614174000',  # Standard format
        '123e4567e89b12d3a456426614174000',       # No hyphens
        '123E4567-E89B-12D3-A456-426614174000',   # Uppercase
        '123e4567 e89b 12d3 a456 426614174000',   # Spaces instead of hyphens
        '{123e4567-e89b-12d3-a456-426614174000}', # Curly braces
        '(123e4567-e89b-12d3-a456-426614174000)', # Parentheses
        'urn:uuid:123e4567-e89b-12d3-a456-426614174000'  # URN format
    ]
    
    print("Testing valid GUIDs:")
    for guid_str in valid_guids:
        # Create field value and record
        field_value = FieldValue(field=field, value=guid_str)
        record = ParsedRecord(
            section=section,
            record_number=1,
            field_values={'guid': field_value},
            raw_data=guid_str
        )
        
        try:
            rule.validate(field_value, record)
            print(f"GUID: {guid_str:50} Valid: True")
        except ValidationError as e:
            print(f"GUID: {guid_str:50} Valid: False Error: {str(e)}")
        
    # Test invalid GUIDs
    invalid_guids = [
        'not-a-guid',  # Invalid format
        '12345678-1234-1234-1234-1234567890123',  # Too long
        '12345678-1234-1234-1234-12345678901',    # Too short
        '12345678-1234-1234-1234-12345678901g',   # Invalid character
        '12345678-1234-1234-1234-12345678901-',   # Extra hyphen
        '12345678-1234-1234-1234-12345678901 ',   # Extra space
        '12345678-1234-1234-1234-12345678901}',   # Unmatched brace
        '12345678-1234-1234-1234-12345678901)',   # Unmatched parenthesis
        'urn:uuid:12345678-1234-1234-1234-12345678901g'  # Invalid URN
    ]
    
    print("\nTesting invalid GUIDs:")
    for guid_str in invalid_guids:
        # Create field value and record
        field_value = FieldValue(field=field, value=guid_str)
        record = ParsedRecord(
            section=section,
            record_number=1,
            field_values={'guid': field_value},
            raw_data=guid_str
        )
        
        try:
            rule.validate(field_value, record)
            print(f"GUID: {guid_str:50} Valid: True")
        except ValidationError as e:
            print(f"GUID: {guid_str:50} Valid: False Error: {str(e)}")

def main():
    """Run all tests."""
    print(f"FlatForge Validation Rules Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    test_luhn_rule()
    test_guid_rule()
    
    print("\nAll tests completed!")

if __name__ == '__main__':
    main() 