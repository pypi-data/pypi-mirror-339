from datetime import datetime
from flatforge.core import FieldValue, ParsedRecord
from flatforge.transformers.base import TransformerRule

class DateFormatRule(TransformerRule):
    """A transformer that changes the format of a date string.

    Example:
        Input: "20240315"
        Output: "15-03-2024" (with input_format="%Y%m%d", output_format="%d-%m-%Y")
    """

    def __init__(self, config: dict):
        """Initialize the transformer.

        Args:
            config (dict): Configuration dictionary containing:
                - input_format (str): The format of the input date string.
                - output_format (str): The desired format for the output date string.
        """
        super().__init__("date_format", config)
        self.input_format = config.get("input_format")
        self.output_format = config.get("output_format")
        if not self.input_format or not self.output_format:
            raise ValueError("Both input_format and output_format must be specified")

    def transform(self, field_value: FieldValue, parsed_record: ParsedRecord) -> str:
        """Transform a date string from one format to another.

        Args:
            field_value (FieldValue): The field value to transform.
            parsed_record (ParsedRecord): The parsed record containing all field values.

        Returns:
            str: The date string in the new format.
        """
        value = field_value.value
        if not value:
            return value

        try:
            date = datetime.strptime(value, self.input_format)
            return date.strftime(self.output_format)
        except ValueError:
            return value  # Return original value if parsing fails 