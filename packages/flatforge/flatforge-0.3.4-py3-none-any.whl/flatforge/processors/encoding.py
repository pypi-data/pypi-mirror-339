"""File encoding transformation functionality."""

class EncodingTransformation:
    """Transforms file encoding from one format to another.
    
    Configuration parameters:
        input_encoding (str): Source file encoding (e.g., 'iso-8859-1', 'utf-8')
        output_encoding (str): Target file encoding (e.g., 'utf-8', 'ascii')
        errors (str): How to handle encoding errors (default: 'strict')
            - 'strict': Raise an error for invalid characters
            - 'replace': Replace invalid characters with a replacement character
            - 'ignore': Skip invalid characters
    """
    
    def __init__(self, config):
        """Initialize the encoding transformation.
        
        Args:
            config (dict): Configuration dictionary containing transformation parameters
            
        Raises:
            ValueError: If required parameters are missing
        """
        self.input_encoding = config.get('input_encoding')
        self.output_encoding = config.get('output_encoding')
        self.errors = config.get('errors', 'strict')
        
        if not self.input_encoding or not self.output_encoding:
            raise ValueError("input_encoding and output_encoding are required")
            
    def transform(self, input_file, output_file):
        """Transform file encoding from input to output format.
        
        Args:
            input_file (str): Path to the input file
            output_file (str): Path to the output file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            LookupError: If encoding is not supported
            UnicodeError: If encoding errors occur and errors='strict'
        """
        # Read input file with specified encoding
        with open(input_file, 'r', encoding=self.input_encoding, errors=self.errors) as f:
            content = f.read()
            
        # Write output file with specified encoding
        with open(output_file, 'w', encoding=self.output_encoding, errors=self.errors) as f:
            f.write(content) 