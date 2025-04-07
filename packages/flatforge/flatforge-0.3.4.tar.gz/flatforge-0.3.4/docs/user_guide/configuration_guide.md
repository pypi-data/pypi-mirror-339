# FlatForge Configuration Guide

## Table of Contents

- [Introduction](#introduction)
- [Configuration File Structure](#configuration-file-structure)
- [Supported File Formats](#supported-file-formats)
- [File-Level Settings](#file-level-settings)
- [Section-Level Settings](#section-level-settings)
- [Record-Level Settings](#record-level-settings)
- [Field-Level Settings](#field-level-settings)
- [Global Rules](#global-rules)
- [Complete Configuration Examples](#complete-configuration-examples)

## Introduction

FlatForge uses YAML or JSON configuration files to define the structure, validation rules, and transformation rules for flat files. This guide explains the configuration file structure and all supported settings.

## Configuration File Structure

A configuration file has a hierarchical structure that defines:

1. File format properties (type, encoding, delimiters, etc.)
2. Sections in the file (header, body, footer)
3. Record structure for each section
4. Fields within each record
5. Rules for each field
6. Global rules that apply across multiple records

Here's a simplified structure of a configuration file:

```yaml
name: Format Name
type: fixed_length  # or delimited
# File-level settings
sections:
  - name: section_name
    type: header  # or body, footer
    # Section-level settings
    record:
      name: record_name
      # Record-level settings
      fields:
        - name: field_name
          # Field-level settings
          rules:
            - type: rule_type
              # Rule parameters
global_rules:
  - type: rule_type
    # Global rule parameters
```

## Supported File Formats

FlatForge supports two main file formats:

### Fixed-Length Format

Fixed-length files have fields with predefined lengths. Each field occupies a specific number of characters in the record.

```yaml
name: Employee File
type: fixed_length
newline: "\n"
encoding: utf-8
sections:
  - name: body
    type: body
    record:
      name: employee_record
      fields:
        - name: id
          position: 0
          length: 5
        - name: name
          position: 5
          length: 30
        - name: salary
          position: 35
          length: 10
```

### Delimited Format

Delimited files use special characters to separate fields. CSV (Comma-Separated Values) is a common example.

```yaml
name: Sales Data
type: delimited
delimiter: ","
quote_char: "\""
escape_char: "\\"
newline: "\n"
encoding: utf-8
sections:
  - name: body
    type: body
    record:
      name: sales_record
      fields:
        - name: date
          position: 0
        - name: product
          position: 1
        - name: quantity
          position: 2
        - name: price
          position: 3
```

## File-Level Settings

These settings apply to the entire file format:

| Setting | Description | Type | Default | Required |
|---------|-------------|------|---------|----------|
| `name` | Name of the file format | String | N/A | Yes |
| `type` | Type of file format: `fixed_length` or `delimited` | String | N/A | Yes |
| `description` | Description of the file format | String | Empty string | No |
| `delimiter` | Field delimiter character (for delimited files) | String | "," | Only for delimited files |
| `quote_char` | Quote character for field values (for delimited files) | String | "\"" | No |
| `escape_char` | Escape character (for delimited files) | String | "\\" | No |
| `newline` | Line ending character(s) | String | "\n" | No |
| `encoding` | File encoding | String | "utf-8" | No |
| `skip_blank_lines` | Whether to skip blank lines | Boolean | `true` | No |
| `exit_on_first_error` | Whether to stop processing on the first error | Boolean | `false` | No |
| `trim_whitespace` | Whether to trim whitespace from field values | Boolean | `false` | No |
| `ignore_extra_fields` | Whether to ignore extra fields in records | Boolean | `false` | No |
| `ignore_missing_fields` | Whether to ignore missing fields in records | Boolean | `false` | No |

Example:

```yaml
name: Sales Data
type: delimited
description: "Sales data in CSV format"
delimiter: ","
quote_char: "\""
escape_char: "\\"
newline: "\n"
encoding: utf-8
skip_blank_lines: true
exit_on_first_error: false
trim_whitespace: true
ignore_extra_fields: false
ignore_missing_fields: false
```

## Section-Level Settings

These settings apply to a section within the file:

| Setting | Description | Type | Default | Required |
|---------|-------------|------|---------|----------|
| `name` | Name of the section | String | N/A | Yes |
| `type` | Type of section: `header`, `body`, or `footer` | String | N/A | Yes |
| `description` | Description of the section | String | Empty string | No |
| `min_records` | Minimum number of records in this section | Integer | 0 | No |
| `max_records` | Maximum number of records in this section | Integer | Unlimited | No |
| `identifier` | Configuration for identifying records in this section | Object | N/A | No |

### Section Identification

The `identifier` setting is used to identify which section a record belongs to. It has the following structure:

```yaml
identifier:
  field: field_name  # The field used to identify the section
  value: expected_value  # The expected value of the field
```

If no identifiers are provided, FlatForge uses positional logic:
- For 2-section files (header + body): The header is the first record, the body is everything else.
- For 3-section files (header + body + footer): The header is the first record, the footer is the last record, and the body is everything in between.

Example:

```yaml
sections:
  - name: header
    type: header
    min_records: 1
    max_records: 1
    description: "File header containing batch information"
    identifier:
      field: record_type
      value: "H"
    record:
      # Record definition
  
  - name: body
    type: body
    min_records: 1
    description: "Data records"
    identifier:
      field: record_type
      value: "D"
    record:
      # Record definition
      
  - name: footer
    type: footer
    min_records: 1
    max_records: 1
    description: "File footer with summary information"
    identifier:
      field: record_type
      value: "F"
    record:
      # Record definition
```

## Record-Level Settings

These settings apply to a record within a section:

| Setting | Description | Type | Default | Required |
|---------|-------------|------|---------|----------|
| `name` | Name of the record | String | N/A | Yes |
| `description` | Description of the record | String | Empty string | No |

Example:

```yaml
record:
  name: employee_record
  description: "Employee information record"
  fields:
    # Field definitions
```

## Field-Level Settings

These settings apply to a field within a record:

| Setting | Description | Type | Default | Required |
|---------|-------------|------|---------|----------|
| `name` | Name of the field | String | N/A | Yes |
| `position` | Position of the field in the record (0-based) | Integer | N/A | Yes |
| `length` | Length of the field (for fixed-length files) | Integer | N/A | Only for fixed-length files |
| `description` | Description of the field | String | Empty string | No |
| `rules` | List of rules to apply to this field | Array | Empty array | No |

Example for fixed-length format:

```yaml
fields:
  - name: employee_id
    position: 0
    length: 10
    description: "Employee ID"
    rules:
      - type: required
      - type: string_length
        params:
          min_length: 10
          max_length: 10
```

Example for delimited format:

```yaml
fields:
  - name: product_code
    position: 0
    description: "Product code"
    rules:
      - type: required
      - type: regex
        params:
          pattern: "^[A-Z]{2}\\d{4}$"
```

## Rules

Field rules are divided into two main categories:

1. **Validation Rules**: These rules validate that field values meet certain criteria.
2. **Transformation Rules**: These rules modify field values during processing.

For detailed information about rules, refer to:
- [Validation and Transformation Rules Guide](rules_guide.md)
- [Transformation Rules Guide](transformation_rules.md)

Basic rule structure:

```yaml
rules:
  - type: rule_type  # The type of rule
    name: rule_name  # Optional, defaults to the type
    params:          # Optional parameters for the rule
      param1: value1
      param2: value2
```

## Global Rules

Global rules apply across multiple records in a file. They are defined at the file level:

```yaml
global_rules:
  - type: rule_type
    name: rule_name
    params:
      param1: value1
      param2: value2
```

For detailed information about global rules, refer to:
- [Global Rules Guide](global_rules.md)

## Complete Configuration Examples

### Fixed-Length File Example

```yaml
name: Employee File Format
type: fixed_length
description: "Fixed-length file format for employee data"
newline: "\n"
encoding: utf-8
skip_blank_lines: true
exit_on_first_error: false

sections:
  - name: header
    type: header
    min_records: 1
    max_records: 1
    description: "Header section containing batch information"
    record:
      name: header_record
      description: "Header record format"
      fields:
        - name: record_type
          position: 0
          length: 1
          description: "Record type indicator (H for header)"
          rules:
            - type: choice
              params:
                choices: ["H"]
        - name: batch_reference
          position: 1
          length: 10
          description: "Batch reference number"
          rules:
            - type: required
            - type: string_length
              params:
                min_length: 1
                max_length: 10
        - name: batch_timestamp
          position: 11
          length: 14
          description: "Batch timestamp (YYYYMMDDHHmmss)"
          rules:
            - type: required
            - type: date
              params:
                format: "%Y%m%d%H%M%S"
        - name: record_count
          position: 25
          length: 6
          description: "Expected number of data records"
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0

  - name: body
    type: body
    min_records: 0
    description: "Body section containing employee records"
    identifier:
      field: record_type
      value: "D"
    record:
      name: employee_record
      description: "Employee record format"
      fields:
        - name: record_type
          position: 0
          length: 1
          description: "Record type indicator (D for data)"
          rules:
            - type: choice
              params:
                choices: ["D"]
        - name: employee_id
          position: 1
          length: 10
          description: "Employee ID"
          rules:
            - type: required
            - type: string_length
              params:
                min_length: 10
                max_length: 10
        - name: first_name
          position: 11
          length: 20
          description: "Employee first name"
          rules:
            - type: required
            - type: string_length
              params:
                min_length: 1
                max_length: 20
            - type: trim
              params:
                type: right
        - name: last_name
          position: 31
          length: 30
          description: "Employee last name"
          rules:
            - type: required
            - type: string_length
              params:
                min_length: 1
                max_length: 30
            - type: trim
              params:
                type: right
        - name: date_of_birth
          position: 61
          length: 8
          description: "Date of birth (YYYYMMDD)"
          rules:
            - type: required
            - type: date
              params:
                format: "%Y%m%d"
        - name: salary
          position: 69
          length: 10
          description: "Annual salary (no decimal part)"
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0
            - type: pad
              params:
                length: 10
                char: "0"
                side: left

  - name: footer
    type: footer
    min_records: 1
    max_records: 1
    description: "Footer section containing summary information"
    identifier:
      field: record_type
      value: "F"
    record:
      name: footer_record
      description: "Footer record format"
      fields:
        - name: record_type
          position: 0
          length: 1
          description: "Record type indicator (F for footer)"
          rules:
            - type: choice
              params:
                choices: ["F"]
        - name: batch_reference
          position: 1
          length: 10
          description: "Batch reference number (must match header)"
          rules:
            - type: required
            - type: string_length
              params:
                min_length: 1
                max_length: 10
        - name: record_count
          position: 11
          length: 6
          description: "Total number of data records"
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0
        - name: total_salary
          position: 17
          length: 15
          description: "Sum of all salaries"
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0

global_rules:
  - type: count
    name: record_count_validation
    params:
      section: body
      expected_count_field: header.record_count
  - type: sum
    name: salary_sum_validation
    params:
      section: body
      field: salary
      target_field: footer.total_salary
  - type: uniqueness
    name: unique_employee_id
    params:
      section: body
      field: employee_id
```

### Delimited File Example

```yaml
name: Transaction Data Format
type: delimited
description: "CSV format for transaction data"
delimiter: ","
quote_char: "\""
escape_char: "\\"
newline: "\n"
encoding: utf-8
skip_blank_lines: true
exit_on_first_error: false

sections:
  - name: header
    type: header
    min_records: 1
    max_records: 1
    description: "Header section containing file information"
    record:
      name: header_record
      description: "Header record format"
      fields:
        - name: record_type
          position: 0
          description: "Record type indicator"
          rules:
            - type: choice
              params:
                choices: ["HEADER"]
        - name: file_date
          position: 1
          description: "File creation date (YYYY-MM-DD)"
          rules:
            - type: required
            - type: date
              params:
                format: "%Y-%m-%d"
        - name: source_system
          position: 2
          description: "Source system code"
          rules:
            - type: required
            - type: string_length
              params:
                min_length: 3
                max_length: 10

  - name: body
    type: body
    min_records: 1
    description: "Body section containing transaction records"
    record:
      name: transaction_record
      description: "Transaction record format"
      fields:
        - name: transaction_id
          position: 0
          description: "Unique transaction ID"
          rules:
            - type: required
            - type: regex
              params:
                pattern: "^TX\\d{10}$"
        - name: customer_id
          position: 1
          description: "Customer ID"
          rules:
            - type: required
            - type: string_length
              params:
                min_length: 5
                max_length: 15
        - name: transaction_date
          position: 2
          description: "Transaction date (YYYY-MM-DD)"
          rules:
            - type: required
            - type: date
              params:
                format: "%Y-%m-%d"
        - name: amount
          position: 3
          description: "Transaction amount"
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0.01
                decimal_precision: 2
        - name: currency
          position: 4
          description: "Currency code"
          rules:
            - type: required
            - type: choice
              params:
                choices: ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
        - name: description
          position: 5
          description: "Transaction description"
          rules:
            - type: string_length
              params:
                max_length: 100
            - type: trim
              params:
                type: both

  - name: footer
    type: footer
    min_records: 1
    max_records: 1
    description: "Footer section containing summary information"
    identifier:
      field: record_type
      value: "FOOTER"
    record:
      name: footer_record
      description: "Footer record format"
      fields:
        - name: record_type
          position: 0
          description: "Record type indicator"
          rules:
            - type: choice
              params:
                choices: ["FOOTER"]
        - name: record_count
          position: 1
          description: "Total number of transaction records"
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0
        - name: total_amount
          position: 2
          description: "Sum of all transaction amounts"
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0
                decimal_precision: 2

global_rules:
  - type: count
    name: transaction_count_validation
    params:
      section: body
      target_field: footer.record_count
  - type: sum
    name: amount_sum_validation
    params:
      section: body
      field: amount
      target_field: footer.total_amount
  - type: uniqueness
    name: unique_transaction_id
    params:
      section: body
      field: transaction_id
```

For more information about specific rules and their parameters, please refer to:
- [Validation and Transformation Rules Guide](rules_guide.md)
- [Transformation Rules Guide](transformation_rules.md)
- [Global Rules Guide](global_rules.md) 