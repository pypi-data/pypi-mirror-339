import unittest
import tempfile
import os
from flatforge.processors.encoding import EncodingTransformation

class TestEncodingTransformation(unittest.TestCase):
    def setUp(self):
        """Set up test files."""
        # Create temporary input file with ISO-8859-1 encoded content
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write('Café,Résumé,Déjà vu'.encode('iso-8859-1'))
            self.input_file_path = f.name
            
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            self.output_file_path = f.name
        
    def tearDown(self):
        """Clean up test files."""
        try:
            os.unlink(self.input_file_path)
        except (OSError, AttributeError):
            pass
            
        try:
            os.unlink(self.output_file_path)
        except (OSError, AttributeError):
            pass
        
    def test_iso_to_utf8(self):
        """Test transformation from ISO-8859-1 to UTF-8."""
        config = {
            'input_encoding': 'iso-8859-1',
            'output_encoding': 'utf-8'
        }
        
        transformer = EncodingTransformation(config)
        transformer.transform(self.input_file_path, self.output_file_path)
        
        # Read the output file and verify encoding
        with open(self.output_file_path, 'rb') as f:
            output_content = f.read()
            
        # Verify the content is properly encoded in UTF-8
        self.assertEqual(output_content.decode('utf-8'), 'Café,Résumé,Déjà vu')
        
    def test_utf8_to_ascii(self):
        """Test transformation from UTF-8 to ASCII with replacement."""
        config = {
            'input_encoding': 'utf-8',
            'output_encoding': 'ascii',
            'errors': 'replace'
        }
        
        # Create a UTF-8 input file
        with open(self.input_file_path, 'w', encoding='utf-8') as f:
            f.write('Café,Résumé,Déjà vu')
            
        transformer = EncodingTransformation(config)
        transformer.transform(self.input_file_path, self.output_file_path)
        
        # Read the output file and verify encoding
        with open(self.output_file_path, 'rb') as f:
            output_content = f.read()
            
        # Verify the content is properly encoded in ASCII with replacements
        self.assertEqual(output_content.decode('ascii'), 'Caf?,R?sum?,D?j? vu')
        
    def test_invalid_encoding(self):
        """Test handling of invalid encoding."""
        config = {
            'input_encoding': 'invalid-encoding',
            'output_encoding': 'utf-8'
        }
        
        transformer = EncodingTransformation(config)
        with self.assertRaises(LookupError):
            transformer.transform(self.input_file_path, self.output_file_path)
            
    def test_missing_parameters(self):
        """Test handling of missing configuration parameters."""
        config = {
            'input_encoding': 'utf-8'
            # Missing output_encoding
        }
        
        with self.assertRaises(ValueError) as cm:
            EncodingTransformation(config)
        self.assertEqual(str(cm.exception), "input_encoding and output_encoding are required")
        
        config = {
            'output_encoding': 'utf-8'
            # Missing input_encoding
        }
        
        with self.assertRaises(ValueError) as cm:
            EncodingTransformation(config)
        self.assertEqual(str(cm.exception), "input_encoding and output_encoding are required")
        
        config = {}  # Both missing
        
        with self.assertRaises(ValueError) as cm:
            EncodingTransformation(config)
        self.assertEqual(str(cm.exception), "input_encoding and output_encoding are required")
        
    def test_nonexistent_file(self):
        """Test handling of nonexistent input file."""
        config = {
            'input_encoding': 'utf-8',
            'output_encoding': 'ascii'
        }
        
        transformer = EncodingTransformation(config)
        with self.assertRaises(FileNotFoundError):
            transformer.transform('nonexistent.txt', self.output_file_path) 