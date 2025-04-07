"""
Domain validator module for FlatForge.

This module contains the domain validator class used to validate
configuration files against domain-specific rules.
"""
from typing import Dict, List, Any, Set


class DomainValidator:
    """
    Domain validator for FlatForge configuration files.
    
    This class validates a configuration against domain-specific rules that
    cannot be expressed in a JSON schema.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize a domain validator.
        
        Args:
            config: The configuration to validate
        """
        self.config = config
        
    def validate(self) -> List[str]:
        """
        Validate a configuration against domain-specific rules.
        
        Returns:
            A list of error messages, or an empty list if validation succeeds
        """
        errors = []
        
        errors.extend(self._validate_file_structure())
        errors.extend(self._validate_field_positions())
        errors.extend(self._validate_rule_references())
        errors.extend(self._validate_field_names())
        errors.extend(self._validate_global_rules())
        errors.extend(self._validate_section_constraints())
        
        return errors
    
    def _validate_file_structure(self) -> List[str]:
        """
        Validate the structure of the file format.
        
        Returns:
            A list of error messages
        """
        errors = []
        
        # Check that the file format has the correct number of sections of each type
        sections = self.config.get('sections', [])
        section_types = {'header': 0, 'body': 0, 'footer': 0}
        
        for section in sections:
            section_type = section.get('type')
            if section_type in section_types:
                section_types[section_type] += 1
        
        # Validate that there is at least one body section
        if section_types['body'] == 0:
            errors.append("File format must have at least one body section")
            
        # Validate that there is at most one header section
        if section_types['header'] > 1:
            errors.append("File format can have at most one header section")
            
        # Validate that there is at most one footer section
        if section_types['footer'] > 1:
            errors.append("File format can have at most one footer section")
        
        return errors
    
    def _validate_field_positions(self) -> List[str]:
        """
        Validate field positions in fixed-length files.
        
        Returns:
            A list of error messages
        """
        errors = []
        
        # Only check for fixed-length files
        if self.config.get('type') != 'fixed_length':
            return errors
        
        # Check for overlapping fields in each record
        for section in self.config.get('sections', []):
            if 'record' not in section:
                continue
                
            record = section['record']
            if 'fields' not in record:
                continue
                
            fields = record['fields']
            field_ranges = {}
            
            for field in fields:
                if 'position' not in field or 'length' not in field:
                    continue
                    
                name = field.get('name', 'Unknown')
                position = field['position']
                length = field['length']
                
                # Check for field overlap
                for pos in range(position, position + length):
                    if pos in field_ranges:
                        errors.append(f"Field '{name}' at position {pos} overlaps with field '{field_ranges[pos]}'")
                    else:
                        field_ranges[pos] = name
        
        return errors
    
    def _validate_rule_references(self) -> List[str]:
        """
        Validate rule references and parameters.
        
        Returns:
            A list of error messages
        """
        errors = []
        
        # Validation rule types
        validation_rules = [
            'required', 'string_length', 'numeric', 'date', 'regex', 
            'choice', 'luhn'
        ]
        
        # Transformation rule types
        transformation_rules = [
            'trim', 'case', 'pad', 'date_format', 'substring', 'replace', 
            'value_resolver', 'mask', 'guid'
        ]
        
        # Global rule types
        global_rule_types = ['count', 'sum', 'checksum', 'uniqueness']
        
        # Validate field rules
        for section in self.config.get('sections', []):
            if 'record' not in section:
                continue
                
            record = section['record']
            if 'fields' not in record:
                continue
                
            for field in record['fields']:
                if 'rules' not in field:
                    continue
                    
                for rule in field['rules']:
                    if 'type' not in rule:
                        errors.append(f"Rule in field '{field.get('name', 'Unknown')}' is missing 'type'")
                        continue
                        
                    rule_type = rule['type']
                    
                    # Check if rule type is valid
                    if rule_type not in validation_rules and rule_type not in transformation_rules:
                        errors.append(f"Invalid rule type '{rule_type}' in field '{field.get('name', 'Unknown')}'")
                        
                    # Check for rule-specific parameters
                    if rule_type == 'string_length' and 'params' in rule:
                        params = rule['params']
                        if 'min_length' in params and 'max_length' in params:
                            min_len = params['min_length']
                            max_len = params['max_length']
                            if min_len > max_len:
                                errors.append(
                                    f"In field '{field.get('name', 'Unknown')}', "
                                    f"string_length rule has min_length ({min_len}) > max_length ({max_len})"
                                )
        
        # Validate global rules
        for rule in self.config.get('global_rules', []):
            if 'type' not in rule:
                errors.append("Global rule is missing 'type'")
                continue
                
            rule_type = rule['type']
            
            # Check if global rule type is valid
            if rule_type not in global_rule_types:
                errors.append(f"Invalid global rule type: {rule_type}")
                
            # Check for required parameters
            if rule_type == 'count' and 'params' in rule:
                params = rule['params']
                if 'section' not in params:
                    errors.append(f"Global count rule '{rule.get('name', rule_type)}' is missing required parameter: section")
            
            if rule_type == 'sum' and 'params' in rule:
                params = rule['params']
                if 'field' not in params:
                    errors.append(f"Global sum rule '{rule.get('name', rule_type)}' is missing required parameter: field")
                if 'section' not in params:
                    errors.append(f"Global sum rule '{rule.get('name', rule_type)}' is missing required parameter: section")
            
            if rule_type == 'uniqueness' and 'params' in rule:
                params = rule['params']
                if 'field' not in params and 'fields' not in params:
                    errors.append(f"Global uniqueness rule '{rule.get('name', rule_type)}' is missing required parameter: field or fields")
                if 'section' not in params:
                    errors.append(f"Global uniqueness rule '{rule.get('name', rule_type)}' is missing required parameter: section")
        
        return errors
    
    def _validate_field_names(self) -> List[str]:
        """
        Validate that field names are unique within a record.
        
        Returns:
            A list of error messages
        """
        errors = []
        
        for section in self.config.get('sections', []):
            if 'record' not in section:
                continue
                
            record = section['record']
            if 'fields' not in record:
                continue
                
            fields = record['fields']
            field_names = set()
            
            for field in fields:
                if 'name' not in field:
                    continue
                    
                name = field['name']
                if name in field_names:
                    errors.append(f"Duplicate field name '{name}' in record '{record.get('name', 'Unknown')}'")
                else:
                    field_names.add(name)
        
        return errors
    
    def _validate_global_rules(self) -> List[str]:
        """
        Validate global rules.
        
        Returns:
            A list of error messages
        """
        errors = []
        
        # Check for target fields in global rules that must reference existing fields
        for rule in self.config.get('global_rules', []):
            if 'type' not in rule or 'params' not in rule:
                continue
                
            rule_type = rule['type']
            params = rule['params']
            
            # Check for field references in sum rule
            if rule_type == 'sum' and 'target_field' in params:
                target = params['target_field']
                if '.' not in target:
                    errors.append(f"Global sum rule '{rule.get('name', rule_type)}' has invalid target_field: {target}")
                else:
                    section_name, field_name = target.split('.', 1)
                    if not self._field_exists(section_name, field_name):
                        errors.append(
                            f"Global sum rule '{rule.get('name', rule_type)}' references "
                            f"non-existent field: {target}"
                        )
        
        return errors
    
    def _validate_section_constraints(self) -> List[str]:
        """
        Validate constraints between sections.
        
        Returns:
            A list of error messages
        """
        errors = []
        
        # Check that section min_records <= max_records when both are specified
        for section in self.config.get('sections', []):
            if 'min_records' in section and 'max_records' in section:
                min_records = section['min_records']
                max_records = section['max_records']
                
                if min_records > max_records:
                    errors.append(
                        f"Section '{section.get('name', 'Unknown')}' has "
                        f"min_records ({min_records}) > max_records ({max_records})"
                    )
        
        return errors
    
    def _field_exists(self, section_name: str, field_name: str) -> bool:
        """
        Check if a field exists in a section.
        
        Args:
            section_name: Name of the section
            field_name: Name of the field
            
        Returns:
            True if the field exists, False otherwise
        """
        for section in self.config.get('sections', []):
            if section.get('name') == section_name:
                if 'record' not in section:
                    return False
                    
                record = section['record']
                if 'fields' not in record:
                    return False
                    
                for field in record['fields']:
                    if field.get('name') == field_name:
                        return True
                        
                return False
                
        return False
