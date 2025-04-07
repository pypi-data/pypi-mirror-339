#!/usr/bin/env python
"""
Test script specifically focused on demonstrating the enhanced ChecksumRule functionality.
This script tests:
- Single column checksum (legacy)
- Multi-column checksum (new)
- Row-based checksum (new)
- Different algorithms (MD5, SHA256)
"""
import os
import sys
import hashlib
import argparse
import subprocess

def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def create_test_data():
    """Create test data files for the various checksum validation scenarios."""
    # Ensure output directory exists
    os.makedirs("samples/output", exist_ok=True)
    
    # Create test directory if it doesn't exist
    os.makedirs("samples/test_data", exist_ok=True)
    
    # 1. Create test file for single column checksum
    single_column_file = "samples/test_data/single_column_checksum.csv"
    with open(single_column_file, 'w') as f:
        f.write("data,checksum\n")
        # Valid record
        data = "test_data_1"
        checksum = hashlib.md5(data.encode()).hexdigest()
        f.write(f"{data},{checksum}\n")
        # Invalid record
        f.write("test_data_2,invalid_checksum\n")
    
    # 2. Create test file for multi-column checksum
    multi_column_file = "samples/test_data/multi_column_checksum.csv"
    with open(multi_column_file, 'w') as f:
        f.write("H,FILE001,3\n")
        
        # Valid record 1
        customer_id = "CUST001"
        order_id = "ORD001"
        amount = "125.50"
        combined = customer_id + order_id + amount
        checksum = hashlib.sha256(combined.encode()).hexdigest()
        f.write(f"D,{customer_id},{order_id},{amount},{checksum}\n")
        
        # Valid record 2
        customer_id = "CUST002"
        order_id = "ORD002"
        amount = "75.25"
        combined = customer_id + order_id + amount
        checksum = hashlib.sha256(combined.encode()).hexdigest()
        f.write(f"D,{customer_id},{order_id},{amount},{checksum}\n")
        
        # Invalid record
        f.write("D,CUST003,ORD003,200.00,invalid_checksum\n")
    
    # 3. Create test file for row checksum
    row_checksum_file = "samples/test_data/row_checksum.csv"
    with open(row_checksum_file, 'w') as f:
        f.write("name,email,age,checksum\n")
        
        # Valid record 1
        row_data = {"name": "John Doe", "email": "john@example.com", "age": "30"}
        row_str = str(row_data)
        checksum = hashlib.sha256(row_str.encode()).hexdigest()
        f.write(f"{row_data['name']},{row_data['email']},{row_data['age']},{checksum}\n")
        
        # Valid record 2
        row_data = {"name": "Jane Smith", "email": "jane@example.com", "age": "25"}
        row_str = str(row_data)
        checksum = hashlib.sha256(row_str.encode()).hexdigest()
        f.write(f"{row_data['name']},{row_data['email']},{row_data['age']},{checksum}\n")
        
        # Invalid record
        f.write("Bob Johnson,bob@example.com,40,invalid_checksum\n")
    
    print("Created test data files:")
    print(f"- {single_column_file}")
    print(f"- {multi_column_file}")
    print(f"- {row_checksum_file}")

def create_test_configs():
    """Create test configuration files for the various checksum validation scenarios."""
    # Ensure output directory exists
    os.makedirs("samples/test_data", exist_ok=True)
    
    # 1. Create config for single column checksum (legacy approach)
    single_column_config = "samples/test_data/single_column_config.yaml"
    with open(single_column_config, 'w') as f:
        f.write("""
name: Single Column Checksum Test
type: delimited
description: Test for single column checksum validation using global rules
delimiter: ","
quote_char: "\\"" 
encoding: utf-8
skip_blank_lines: true

global_rules:
  - name: data_checksum
    type: checksum
    params:
      field: data
      type: md5
      section: body

sections:
  - name: header
    type: header
    min_records: 1
    max_records: 1
    description: Header section
    record:
      name: header_record
      description: Header record format
      fields:
        - name: data
          position: 0
          description: Data field
        - name: checksum
          position: 1
          description: MD5 checksum of data field

  - name: body
    type: body
    min_records: 0
    record:
      name: data_record
      description: Data record format
      fields:
        - name: data
          position: 0
          description: Data field
        - name: checksum
          position: 1
          description: MD5 checksum of data field
""")
    
    # 2. Create config for multi-column checksum
    multi_column_config = "samples/test_data/multi_column_config.yaml"
    with open(multi_column_config, 'w') as f:
        f.write("""
name: Multi-Column Checksum Test
type: delimited
description: Test for multi-column checksum validation
delimiter: ","
quote_char: "\\"" 
encoding: utf-8
skip_blank_lines: true

global_rules:
  - name: order_checksum
    type: checksum
    params:
      validation_type: multi_column
      columns:
        - customer_id
        - order_id
        - amount
      target_field: checksum
      algorithm: SHA256
      section: body

sections:
  - name: header
    type: header
    min_records: 1
    max_records: 1
    description: Header section
    record:
      name: header_record
      description: Header record format
      fields:
        - name: record_type
          position: 0
          description: Record type indicator (H for header)
          rules:
            - type: choice
              params:
                choices: ["H"]
        - name: file_id
          position: 1
          description: File identifier
        - name: row_count
          position: 2
          description: Number of data rows

  - name: body
    type: body
    min_records: 0
    description: Body section containing data records
    identifier:
      field: record_type
      value: "D"
    record:
      name: data_record
      description: Data record format
      fields:
        - name: record_type
          position: 0
          description: Record type indicator (D for data)
          rules:
            - type: choice
              params:
                choices: ["D"]
        - name: customer_id
          position: 1
          description: Customer identifier
        - name: order_id
          position: 2
          description: Order identifier
        - name: amount
          position: 3
          description: Order amount
        - name: checksum
          position: 4
          description: SHA256 checksum of other fields
""")
    
    # 3. Create config for row checksum
    row_checksum_config = "samples/test_data/row_checksum_config.yaml"
    with open(row_checksum_config, 'w') as f:
        f.write("""
name: Row Checksum Test
type: delimited
description: Test for row-based checksum validation
delimiter: ","
quote_char: "\\"" 
encoding: utf-8
skip_blank_lines: true

global_rules:
  - name: row_checksum
    type: checksum
    params:
      validation_type: row
      target_field: checksum
      algorithm: SHA256
      section: body

sections:
  - name: header
    type: header
    min_records: 1
    max_records: 1
    description: Header section
    record:
      name: header_record
      description: Header record format
      fields:
        - name: name
          position: 0
          description: Name field header
        - name: email
          position: 1
          description: Email field header
        - name: age
          position: 2
          description: Age field header
        - name: checksum
          position: 3
          description: Checksum field header

  - name: body
    type: body
    min_records: 0
    record:
      name: data_record
      description: Data record format
      fields:
        - name: name
          position: 0
          description: Person's name
        - name: email
          position: 1
          description: Email address
        - name: age
          position: 2
          description: Age
        - name: checksum
          position: 3
          description: SHA256 checksum of the entire row
""")
    
    print("Created test configuration files:")
    print(f"- {single_column_config}")
    print(f"- {multi_column_config}")
    print(f"- {row_checksum_config}")

def run_validate_command(config_file, input_file, output_file, errors_file):
    """Run the flatforge validate command."""
    try:
        cmd = [
            sys.executable, '-m', 'flatforge.cli.main', 'validate',
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

def test_single_column_checksum():
    """Test single column checksum validation."""
    print_separator("SINGLE COLUMN CHECKSUM (Legacy)")
    
    config_file = "samples/test_data/single_column_config.yaml"
    input_file = "samples/test_data/single_column_checksum.csv"
    output_file = "samples/output/valid_single_column.csv"
    errors_file = "samples/output/single_column_errors.csv"
    
    print(f"Validating data with single column checksum: {config_file}")
    run_validate_command(config_file, input_file, output_file, errors_file)
    
    # Print results
    print("\nValid records:")
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            print(f.read())
    
    print("\nErrors:")
    if os.path.exists(errors_file):
        with open(errors_file, 'r') as f:
            print(f.read())

def test_multi_column_checksum():
    """Test multi-column checksum validation."""
    print_separator("MULTI-COLUMN CHECKSUM")
    
    config_file = "samples/test_data/multi_column_config.yaml"
    input_file = "samples/test_data/multi_column_checksum.csv"
    output_file = "samples/output/valid_multi_column.csv"
    errors_file = "samples/output/multi_column_errors.csv"
    
    print(f"Validating data with multi-column checksum: {config_file}")
    run_validate_command(config_file, input_file, output_file, errors_file)
    
    # Print results
    print("\nValid records:")
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            print(f.read())
    
    print("\nErrors:")
    if os.path.exists(errors_file):
        with open(errors_file, 'r') as f:
            print(f.read())

def test_row_checksum():
    """Test row-based checksum validation."""
    print_separator("ROW CHECKSUM")
    
    config_file = "samples/test_data/row_checksum_config.yaml"
    input_file = "samples/test_data/row_checksum.csv"
    output_file = "samples/output/valid_row_checksum.csv"
    errors_file = "samples/output/row_checksum_errors.csv"
    
    print(f"Validating data with row checksum: {config_file}")
    run_validate_command(config_file, input_file, output_file, errors_file)
    
    # Print results
    print("\nValid records:")
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            print(f.read())
    
    print("\nErrors:")
    if os.path.exists(errors_file):
        with open(errors_file, 'r') as f:
            print(f.read())

def main():
    """Run tests for checksum validation."""
    parser = argparse.ArgumentParser(description="Test FlatForge checksum validation features")
    parser.add_argument('--type', choices=['single', 'multi', 'row', 'all'], 
                        default='all', help="Type of checksum validation to test")
    parser.add_argument('--create-data', action='store_true', 
                        help="Create test data and configuration files")
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs("samples/output", exist_ok=True)
    
    # Create test data and configurations if requested
    if args.create_data:
        create_test_data()
        create_test_configs()
    
    if args.type == 'single' or args.type == 'all':
        test_single_column_checksum()
    
    if args.type == 'multi' or args.type == 'all':
        test_multi_column_checksum()
    
    if args.type == 'row' or args.type == 'all':
        test_row_checksum()

if __name__ == "__main__":
    main() 