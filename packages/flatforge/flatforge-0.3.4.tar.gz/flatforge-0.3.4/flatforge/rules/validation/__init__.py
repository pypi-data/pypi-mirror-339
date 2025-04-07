"""
Validation rules package for FlatForge.

This package contains all validation rules used for validating field values.
"""
from flatforge.rules.validation.required import RequiredRule
from flatforge.rules.validation.numeric import NumericRule
from flatforge.rules.validation.string_length import StringLengthRule
from flatforge.rules.validation.regex import RegexRule
from flatforge.rules.validation.date import DateRule
from flatforge.rules.validation.choice import ChoiceRule
from flatforge.rules.validation.luhn import LuhnRule
from flatforge.rules.validation.guid import GuidRule
from flatforge.rules.validation.factory import ValidationRuleFactory

# Backward compatibility aliases with custom constructor wrappers
class GuidValidationRule(GuidRule):
    """
    A rule for validating GUIDs, with backward compatibility support.
    
    This class can be instantiated in two ways:
    1. Old style: GuidValidationRule(config_dict)  
    2. New style: GuidValidationRule(name, config_dict)
    
    Parameters are extracted from the config dictionary either way.
    """
    def __init__(self, name_or_config, config=None):
        """
        Initialize a GuidValidationRule with backward compatibility support.
        
        Args:
            name_or_config: Either the rule name (str) or a config dictionary
            config: The configuration dictionary (when name is provided)
        """
        # Handle both constructor patterns
        if config is None:
            # Old style: GuidValidationRule(config_dict)
            config = name_or_config
            name = "guid_rule"
        else:
            # New style: GuidValidationRule(name, config_dict)
            name = name_or_config
            
        # Extract parameters from config - we'll pass these in params
        params = config.copy()
        
        # Make sure 'field' is available in params if 'column' is used
        if 'column' in params and 'field' not in params:
            params['field'] = params['column']
            
        # Initialize the parent class
        super().__init__(name, params)

class LuhnValidationRule(LuhnRule):
    """
    A rule for validating credit card numbers using the Luhn algorithm, with backward compatibility support.
    
    This class can be instantiated in two ways:
    1. Old style: LuhnValidationRule(config_dict)
    2. New style: LuhnValidationRule(name, config_dict)
    
    Parameters are extracted from the config dictionary either way.
    """
    def __init__(self, name_or_config, config=None):
        """
        Initialize a LuhnValidationRule with backward compatibility support.
        
        Args:
            name_or_config: Either the rule name (str) or a config dictionary
            config: The configuration dictionary (when name is provided)
        """
        # Handle both constructor patterns
        if config is None:
            # Old style: LuhnValidationRule(config_dict)
            config = name_or_config
            name = "luhn_rule"
        else:
            # New style: LuhnValidationRule(name, config_dict)
            name = name_or_config
            
        # Extract parameters from config - we'll pass these in params
        params = config.copy()
        
        # Make sure 'field' is available in params if 'column' is used
        if 'column' in params and 'field' not in params:
            params['field'] = params['column']
            
        # Initialize the parent class
        super().__init__(name, params)

__all__ = [
    'RequiredRule',
    'NumericRule',
    'StringLengthRule',
    'RegexRule',
    'DateRule',
    'ChoiceRule',
    'LuhnRule',
    'GuidRule',
    'GuidValidationRule',  # Backward compatibility
    'LuhnValidationRule',  # Backward compatibility
    'ValidationRuleFactory',
] 