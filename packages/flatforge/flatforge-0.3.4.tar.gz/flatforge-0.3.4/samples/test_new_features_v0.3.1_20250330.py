#!/usr/bin/env python3
"""
Test script for FlatForge v0.3.1 features.

This script demonstrates and tests all the new features in FlatForge v0.3.1:
1. Extended Checksum Validation (Multiple Types: sum, xor, mod10, md5, SHA256)
2. Value Resolver Transformer
3. Luhn Algorithm Validation
4. Card Number Masking
5. Encoding Transformation
6. GUID Validation and Generation

Run this script with:
    python test_new_features_v0.3.1_20250330.py [--feature <feature_name>]

Where <feature_name> can be:
    - credit_card: Test credit card processing (Luhn + masking)
    - guid: Test GUID validation and generation
    - checksum: Test checksum validation
    - encoding: Test encoding transformation
    - all: Test all features (default)
"""

import os
import sys
import argparse
import tempfile
from flatforge.cli.main import validate_file, transform_file

def print_separator(title):
    """Print a formatted separator with title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def run_command(command_type, config_file, input_file, output_file, errors_file):
    """Run a FlatForge command and handle errors."""
    try:
        if command_type == "validate":
            return validate_file(config_file, input_file, output_file, errors_file)
        elif command_type == "transform":
            return transform_file(config_file, input_file, output_file, errors_file)
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_credit_card_processing():
    """Test credit card validation with Luhn algorithm and card masking."""
    print_separator("CREDIT CARD PROCESSING")
    
    config_file = "samples/config/credit_card_processing.yaml"
    input_file = "samples/input/credit_card_data.csv"
    output_file = "samples/output/valid_cards.csv"
    errors_file = "samples/output/card_errors.csv"
    
    print(f"Validating credit card data using Luhn algorithm...")
    print(f"Config: {config_file}")
    print(f"Input: {input_file}")
    
    result = run_command("validate", config_file, input_file, output_file, errors_file)
    
    if result:
        print(f"\nProcessed {result.records_processed} records with {result.error_count} errors")
        print(f"Valid records saved to: {output_file}")
        print(f"Error details saved to: {errors_file}")
        
        # Show sample masked card numbers
        try:
            with open(output_file, 'r') as f:
                lines = f.readlines()
                print("\nSample masked cards:")
                for i, line in enumerate(lines):
                    if i == 0 or i > 3:  # Skip header and limit to 3 lines
                        continue
                    print(f"  {line.strip()}")
        except Exception as e:
            print(f"Error reading output file: {e}")

def test_guid_generation():
    """Test GUID validation and generation."""
    print_separator("GUID VALIDATION AND GENERATION")
    
    config_file = "samples/config/guid_generation.yaml"
    input_file = "samples/input/user_data.csv"
    output_file = "samples/output/users_with_guids.csv"
    errors_file = "samples/output/guid_errors.csv"
    
    print(f"Processing data with GUID validation and generation...")
    print(f"Config: {config_file}")
    print(f"Input: {input_file}")
    
    result = run_command("validate", config_file, input_file, output_file, errors_file)
    
    if result:
        print(f"\nProcessed {result.records_processed} records with {result.error_count} errors")
        print(f"Records with GUIDs saved to: {output_file}")
        print(f"Error details saved to: {errors_file}")
        
        # Show sample GUIDs
        try:
            with open(output_file, 'r') as f:
                lines = f.readlines()
                print("\nSample records with GUIDs:")
                for i, line in enumerate(lines):
                    if i == 0 or i > 3:  # Skip header and limit to 3 lines
                        continue
                    print(f"  {line.strip()}")
        except Exception as e:
            print(f"Error reading output file: {e}")

def test_checksum_all_types():
    """Test all checksum types (single column, multi-column, row-based)."""
    print_separator("CHECKSUM VALIDATION (ALL TYPES)")
    
    config_file = "samples/config/multi_column_checksum.yaml"
    input_file = "samples/input/orders_with_checksum.csv"
    output_file = "samples/output/valid_orders.csv"
    errors_file = "samples/output/checksum_errors.csv"
    
    print(f"Validating data with multi-column SHA256 checksum...")
    print(f"Config: {config_file}")
    print(f"Input: {input_file}")
    
    result = run_command("validate", config_file, input_file, output_file, errors_file)
    
    if result:
        print(f"\nProcessed {result.records_processed} records with {result.error_count} errors")
        print(f"Valid records saved to: {output_file}")
        print(f"Error details saved to: {errors_file}")
        
        try:
            with open(output_file, 'r') as f:
                lines = f.readlines()
                print("\nValid records:")
                for line in lines:
                    print(f"  {line.strip()}")
        except Exception as e:
            print(f"Error reading output file: {e}")
    
    print("\nFor comprehensive testing of all checksum types (sum, xor, mod10, md5, SHA256),")
    print("run the dedicated test script: python samples/test_checksum.py --type all")

def test_encoding_transformation():
    """Test file encoding transformation."""
    print_separator("ENCODING TRANSFORMATION")
    
    # Create a test file with ISO-8859-1 encoding
    test_file = "samples/input/encoding_test.txt"
    
    print(f"Creating test file with ISO-8859-1 encoding: {test_file}")
    
    try:
        with open(test_file, 'w', encoding='ISO-8859-1') as f:
            f.write("Hello World with special characters: à é è ç ù\n")
            f.write("Another line with symbols: € £ © ®\n")
        
        print("Test file created successfully")
        
        config_file = "samples/config/encoding_test.yaml"
        output_file = "samples/output/encoding_test_utf8.txt"
        errors_file = "samples/output/encoding_errors.txt"
        
        # Create a simple config file for encoding transformation
        with open(config_file, 'w') as f:
            f.write("""file_format:
  type: delimited
  delimiter: ","
  has_header: false

file_settings:
  input_encoding: ISO-8859-1
  output_encoding: UTF-8

fields:
  - name: line
    rules:
      - type: required
""")
        
        print(f"\nTransforming file encoding from ISO-8859-1 to UTF-8...")
        print(f"Config: {config_file}")
        print(f"Input: {test_file}")
        
        result = run_command("transform", config_file, test_file, output_file, errors_file)
        
        if result:
            print(f"\nProcessed {result.records_processed} records with {result.error_count} errors")
            print(f"UTF-8 encoded file saved to: {output_file}")
            
            # Show the transformed content
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("\nTransformed content (UTF-8):")
                    print(content)
            except Exception as e:
                print(f"Error reading output file: {e}")
    
    except Exception as e:
        print(f"Error during encoding test: {e}")

def main():
    """Run tests for specified features."""
    parser = argparse.ArgumentParser(description='Test FlatForge v0.3.1 features')
    parser.add_argument('--feature', choices=['credit_card', 'guid', 'checksum', 'encoding', 'all'],
                        default='all', help='Feature to test (default: all)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs('samples/output', exist_ok=True)
    
    if args.feature == 'credit_card' or args.feature == 'all':
        test_credit_card_processing()
    
    if args.feature == 'guid' or args.feature == 'all':
        test_guid_generation()
    
    if args.feature == 'checksum' or args.feature == 'all':
        test_checksum_all_types()
    
    if args.feature == 'encoding' or args.feature == 'all':
        test_encoding_transformation()
    
    print_separator("TESTING COMPLETE")
    print("All tests for FlatForge v0.3.1 features have been completed.")
    print("For more information, see the documentation in docs/user_guide/rules_guide.md")

if __name__ == "__main__":
    main() 