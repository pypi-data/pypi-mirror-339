# FlatForge Rules Guide

## Table of Contents
- [Introduction](#introduction)
- [Validation Rules](#validation-rules)
  - [Required Field](#required-field)
  - [String Length](#string-length)
  - [Numeric Range](#numeric-range)
  - [Date Format](#date-format)
  - [Regular Expression](#regular-expression)
  - [Checksum](#checksum)
  - [Luhn Algorithm](#luhn-algorithm)
  - [GUID Validation](#guid-validation)
- [Transformation Rules](#transformation-rules)
  - [Trim](#trim)
  - [Case Conversion](#case-conversion)
  - [Padding](#padding)
  - [Date Format Conversion](#date-format-conversion)
  - [Substring](#substring)
  - [Replace](#replace)
  - [Value Resolver](#value-resolver)
  - [Field Masking](#field-masking)
  - [GUID Generation](#guid-generation)
- [Global Rules](#global-rules)
  - [Count](#count)
  - [Sum](#sum)
  - [Uniqueness](#uniqueness)
- [File Settings](#file-settings)

## Introduction

FlatForge provides a powerful rule system for validating and transforming data in flat files. Rules are defined in the YAML configuration file and are applied to fields during processing. This guide provides detailed information about all available rules.

## Validation Rules

Validation rules check if field values meet specific criteria. If a validation rule fails, an error is reported.

### Required Field

The `required` rule validates that a field is not empty.

```yaml
- type: required
```

### String Length

The `string_length` rule validates the length of a string field.

```yaml
- type: string_length
  params:
    min_length: 5
    max_length: 10
```

Parameters:
- `min_length` (optional): Minimum length of the string
- `max_length` (optional): Maximum length of the string

### Numeric Range

The `numeric` rule validates that a field is numeric and within a specified range.

```yaml
- type: numeric
  params:
    min_value: 0
    max_value: 100
    decimal_precision: 2
```

Parameters:
- `min_value` (optional): Minimum value
- `max_value` (optional): Maximum value
- `decimal_precision` (optional): Maximum number of decimal places

### Date Format

The `date` rule validates that a field is a valid date in a specified format.

```yaml
- type: date
  params:
    format: "%Y-%m-%d"
    min_date: "2020-01-01"
    max_date: "2029-12-31"
```

Parameters:
- `format` (optional, default: "%Y-%m-%d"): Date format string using Python's datetime format
- `min_date` (optional): Minimum date in the specified format
- `max_date` (optional): Maximum date in the specified format

### Regular Expression

The `regex` rule validates that a field matches a regular expression.

```yaml
- type: regex
  params:
    pattern: "^[A-Z]{2}\\d{4}$"
```

Parameters:
- `pattern` (required): Regular expression pattern

### Checksum

The checksum rule validates that a checksum value in a record matches the calculated checksum of specified data. This rule is now implemented as a global rule, which provides more flexibility for validating checksums across records or within records.

#### Configuration Options

Checksum validation can be configured in two ways:

1. **As a field validation rule (Legacy)**: This approach is maintained for backward compatibility but is not recommended for new configurations.
2. **As a global rule (Recommended)**: This approach provides more flexibility and better performance.

#### Using as a Global Rule (Recommended)

```yaml
global_rules:
  - name: data_checksum
    type: checksum
    params:
      field: data_field                # For single column checksum
      type: md5                        # Checksum algorithm type
      expected_checksum: "abc123..."   # Optional expected value
      section: body                    # Section to process
```

#### Single Column Checksum

```yaml
global_rules:
  - name: data_checksum
    type: checksum
    params:
      field: data_field                # Field containing the value to checksum
      type: md5                        # Checksum type (md5, sum, xor, mod10)
      section: body                    # Section to process
      target_field: checksum_field     # Field containing the expected checksum
```

#### Multi-Column Checksum

```yaml
global_rules:
  - name: multi_column_checksum
    type: checksum
    params:
      validation_type: multi_column    # Specify multi-column validation
      columns:                         # List of fields to include
        - customer_id
        - order_id
        - amount
      target_field: checksum_field     # Field containing the expected checksum
      algorithm: SHA256                # Hash algorithm (MD5 or SHA256)
      section: body                    # Section to process
```

#### Row Checksum

```yaml
global_rules:
  - name: row_checksum
    type: checksum
    params:
      validation_type: row             # Specify row validation
      target_field: row_checksum_field # Field containing the expected checksum
      algorithm: SHA256                # Hash algorithm (MD5 or SHA256)
      section: body                    # Section to process
```

Parameters:
- `field` (for single column): Field containing the value to checksum
- `validation_type` (optional, default: "column"): Type of checksum validation ("column", "multi_column", or "row")
- `columns` (required for multi-column): List of fields to include in the checksum calculation
- `target_field` (optional): Field containing the expected checksum
- `algorithm` (optional, default: "MD5"): Hash algorithm to use (MD5 or SHA256)
- `type` (optional, legacy parameter): Checksum type for single column (md5, sum, xor, mod10)
- `section` (optional): Section to process
- `expected_checksum` (optional): Expected checksum value

### Luhn Algorithm

The Luhn algorithm rule validates credit card numbers and other identification numbers using the Luhn algorithm (mod 10).

```yaml
- type: luhn
  params:
    strip_spaces: true    # Optional, default: true
    strip_hyphens: true   # Optional, default: true
    error_message: "Invalid credit card number"  # Optional custom error
```

Parameters:
- `strip_spaces` (optional, default: true): Whether to remove spaces before validation
- `strip_hyphens` (optional, default: true): Whether to remove hyphens before validation
- `error_message` (optional): Custom error message for validation failures

### GUID Validation

Validates that a field contains a valid GUID/UUID.

```yaml
- type: guid
  params:
    version: 4  # Optional, validates specific UUID version
```

Parameters:
- `version` (optional): Validates that the UUID is of a specific version (1, 3, 4, or 5)

## Transformation Rules

Transformation rules modify field values during processing.

### Trim

The `trim` rule removes whitespace from a field value.

```yaml
- type: trim
  params:
    type: both  # can be "left", "right", or "both"
```

Parameters:
- `type` (optional, default: "both"): Type of trimming to perform ("left", "right", or "both")

### Case Conversion

The `case` rule changes the case of a field value.

```yaml
- type: case
  params:
    type: upper  # can be "upper", "lower", "title", or "camel"
```

Parameters:
- `type` (optional, default: "upper"): Type of case conversion to perform ("upper", "lower", "title", or "camel")

### Padding

The `pad` rule pads a field value to a specified length.

```yaml
- type: pad
  params:
    length: 10
    char: "0"
    side: left  # can be "left" or "right"
```

Parameters:
- `length` (required): Target length for the field
- `char` (optional, default: " "): Character to use for padding
- `side` (optional, default: "left"): Side to pad ("left" or "right")

### Date Format Conversion

The `date_format` rule converts a date from one format to another.

```yaml
- type: date_format
  params:
    input_format: "%Y%m%d"
    output_format: "%Y-%m-%d"
```

Parameters:
- `input_format` (optional, default: "%Y%m%d"): Input date format
- `output_format` (optional, default: "%Y-%m-%d"): Output date format

### Substring

The `substring` rule extracts a substring from a field value.

```yaml
- type: substring
  params:
    start: 0
    end: 10
```

Parameters:
- `start` (optional, default: 0): Start index
- `end` (optional): End index

### Replace

The `replace` rule replaces text in a field value.

```yaml
- type: replace
  params:
    old: "find_this"
    new: "replace_with_this"
```

Parameters:
- `old` (required): Text to find
- `new` (optional, default: ""): Text to replace with

### Value Resolver

Transforms a value by looking it up in a mapping file.

```yaml
- type: value_resolver
  params:
    source_field: status_code
    target_field: status_description
    mapping_file: path/to/mappings.json
    default_value: Unknown  # Optional, used when mapping not found
```

Parameters:
- `source_field` (required): Field containing the value to look up
- `target_field` (required): Field to store the resolved value
- `mapping_file` (required): Path to the JSON mapping file
- `default_value` (optional, default: ""): Value to use when mapping is not found

The JSON mapping file should have a simple key-value structure:
```json
{
  "A": "Active",
  "I": "Inactive",
  "P": "Pending"
}
```

### Field Masking

Masks sensitive data like credit card numbers.

**Using start_index and mask_length:**
```yaml
- type: mask
  params:
    source_field: card_number
    target_field: masked_card_number  # Optional, defaults to source_field
    mask_char: "*"  # Optional, defaults to "*"
    start_index: 6
    mask_length: 6
```

**Using keep_first and keep_last:**
```yaml
- type: mask
  params:
    source_field: card_number
    target_field: masked_card_number
    mask_char: "X"
    keep_first: 4
    keep_last: 4
```

Parameters:
- `source_field` (required): Field containing the value to mask
- `target_field` (optional): Field to store the masked value, defaults to source_field
- `mask_char` (optional, default: "*"): Character to use for masking
- `start_index` and `mask_length`: Start position and length of the section to mask
- `keep_first` and `keep_last`: Number of characters to keep at the beginning and end

### GUID Generation

Generates a GUID/UUID and stores it in the specified field.

```yaml
- type: generate_guid
  params:
    version: 4  # Optional, defaults to 4 (random)
    # Supported versions: 1 (time-based), 3 (MD5), 4 (random), 5 (SHA-1)
```

Parameters:
- `version` (optional, default: 4): Version of UUID to generate (1, 3, 4, or 5)

## Global Rules

Global rules are applied across multiple records rather than to a single field. They are defined at the top level of the configuration file.

```yaml
global_rules:
  - type: count
    name: count_records
    params:
      section: body
      count_field: footer.record_count
```

### Count

The `count` rule counts the number of records in a section and stores the result in a specified field.

Parameters:
- `section` (required): Section to count records in
- `count_field` (required): Field to store the count in, specified as `section.field`

### Sum

The `sum` rule calculates the sum of values in a specified field across all records in a section.

```yaml
global_rules:
  - type: sum
    name: sum_amount
    params:
      section: body
      field: amount
      sum_field: footer.total_amount
```

Parameters:
- `section` (required): Section to sum records in
- `field` (required): Field to sum
- `sum_field` (required): Field to store the sum in, specified as `section.field`

### Uniqueness

The `uniqueness` rule ensures that a field or combination of fields is unique across all records in a section.

```yaml
global_rules:
  - type: uniqueness
    name: unique_id
    params:
      section: body
      fields:
        - customer_id
        - order_id
```

Parameters:
- `section` (required): Section to check uniqueness in
- `fields` (required): List of fields that must be unique in combination

## File Settings

The `file_settings` section allows you to control file-level options.

```yaml
file_settings:
  input_encoding: ASCII  # Encoding of the input file
  output_encoding: UTF-8  # Encoding for the output file
```

Supported encodings include:
- UTF-8
- ASCII
- ISO-8859-1
- Windows-1252
- UTF-16
- And other encodings supported by Python

```yaml
# Example with file settings
file_settings:
  input_encoding: Windows-1252
  output_encoding: UTF-8

sections:
  - name: header
    # ... section configuration ...
```

## 3. CHANGELOG Update

```markdown:CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Extended Checksum Validation: Support for validating checksums across multiple columns or entire rows
- Value Resolver transformer: Transform values using a JSON mapping file
- Luhn Algorithm validation: Validate credit card numbers and other identifiers
- Card Number Masking: Mask sensitive data with configurable parameters
- File Encoding Transformation: Convert between different file encodings
- GUID Validation and Generation: Validate and generate UUIDs
- File-level settings for controlling input and output encoding

## [0.3.0] - 2023-XX-XX

<!-- ... existing content ... -->
```

## Example Configuration Files

Let's also create a few example configuration files to demonstrate the new functionality:

### 1. Example: Credit Card Processing

```yaml:samples/config/credit_card_processing.yaml
file_settings:
  input_encoding: UTF-8
  output_encoding: UTF-8

sections:
  - name: header
    fields:
      - name: record_type
      - name: batch_id
      - name: timestamp

  - name: body
    fields:
      - name: record_type
      - name: card_number
      - name: expiry_date
      - name: cardholder_name
      - name: transaction_id
      - name: amount
      - name: status_code

    validation_rules:
      - rule: luhn
        column: card_number
        strip_spaces: true
        strip_hyphens: true
        error_message: "Invalid credit card number"
      
      - rule: guid
        column: transaction_id

    transformation_rules:
      - rule: mask
        source_field: card_number
        target_field: masked_card
        keep_first: 6
        keep_last: 4
        mask_char: "*"
      
      - rule: value_resolver
        source_field: status_code
        target_field: status_description
        mapping_file: ./samples/data/status_codes.json
        default_value: "Unknown Status"
```

### 2. Example: Data with GUID Generation

```yaml:samples/config/guid_generation.yaml
file_settings:
  input_encoding: UTF-8
  output_encoding: UTF-8

sections:
  - name: header
    fields:
      - name: record_type
      - name: file_id
      - name: timestamp

  - name: body
    fields:
      - name: record_type
      - name: name
      - name: email
      - name: transaction_id

    transformation_rules:
      - rule: generate_guid
        target_field: transaction_id
        version: 4

    validation_rules:
      - rule: required
        column: name
      
      - rule: required
        column: email
```

### 3. Example: Multi-column Checksum

```yaml:samples/config/multi_column_checksum.yaml
file_settings:
  input_encoding: UTF-8
  output_encoding: UTF-8

sections:
  - name: header
    fields:
      - name: record_type
      - name: file_id
      - name: row_count

  - name: body
    fields:
      - name: record_type
      - name: customer_id
      - name: order_id
      - name: amount
      - name: checksum

    validation_rules:
      - rule: checksum
        type: column
        columns:
          - customer_id
          - order_id
          - amount
        target_field: checksum
        algorithm: SHA256
```

These tests, documentation, and examples provide a comprehensive implementation plan for all the requested features while maintaining backward compatibility. 