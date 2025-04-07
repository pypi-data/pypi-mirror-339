import unittest
from flatforge.rules.transformation import MaskTransformationRule

class TestMaskTransformation(unittest.TestCase):
    def test_start_index_mask_length(self):
        """Test masking with start_index and mask_length."""
        config = {
            'source_field': 'card_number',
            'target_field': 'masked_card',
            'mask_char': '*',
            'start_index': 6,
            'mask_length': 6
        }
        rule = MaskTransformationRule(config)
        
        record = {'card_number': '4111111111111111'}
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(transformed['masked_card'], '411111******1111')
        
    def test_keep_first_last(self):
        """Test masking with keep_first and keep_last."""
        config = {
            'source_field': 'card_number',
            'target_field': 'masked_card',
            'mask_char': 'X',
            'keep_first': 4,
            'keep_last': 4
        }
        rule = MaskTransformationRule(config)
        
        record = {'card_number': '4111111111111111'}
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)
        self.assertEqual(transformed['masked_card'], '4111XXXXXXXX1111')
        
    def test_in_place_masking(self):
        """Test in-place masking (source = target)."""
        config = {
            'source_field': 'card_number',
            'mask_char': '#',
            'keep_first': 6,
            'keep_last': 4
        }
        rule = MaskTransformationRule(config)
        
        record = {'card_number': '4111111111111111'}
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)
        self.assertEqual(transformed['card_number'], '411111######1111')
        
    def test_short_string(self):
        """Test masking a string that's too short."""
        config = {
            'source_field': 'card_number',
            'target_field': 'masked_card',
            'keep_first': 2,
            'keep_last': 2
        }
        rule = MaskTransformationRule(config)
        
        record = {'card_number': '1234'}
        transformed, success, error = rule.transform(record)
        
        self.assertTrue(success)
        # With keep_first=2 and keep_last=2 on a 4-char string, no masking should occur
        self.assertEqual(transformed['masked_card'], '1234') 