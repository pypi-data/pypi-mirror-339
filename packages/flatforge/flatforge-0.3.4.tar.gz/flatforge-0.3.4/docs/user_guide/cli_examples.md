# FlatForge CLI Examples

This document provides examples of how to use the FlatForge command-line interface (CLI) to test all the sample configurations and input files included in the repository.

## Basic CLI Commands

FlatForge provides three main commands:

1. `validate`: Validate a file against a schema
2. `convert`: Convert a file from one format to another
3. `count`: Count records in a file

## Validation Examples

### Validating a Fixed-Length File

```bash
flatforge validate --config schemas/fixed_length.yaml --input data/fixed_length.txt --output output/valid.txt --errors output/errors.txt
```

### Validating a Delimited File

```bash
flatforge validate --config schemas/delimited.yaml --input data/delimited.csv --output output/valid.csv --errors output/errors.csv
```

### Validating with Record Type Identifiers

```bash
flatforge validate --config schemas/multi_section.yaml --input data/multi_section.txt --output output/valid.txt --errors output/errors.txt
```

### Validating with Global Rules

```bash
flatforge validate --config samples/config/multi_column_checksum.yaml --input samples/input/orders_with_checksum.csv --output samples/output/valid_orders.csv --errors samples/output/checksum_errors.csv
```

## Conversion Examples

### Converting from Fixed-Length to Delimited

```bash
flatforge convert --input-config schemas/fixed_length.yaml --output-config schemas/delimited.yaml --input data/fixed_length.txt --output output/converted.csv --errors output/errors.csv
```

### Converting with Mapping Configuration

```bash
flatforge convert --input-config schemas/fixed_length.yaml --output-config schemas/delimited.yaml --mapping schemas/mapping.yaml --input data/fixed_length.txt --output output/converted.csv --errors output/errors.csv
```

### Converting with Transformation Rules

```bash
flatforge convert --input-config schemas/fixed_length_with_transformations.yaml --output-config schemas/delimited.yaml --input data/fixed_length.txt --output output/converted.csv --errors output/errors.csv
```

## Counting Examples

### Counting Records in a Fixed-Length File

```bash
flatforge count --config schemas/fixed_length.yaml --input data/fixed_length.txt --output output/counts.txt
```

### Counting Records in a Delimited File

```bash
flatforge count --config schemas/delimited.yaml --input data/delimited.csv --output output/counts.txt
```

### Counting Records with Record Type Identifiers

```bash
flatforge count --config schemas/multi_section.yaml --input data/multi_section.txt --output output/counts.txt
```

## Testing Feature Sets

FlatForge includes sample scripts to test specific feature sets. These scripts use a naming convention of `test_<feature_set>_v<version>_<yyyyMMdd>.py`.

### Testing Extended Checksum Validation

To test the extended checksum validation features (including sum, xor, mod10, md5, and SHA256 algorithms):

```bash
python samples/test_new_features_v0.3.0_20250330.py --feature checksum
```

This script will:
1. Run a test for multi-column checksum validation using SHA256
2. Provide instructions on running more detailed tests for all checksum types

For a more comprehensive test of checksum validation:

```bash
python samples/test_checksum.py --create-data
python samples/test_checksum.py --type all
```

This creates test data for all checksum types and validates it.

### Testing Credit Card Processing with Luhn Validation

To test credit card processing with Luhn algorithm validation and card number masking:

```bash
python samples/test_new_features_v0.3.0_20250330.py --feature credit_card
```

### Testing GUID Validation and Generation

To test GUID validation and generation:

```bash
python samples/test_new_features_v0.3.0_20250330.py --feature guid
```

### Testing Encoding Transformation

To test file encoding transformation:

```bash
python samples/test_new_features_v0.3.0_20250330.py --feature encoding
```

### Testing All New Features

To test all new features at once:

```bash
python samples/test_new_features_v0.3.0_20250330.py
```

## Testing All Transformation Rules

To test all transformation rules at once, you can use the provided Python script:

```bash
python samples/test_transformations.py
```

This script will:
1. Test transformations on delimited files
2. Test transformations on fixed-length files
3. Test format conversion between delimited and fixed-length formats

## Batch Testing

You can create a shell script to run all the tests at once. Here's an example for Unix-based systems:

```bash
#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p samples/output

# Validation tests
echo "Running validation tests..."

# Employee data tests
flatforge validate --config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_valid.txt --errors samples/output/employee_data_errors.txt
flatforge validate --config samples/config/employee_fixed_length_no_identifier.yaml --input samples/input/employee_data_no_identifier.txt --output samples/output/employee_data_no_identifier_valid.txt --errors samples/output/employee_data_no_identifier_errors.txt
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_valid.csv --errors samples/output/employee_data_errors.csv
flatforge validate --config samples/config/employee_csv_no_identifier.yaml --input samples/input/employee_data_no_identifier.csv --output samples/output/employee_data_no_identifier_valid.csv --errors samples/output/employee_data_no_identifier_errors.csv

# Global rules and checksum tests
flatforge validate --config samples/config/multi_column_checksum.yaml --input samples/input/orders_with_checksum.csv --output samples/output/valid_orders.csv --errors samples/output/checksum_errors.csv

# Credit card processing tests
flatforge validate --config samples/config/credit_card_processing.yaml --input samples/input/credit_card_data.csv --output samples/output/valid_cards.csv --errors samples/output/card_errors.csv

# GUID validation and generation tests
flatforge validate --config samples/config/guid_generation.yaml --input samples/input/user_data.csv --output samples/output/users_with_guids.csv --errors samples/output/guid_errors.csv

# Transformation tests
flatforge validate --config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_fixed_length_valid.txt --errors samples/output/transformation_test_fixed_length_errors.txt
flatforge validate --config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_valid.csv --errors samples/output/transformation_test_errors.csv

# Conversion tests
echo "Running conversion tests..."
flatforge convert --input-config samples/config/employee_csv.yaml --output-config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_converted.txt --errors samples/output/employee_data_conversion_errors.txt
flatforge convert --input-config samples/config/employee_fixed_length.yaml --output-config samples/config/employee_csv.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_converted.csv --errors samples/output/employee_data_conversion_errors.csv
flatforge convert --input-config samples/config/transformation_rules_test.yaml --output-config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_converted.txt --errors samples/output/transformation_test_conversion_errors.txt
flatforge convert --input-config samples/config/transformation_rules_fixed_length.yaml --output-config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_converted.csv --errors samples/output/transformation_test_conversion_errors.txt

# Counting tests
echo "Running counting tests..."
flatforge count --config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_counts.txt
flatforge count --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_counts.txt
flatforge count --config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_fixed_length_counts.txt
flatforge count --config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_counts.txt

# Run the Python test scripts
echo "Running Python test scripts..."
python samples/test_transformations.py
python samples/test_new_features_v0.3.0_20250330.py

echo "All tests completed."
```

For Windows systems, you can create a similar batch file:

```batch
@echo off
REM Create output directory if it doesn't exist
mkdir samples\output 2>nul

REM Validation tests
echo Running validation tests...

REM Employee data tests
flatforge validate --config samples\config\employee_fixed_length.yaml --input samples\input\employee_data.txt --output samples\output\employee_data_valid.txt --errors samples\output\employee_data_errors.txt
flatforge validate --config samples\config\employee_fixed_length_no_identifier.yaml --input samples\input\employee_data_no_identifier.txt --output samples\output\employee_data_no_identifier_valid.txt --errors samples\output\employee_data_no_identifier_errors.txt
flatforge validate --config samples\config\employee_csv.yaml --input samples\input\employee_data.csv --output samples\output\employee_data_valid.csv --errors samples\output\employee_data_errors.csv
flatforge validate --config samples\config\employee_csv_no_identifier.yaml --input samples\input\employee_data_no_identifier.csv --output samples\output\employee_data_no_identifier_valid.csv --errors samples\output\employee_data_no_identifier_errors.csv

REM Global rules and checksum tests
flatforge validate --config samples\config\multi_column_checksum.yaml --input samples\input\orders_with_checksum.csv --output samples\output\valid_orders.csv --errors samples\output\checksum_errors.csv

REM Credit card processing tests
flatforge validate --config samples\config\credit_card_processing.yaml --input samples\input\credit_card_data.csv --output samples\output\valid_cards.csv --errors samples\output\card_errors.csv

REM GUID validation and generation tests
flatforge validate --config samples\config\guid_generation.yaml --input samples\input\user_data.csv --output samples\output\users_with_guids.csv --errors samples\output\guid_errors.csv

REM Transformation tests
flatforge validate --config samples\config\transformation_rules_fixed_length.yaml --input samples\input\transformation_test_fixed_length.txt --output samples\output\transformation_test_fixed_length_valid.txt --errors samples\output\transformation_test_fixed_length_errors.txt
flatforge validate --config samples\config\transformation_rules_test.yaml --input samples\input\transformation_test_input.csv --output samples\output\transformation_test_valid.csv --errors samples\output\transformation_test_errors.txt

REM Conversion tests
echo Running conversion tests...
flatforge convert --input-config samples\config\employee_csv.yaml --output-config samples\config\employee_fixed_length.yaml --input samples\input\employee_data.csv --output samples\output\employee_data_converted.txt --errors samples\output\employee_data_conversion_errors.txt
flatforge convert --input-config samples\config\employee_fixed_length.yaml --output-config samples\config\employee_csv.yaml --input samples\input\employee_data.txt --output samples\output\employee_data_converted.csv --errors samples\output\employee_data_conversion_errors.csv
flatforge convert --input-config samples\config\transformation_rules_test.yaml --output-config samples\config\transformation_rules_fixed_length.yaml --input samples\input\transformation_test_input.csv --output samples\output\transformation_test_converted.txt --errors samples\output\transformation_test_conversion_errors.txt
flatforge convert --input-config samples\config\transformation_rules_fixed_length.yaml --output-config samples\config\transformation_rules_test.yaml --input samples\input\transformation_test_fixed_length.txt --output samples\output\transformation_test_converted.csv --errors samples\output\transformation_test_conversion_errors.csv

REM Counting tests
echo Running counting tests...
flatforge count --config samples\config\employee_fixed_length.yaml --input samples\input\employee_data.txt --output samples\output\employee_data_counts.txt
flatforge count --config samples\config\employee_csv.yaml --input samples\input\employee_data.csv --output samples\output\employee_data_counts.txt
flatforge count --config samples\config\transformation_rules_fixed_length.yaml --input samples\input\transformation_test_fixed_length.txt --output samples\output\transformation_test_fixed_length_counts.txt
flatforge count --config samples\config\transformation_rules_test.yaml --input samples\input\transformation_test_input.csv --output samples\output\transformation_test_counts.txt

REM Run the Python test scripts
echo Running Python test scripts...
python samples\test_transformations.py
python samples\test_new_features_v0.3.0_20250330.py

echo All tests completed.
```

## Expected Results

When running these tests, you should expect the following:

1. **Validation Tests**: All records should be validated according to the rules defined in the configuration files. Any validation errors will be written to the error files.

2. **Conversion Tests**: Records should be converted from one format to another according to the mapping defined in the configuration files.

3. **Counting Tests**: The number of records in each section should be counted and written to the output files.

4. **Transformation Tests**: All transformation rules should be applied to the fields as defined in the configuration files.

5. **Global Rules Tests**: Global rules like checksums, uniqueness checks, and counts should be properly validated across multiple records.

6. **Feature-Specific Tests**: Each feature-specific test script should validate its respective functionality and report any issues.

## Troubleshooting

If you encounter any issues when running these tests, check the following:

1. Make sure all the required files exist in the correct locations.
2. Check that the flatforge library is installed correctly.
3. Verify that the configuration files are valid YAML or JSON.
4. Check the error files for specific validation or conversion errors.
5. For global rules, ensure that the rule parameters are correctly configured.
6. For checksum validation, verify that the algorithm type is correctly specified.

For more detailed information about the flatforge CLI, refer to the [User Guide](README.md). 