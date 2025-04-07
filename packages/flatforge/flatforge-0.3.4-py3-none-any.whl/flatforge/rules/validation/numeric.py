"""
Numeric validation rule for FlatForge.

This module contains the NumericRule class that validates that a field is numeric
and performs additional checks on numeric values.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class NumericRule(ValidationRule):
    """
    Rule that validates that a field contains a valid numeric value.
    
    This rule checks if a field contains a valid numeric value (integer or floating point)
    and can perform additional validations such as:
    - Ensuring the value falls within a specified range (min_value, max_value)
    - Checking the decimal precision of floating point values
    
    Parameters:
        min_value (optional): Minimum allowed value (inclusive)
        max_value (optional): Maximum allowed value (inclusive)
        decimal_precision (optional): Maximum number of decimal places allowed
    """
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate that a field contains a valid numeric value with additional constraints.
        
        This method performs the following checks:
        1. Ensures the value is a valid number (integer or float)
        2. For floating point values, checks decimal precision if specified
        3. Validates that the value is within the specified range (min_value/max_value)
        
        Empty values are allowed by default. Use a RequiredRule in combination with
        this rule to enforce non-empty values.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field is not numeric or fails additional constraints
        """
        value = field_value.value.strip()
        
        # Empty values are allowed (use RequiredRule to enforce non-empty)
        if not value:
            return
            
        # Check if the value is numeric
        try:
            # Handle decimal values
            if "." in value:
                float_value = float(value)
                
                # Check decimal precision if specified
                if "decimal_precision" in self.params:
                    decimal_precision = self.params["decimal_precision"]
                    decimal_part = value.split(".")[1]
                    if len(decimal_part) > decimal_precision:
                        raise ValidationError(
                            f"Value has more than {decimal_precision} decimal places",
                            field_name=field_value.field.name,
                            value=value,
                            rule_name=self.name
                        )
                        
                # Check min value if specified
                if "min_value" in self.params and float_value < float(self.params["min_value"]):
                    raise ValidationError(
                        f"Value is less than minimum value {self.params['min_value']}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
                    
                # Check max value if specified
                if "max_value" in self.params and float_value > float(self.params["max_value"]):
                    raise ValidationError(
                        f"Value is greater than maximum value {self.params['max_value']}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
            else:
                # Integer value
                int_value = int(value)
                
                # Check min value if specified
                if "min_value" in self.params and int_value < int(self.params["min_value"]):
                    raise ValidationError(
                        f"Value is less than minimum value {self.params['min_value']}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
                    
                # Check max value if specified
                if "max_value" in self.params and int_value > int(self.params["max_value"]):
                    raise ValidationError(
                        f"Value is greater than maximum value {self.params['max_value']}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
        except (ValueError, TypeError):
            raise ValidationError(
                "Value is not numeric",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            ) 