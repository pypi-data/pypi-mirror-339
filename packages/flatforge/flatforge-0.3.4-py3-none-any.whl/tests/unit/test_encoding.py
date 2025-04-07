import unittest
import os
import tempfile
from flatforge.parsers.file_parser import FileParser

class TestEncodingTransformation(unittest.TestCase):
    def setUp(self):
        """Set up test files."""
        # Create temporary input file with non-ASCII characters
        self.input_file = tempfile.NamedTemporaryFile(delete=False, mode='wb')
        # Write content in ISO-8859-1 encoding
        self.input_file.write('Café,Résumé,Déjà vu'.encode('iso-8859-1'))
        self.input_file.close()
        
        # Output file path
        self.output_file = tempfile.NamedTemporaryFile(delete=False).name
        
        # Basic config
        self.config = {
            'file_settings': {
                'input_encoding': 'iso-8859-1',
                'output_encoding': 'utf-8'
            },
            'sections': [
                {
                    'name': 'body',
                    'fields': [
                        {'name': 'field1'},
                        {'name': 'field2'},
                        {'name': 'field3'}
                    ]
                }
            ]
        }
        
    def tearDown(self):
        """Clean up test files."""
        try:
            os.unlink(self.input_file.name)
            os.unlink(self.output_file)
        except:
            pass
            
    def test_encoding_transformation(self):
        """Test transformation between encodings."""
        parser = FileParser(self.config, self.input_file.name, self.output_file)
        parser.parse_file()
        
        # Read output file in UTF-8
        with open(self.output_file, 'r', encoding='utf-8') as f:
            output_content = f.read()
            
        # Verify content was properly encoded
        self.assertEqual(output_content, 'Café,Résumé,Déjà vu')
        
        # Compare binary content to ensure encoding changed
        with open(self.input_file.name, 'rb') as f:
            input_binary = f.read()
        with open(self.output_file, 'rb') as f:
            output_binary = f.read()
            
        # The binary representation should be different due to encoding change
        self.assertNotEqual(input_binary, output_binary) 