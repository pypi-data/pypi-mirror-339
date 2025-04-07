# Configuration Validation

FlatForge provides a configuration validation tool to help you catch errors in your configuration files before processing any data. This feature allows you to validate your YAML or JSON configuration files against FlatForge's schema and domain-specific rules.

## Using the CLI

The easiest way to validate a configuration file is using the command-line interface:

```bash
flatforge validate-config --config my_config.yaml
```

This will check your configuration file against FlatForge's schema and domain-specific rules, reporting any errors found.

### Options

- `--config`: Path to the configuration file to validate (required)
- `--schema`: Path to a custom JSON schema file (optional)

## Programmatic Validation

You can also validate configuration files programmatically in your Python code:

```python
from flatforge.validators import ConfigValidator

# Validate from a file
validator = ConfigValidator.from_file("my_config.yaml")
is_valid = validator.validate()

if not is_valid:
    for error in validator.errors:
        print(f"Error: {error}")
```

If you already have a configuration loaded as a Python dictionary, you can validate it directly:

```python
import yaml
from flatforge.validators import ConfigValidator

# Load configuration from a file
with open("my_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Validate the configuration
validator = ConfigValidator(config)
is_valid = validator.validate()

if not is_valid:
    for error in validator.errors:
        print(f"Error: {error}")
```

## Types of Validations

The validator performs two types of validations:

1. **Schema Validation**: Ensures that the configuration file conforms to the expected structure and data types defined in the JSON schema.

2. **Domain-Specific Validation**: Performs additional validations that cannot be expressed in a JSON schema, such as:
   - Checking for overlapping fields in fixed-length formats
   - Validating field position and length requirements
   - Ensuring rule references are valid
   - Verifying field names are unique within a record
   - Checking sections for correct constraints (e.g., min_records ≤ max_records)
   - Validating global rule parameters
   - Ensuring field references in global rules point to existing fields
 
## Common Validation Errors

### Schema Validation Errors

These errors occur when the configuration file doesn't conform to the expected structure:

- Missing required properties (e.g., `name`, `type`, `sections`)
- Invalid types (e.g., strings where numbers are expected)
- Unknown properties
- Invalid values for enum properties (e.g., `type` must be `fixed_length` or `delimited`)

Example error messages:
```
Schema error at type: 'fixed' is not one of ['fixed_length', 'delimited']
Schema error at sections.0.record: 'fields' is a required property
```

### Domain-Specific Validation Errors

These errors occur when the configuration file has logical or relational issues:

- Overlapping fields in fixed-length formats
- Invalid rule types or parameters
- Duplicate field names in a record
- References to non-existent fields in global rules
- Section constraints violations

Example error messages:
```
Field 'last_name' at position 15 overlaps with field 'first_name'
Global sum rule 'salary_sum' references non-existent field: footer.total_salary
In field 'age', string_length rule has min_length (10) > max_length (5)
Section 'header' has min_records (2) > max_records (1)
```

## Pre-Processing Validation

It's a good practice to validate your configuration files before processing any data. This can be done as part of your processing pipeline:

```python
from flatforge.validators import ConfigValidator
from flatforge.core import FileFormat
from flatforge.processors import ValidationProcessor

# Validate the configuration first
validator = ConfigValidator.from_file("my_config.yaml")
if not validator.validate():
    print("Configuration is invalid:")
    for error in validator.errors:
        print(f"- {error}")
    exit(1)

# If validation passed, continue with processing
file_format = FileFormat.from_yaml("my_config.yaml")
processor = ValidationProcessor(file_format)
result = processor.process("input.txt", "output.txt", "errors.txt")
```

## Using Custom JSON Schema

You can provide your own JSON schema file if you need to customize the validation requirements:

```bash
flatforge validate-config --config my_config.yaml --schema my_custom_schema.json
```

Or programmatically:

```python
from flatforge.validators import ConfigValidator

validator = ConfigValidator.from_file("my_config.yaml", schema_path="my_custom_schema.json")
is_valid = validator.validate()
```

## Best Practices

1. **Validate Early**: Validate your configuration files during development and before deploying to production.

2. **Use Version Control**: Track changes to your configuration files using version control, and validate after each change.

3. **Automate Validation**: Include validation in your CI/CD pipeline to prevent invalid configurations from being deployed.

4. **Document Your Configurations**: Add comments and descriptions to your configuration files to make them more maintainable.

5. **Maintain a Test Suite**: Create a test suite of valid and invalid configuration files to verify the validation logic.

By validating your configuration files before processing, you can catch errors early and avoid runtime issues, saving time and resources. 