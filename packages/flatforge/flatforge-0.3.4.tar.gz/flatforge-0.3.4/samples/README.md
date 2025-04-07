# FlatForge v0.3.1 Sample Files

This directory contains sample files demonstrating the new features in FlatForge v0.3.1.

## New Features

### 1. Credit Card Validation
The `LuhnValidationRule` validates credit card numbers using the Luhn algorithm. It supports various card formats and handles spaces and hyphens.

Example configuration:
```json
{
    "type": "luhn",
    "column": "card_number",
    "strip_spaces": true,
    "strip_hyphens": true,
    "error_message": "Invalid credit card number"
}
```

### 2. GUID Validation
The `GuidValidationRule` validates GUIDs (Globally Unique Identifiers) in various formats, including standard UUID, no-hyphen, uppercase, and URN formats.

Example configuration:
```json
{
    "type": "guid",
    "column": "transaction_id",
    "strip_spaces": true,
    "strip_hyphens": true,
    "error_message": "Invalid transaction ID"
}
```

### 3. Value Resolution
The `ValueResolverTransformationRule` transforms values using a mapping file. It's useful for standardizing status codes, categories, or other enumerated values.

Example configuration:
```json
{
    "type": "value_resolver",
    "source_field": "status",
    "target_field": "status_code",
    "mapping_file": "config/status_mapping.json",
    "default_value": "UNKNOWN"
}
```

### 4. Encoding Transformation
The `EncodingTransformation` class handles file encoding transformations between different character encodings.

Example configuration:
```json
{
    "input_encoding": "iso-8859-1",
    "output_encoding": "utf-8",
    "errors": "strict"
}
```

## Sample Files

1. `test_features_v0.3.1.py`: A comprehensive test script demonstrating all new features
2. `config/features_v0.3.1.json`: A sample configuration file showing how to use the new features
3. `config/status_mapping.json`: A sample mapping file for value resolution

## Running the Tests

To run the sample tests:

```bash
python test_features_v0.3.1.py
```

The test script will demonstrate:
- Credit card validation with various formats
- GUID validation with different formats
- Value resolution using a mapping file
- File encoding transformation

## Configuration Guide

### File Settings
```json
{
    "file_settings": {
        "input_file": "data/input.csv",
        "output_file": "data/output.csv",
        "input_encoding": "iso-8859-1",
        "output_encoding": "utf-8",
        "delimiter": ",",
        "has_header": true
    }
}
```

### Sections
Sections define different parts of the file with their own rules and transformations:
```json
{
    "sections": [
        {
            "name": "header",
            "start_line": 1,
            "end_line": 1,
            "rules": [...]
        },
        {
            "name": "transactions",
            "start_line": 2,
            "end_line": -1,
            "rules": [...],
            "transformations": [...]
        }
    ]
}
```

### Global Rules
Global rules apply to all records in the file:
```json
{
    "global_rules": [
        {
            "type": "checksum",
            "algorithm": "sha256",
            "columns": ["transaction_id", "card_number", "amount"],
            "target_column": "record_checksum"
        }
    ]
}
```

## Error Handling

The new features include comprehensive error handling:
- Invalid credit card numbers
- Malformed GUIDs
- Missing mapping files
- Encoding errors
- Missing required fields

Each validation rule provides detailed error messages to help identify issues. 