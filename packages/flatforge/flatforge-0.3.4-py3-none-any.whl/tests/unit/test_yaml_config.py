import unittest
import yaml
import os
from flatforge.config import Config

class TestYamlConfig(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.config_path = os.path.join('samples', 'config', 'features_v0.3.1.yaml')
        
    def test_yaml_format(self):
        """Test that the YAML file is properly formatted."""
        with open(self.config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            
        # Verify basic structure
        self.assertIn('file_settings', config_data)
        self.assertIn('sections', config_data)
        self.assertIn('global_rules', config_data)
        
        # Verify file settings
        file_settings = config_data['file_settings']
        self.assertEqual(file_settings['input_file'], 'data/input.csv')
        self.assertEqual(file_settings['output_file'], 'data/output.csv')
        self.assertEqual(file_settings['input_encoding'], 'iso-8859-1')
        self.assertEqual(file_settings['output_encoding'], 'utf-8')
        self.assertEqual(file_settings['delimiter'], ',')
        self.assertTrue(file_settings['has_header'])
        
        # Verify sections
        sections = config_data['sections']
        self.assertEqual(len(sections), 2)
        
        # Verify header section
        header_section = sections[0]
        self.assertEqual(header_section['name'], 'header')
        self.assertEqual(header_section['start_line'], 1)
        self.assertEqual(header_section['end_line'], 1)
        self.assertEqual(len(header_section['rules']), 1)
        
        # Verify transactions section
        transactions_section = sections[1]
        self.assertEqual(transactions_section['name'], 'transactions')
        self.assertEqual(transactions_section['start_line'], 2)
        self.assertEqual(transactions_section['end_line'], -1)
        self.assertEqual(len(transactions_section['rules']), 2)
        self.assertEqual(len(transactions_section['transformations']), 1)
        
        # Verify global rules
        global_rules = config_data['global_rules']
        self.assertEqual(len(global_rules), 1)
        
    def test_config_loading(self):
        """Test that the YAML config can be loaded by FlatForge's Config class."""
        config = Config(self.config_path)
        
        # Verify file settings
        self.assertEqual(config.file_settings.input_file, 'data/input.csv')
        self.assertEqual(config.file_settings.output_file, 'data/output.csv')
        self.assertEqual(config.file_settings.input_encoding, 'iso-8859-1')
        self.assertEqual(config.file_settings.output_encoding, 'utf-8')
        self.assertEqual(config.file_settings.delimiter, ',')
        self.assertTrue(config.file_settings.has_header)
        
        # Verify sections
        self.assertEqual(len(config.sections), 2)
        
        # Verify header section
        header_section = config.sections[0]
        self.assertEqual(header_section.name, 'header')
        self.assertEqual(header_section.start_line, 1)
        self.assertEqual(header_section.end_line, 1)
        self.assertEqual(len(header_section.rules), 1)
        
        # Verify transactions section
        transactions_section = config.sections[1]
        self.assertEqual(transactions_section.name, 'transactions')
        self.assertEqual(transactions_section.start_line, 2)
        self.assertEqual(transactions_section.end_line, -1)
        self.assertEqual(len(transactions_section.rules), 2)
        self.assertEqual(len(transactions_section.transformations), 1)
        
        # Verify global rules
        self.assertEqual(len(config.global_rules), 1) 