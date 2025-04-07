"""
Luhn transformer for FlatForge.

This module contains the LuhnTransformer for computing and appending Luhn check digits.
"""
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule


class LuhnTransformer(TransformerRule):
    """A transformer that appends a check digit to a numeric string using the Luhn algorithm.

    Example:
        Input: "453201511283036"
        Output: "4532015112830368"
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """Initialize the transformer.

        Args:
            name (str): The name of the transformer.
            config (Dict[str, Any]): Configuration dictionary (not used for this transformer).
        """
        super().__init__(name, config)

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a numeric string by appending a check digit using the Luhn algorithm.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The transformed value with the check digit appended.
        """
        value = field_value.value
        if not value or not value.strip():
            return value

        # Remove any spaces or dashes from the input
        digits = value.replace(" ", "").replace("-", "")
        if not digits.isdigit():
            return value

        # Check if the input is already a valid Luhn number
        if self._is_valid_luhn(digits):
            return value

        # If not valid, append a check digit
        check_digit = self._calculate_check_digit(digits)
        return value + str(check_digit)

    def _calculate_check_digit(self, digits: str) -> int:
        """Calculate the check digit for a numeric string using the Luhn algorithm.

        Args:
            digits (str): The numeric string to calculate the check digit for.

        Returns:
            int: The calculated check digit.
        """
        total = 0
        for i in range(len(digits)):
            digit = int(digits[-(i + 1)])  # Start from the rightmost digit
            if i % 2 == 1:  # Double every second digit from the right
                doubled = digit * 2
                total += doubled // 10 + doubled % 10  # Add digits if doubled > 9
            else:
                total += digit

        check_digit = (10 - (total % 10)) % 10
        return check_digit

    def _is_valid_luhn(self, digits: str) -> bool:
        """Check if a numeric string is a valid Luhn number.

        Args:
            digits (str): The numeric string to check.

        Returns:
            bool: True if the string is a valid Luhn number.
        """
        total = 0
        for i in range(len(digits)):
            digit = int(digits[-(i + 1)])  # Start from the rightmost digit
            if i % 2 == 1:  # Double every second digit from the right
                doubled = digit * 2
                total += doubled // 10 + doubled % 10  # Add digits if doubled > 9
            else:
                total += digit

        return total % 10 == 0 