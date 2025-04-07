#!/usr/bin/env python
"""
Test script to demonstrate FlatForge v0.3.0 (20250330) features:
- Extended Checksum Validation (sum, xor, mod10, md5, SHA256)
- Value Resolver Transformer
- Luhn Algorithm Validation
- Card Number Masking
- Encoding Transformation
- GUID Validation and Generation
"""
import os
import sys
import argparse
import subprocess

def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def run_command(command_type, config_file, input_file, output_file, errors_file=None):
    """Run a FlatForge command."""
    try:
        cmd = [
            sys.executable, '-m', 'flatforge.cli.main', command_type,
            '--config', config_file,
            '--input', input_file,
            '--output', output_file
        ]
        
        if errors_file:
            cmd.extend(['--errors', errors_file])
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def test_credit_card_processing():
    """Test credit card processing with Luhn validation, value resolver, and masking."""
    print_separator("CREDIT CARD PROCESSING")
    
    config_file = "samples/config/credit_card_processing.yaml"
    input_file = "samples/input/credit_card_data.csv"
    output_file = "samples/output/valid_cards.csv"
    errors_file = "samples/output/card_errors.csv"
    
    print(f"Validating credit card data with configuration: {config_file}")
    run_command('validate', config_file, input_file, output_file, errors_file)
    
    # Print results
    print("\nValid records:")
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            print(f.read())
    
    print("\nErrors:")
    if os.path.exists(errors_file):
        with open(errors_file, 'r') as f:
            print(f.read())

def test_guid_generation():
    """Test GUID generation."""
    print_separator("GUID GENERATION")
    
    config_file = "samples/config/guid_generation.yaml"
    input_file = "samples/input/user_data.csv"
    output_file = "samples/output/users_with_guids.csv"
    errors_file = "samples/output/guid_errors.csv"
    
    print(f"Processing data with GUID generation: {config_file}")
    run_command('validate', config_file, input_file, output_file, errors_file)
    
    # Print results
    print("\nProcessed records with GUIDs:")
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            print(f.read())

def test_checksum_all_types():
    """Test all checksum validation types (sum, xor, mod10, md5, SHA256)."""
    print_separator("CHECKSUM VALIDATION - ALL TYPES")
    
    # Run the comprehensive test script for checksums
    script_path = "samples/test_checksum.py"
    
    print(f"Running comprehensive checksum tests from {script_path}")
    run_command_result = run_command('validate', "samples/config/multi_column_checksum.yaml", 
                                    "samples/input/orders_with_checksum.csv", 
                                    "samples/output/valid_orders.csv",
                                    "samples/output/checksum_errors.csv")
    
    if run_command_result:
        print("\nTo test all checksum types in detail, run:")
        print(f"python {script_path} --create-data")

def test_encoding_transformation():
    """Test encoding transformation."""
    print_separator("ENCODING TRANSFORMATION")
    
    # Create a simple file with non-ASCII characters in ISO-8859-1 encoding
    test_file = "samples/input/encoding_test.txt"
    with open(test_file, 'wb') as f:
        f.write('Café,Résumé,Déjà vu'.encode('iso-8859-1'))
    
    # Create a simple config file
    config_file = "samples/config/encoding_test.yaml"
    config_content = """
name: Encoding Test
type: delimited
description: A test for encoding transformation
delimiter: ","
quote_char: "\""
escape_char: "\\"
newline: "\\n"
encoding: iso-8859-1
skip_blank_lines: true

file_settings:
  input_encoding: iso-8859-1
  output_encoding: utf-8

sections:
  - name: body
    type: body
    min_records: 0
    record:
      name: data_record
      description: Data record format
      fields:
        - name: field1
          position: 0
        - name: field2
          position: 1
        - name: field3
          position: 2
"""
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    output_file = "samples/output/encoding_test_utf8.txt"
    errors_file = "samples/output/encoding_errors.txt"
    
    print(f"Transforming file encoding from ISO-8859-1 to UTF-8")
    run_command('validate', config_file, test_file, output_file, errors_file)
    
    # Print results
    print("\nTransformed content (UTF-8):")
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            print(f.read())

def main():
    """Run all tests for FlatForge v0.3.0 features."""
    parser = argparse.ArgumentParser(description="Test FlatForge v0.3.0 features (20250330)")
    parser.add_argument('--feature', 
                        choices=['credit_card', 'guid', 'checksum', 'encoding', 'all'], 
                        default='all', 
                        help="Feature to test")
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs("samples/output", exist_ok=True)
    
    if args.feature == 'credit_card' or args.feature == 'all':
        test_credit_card_processing()
    
    if args.feature == 'guid' or args.feature == 'all':
        test_guid_generation()
    
    if args.feature == 'checksum' or args.feature == 'all':
        test_checksum_all_types()
    
    if args.feature == 'encoding' or args.feature == 'all':
        test_encoding_transformation()

if __name__ == "__main__":
    main() 