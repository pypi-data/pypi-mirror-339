# Global Rules

Global rules in FlatForge are rules that operate across multiple records in a file. They are used to validate relationships between records, such as ensuring that the sum of a field across all records matches a specified value, or that a field has unique values across all records.

## Types of Global Rules

FlatForge supports the following types of global rules:

### Count Rule

The Count rule counts the number of records in a section and validates that the count matches a specified value or a value from another field.

```yaml
global_rules:
  - type: count
    name: employee_count
    params:
      section: body
      count_field: footer.employee_count
      insert_value: true  # Insert the calculated count into the target field
      target_field: footer.employee_count
      include_invalid_records: false  # Only include valid records in the count
```

### Sum Rule

The Sum rule sums the values of a field across all records in a section and validates that the sum matches a specified value or a value from another field.

```yaml
global_rules:
  - type: sum
    name: salary_sum
    params:
      section: body
      field: salary
      sum_field: footer.total_salary
      insert_value: true  # Insert the calculated sum into the target field
      target_field: footer.total_salary
      include_invalid_records: false  # Only include valid records in the sum
```

### Checksum Rule

The Checksum rule calculates a checksum of field values and validates that the checksum matches a specified value or a value from another field. This rule supports three modes of operation:

1. **Single Column Checksum**: Calculates a checksum of a single field across all records
2. **Multi-Column Checksum**: Calculates a checksum of multiple fields combined
3. **Row Checksum**: Calculates a checksum of all fields in a record (row-based)

#### Supported Checksum Types

The Checksum rule supports the following checksum algorithms:

- **sum**: Adds the ASCII values of all characters in the input value(s)
- **xor**: Performs XOR operation on the ASCII values of all characters
- **mod10**: Modulo 10 checksum (Luhn algorithm), often used for credit card validation
- **md5**: MD5 hash algorithm, generates a 32-character hexadecimal digest
- **SHA256**: SHA-256 hash algorithm, generates a 64-character hexadecimal digest

#### Single Column Checksum (Legacy)

```yaml
global_rules:
  - type: checksum
    name: data_checksum
    params:
      section: body
      field: data
      type: md5  # Can be sum, xor, mod10, or md5
      checksum_field: footer.checksum
      insert_value: true  # Insert the calculated checksum into the target field
      target_field: footer.checksum
      include_invalid_records: false  # Only include valid records in the checksum
```

#### Multi-Column Checksum

```yaml
global_rules:
  - type: checksum
    name: multi_column_checksum
    params:
      section: body
      validation_type: multi_column
      columns:
        - customer_id
        - order_id
        - amount
      algorithm: SHA256  # MD5 or SHA256
      target_field: checksum_field
      insert_value: false  # Whether to insert the calculated value
```

#### Row Checksum

```yaml
global_rules:
  - type: checksum
    name: row_checksum
    params:
      section: body
      validation_type: row
      algorithm: SHA256  # MD5 or SHA256
      target_field: row_checksum
      insert_value: false  # Whether to insert the calculated value
```

#### Parameters

The Checksum rule supports the following parameters:

- **Common Parameters**:
  - `section`: The section to apply the rule to
  - `include_invalid_records`: Whether to include invalid records in the calculation (default: false)
  - `insert_value`: Whether to insert the calculated value into a target field (default: false)
  - `target_field`: The field to insert the calculated value into
  - `expected_checksum`: The expected checksum value for validation

- **Single Column Parameters**:
  - `field`: The field to calculate the checksum for
  - `type`: The checksum algorithm type (sum, xor, mod10, md5)
  - `checksum_field`: The field containing the expected checksum (legacy parameter)

- **Multi-Column Parameters**:
  - `validation_type`: Set to "multi_column" for multi-column checksum
  - `columns`: List of fields to include in the checksum calculation
  - `algorithm`: Hash algorithm to use (MD5 or SHA256)

- **Row Parameters**:
  - `validation_type`: Set to "row" for row-based checksum
  - `algorithm`: Hash algorithm to use (MD5 or SHA256)

### Uniqueness Rule

The Uniqueness rule validates that the values of a field or a combination of fields are unique across all records in a section.

```yaml
global_rules:
  - type: uniqueness
    name: unique_employee_id
    params:
      section: body
      fields: employee_id  # Single field uniqueness check
```

For composite uniqueness (checking uniqueness across multiple fields):

```yaml
global_rules:
  - type: uniqueness
    name: unique_employee_name_country
    params:
      section: body
      fields:  # Composite field uniqueness check
        - employee_name
        - country_code
```

## Global Rule Parameters

All global rules support the following common parameters:

- `section`: The section to apply the rule to.
- `include_invalid_records`: Whether to include invalid records in the rule calculation. Default is `false`.
- `insert_value`: Whether to insert the calculated value into a target field. Default is `false`.
- `target_field`: The field to insert the calculated value into, in the format `section.field`.

## Aborting Processing After N Errors

FlatForge supports aborting processing after a specified number of errors. This is configured at the file format level:

```yaml
name: Employee CSV Format
type: delimited
abort_after_n_failed_records: 5  # Abort processing after 5 failed records
# ... other file format parameters ...
```

Setting `abort_after_n_failed_records` to `-1` means that the processor will process the entire file regardless of the number of failed records.

## Example Configuration

Here's a complete example of a file format configuration with global rules:

```yaml
name: Employee CSV Format with Global Rules
type: delimited
description: A CSV file format for employee data with global rules for validation and insertion
delimiter: ","
quote_char: "\""
escape_char: "\\"
newline: "\n"
encoding: utf-8
skip_blank_lines: true
exit_on_first_error: false
abort_after_n_failed_records: 5  # Abort processing after 5 failed records

sections:
  # ... section definitions ...

global_rules:
  - type: sum
    name: salary_sum
    params:
      section: body
      field: salary
      sum_field: footer.total_salary
      insert_value: true  # Insert the calculated sum into the target field
      target_field: footer.total_salary
      include_invalid_records: false  # Only include valid records in the sum
  
  - type: count
    name: employee_count
    params:
      section: body
      count_field: footer.employee_count
      insert_value: true  # Insert the calculated count into the target field
      target_field: footer.employee_count
      include_invalid_records: false  # Only include valid records in the count
  
  - type: uniqueness
    name: unique_employee_id
    params:
      section: body
      fields: employee_id  # Single field uniqueness check
  
  - type: uniqueness
    name: unique_employee_name_country
    params:
      section: body
      fields:  # Composite field uniqueness check
        - employee_name
        - country_code
``` 