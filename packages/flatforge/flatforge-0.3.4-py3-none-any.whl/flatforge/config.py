import yaml
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class FileSettings:
    input_file: str
    output_file: str
    input_encoding: str
    output_encoding: str
    delimiter: str
    has_header: bool

@dataclass
class Rule:
    type: str
    column: Optional[str] = None
    algorithm: Optional[str] = None
    columns: Optional[List[str]] = None
    target_column: Optional[str] = None
    strip_spaces: Optional[bool] = None
    strip_hyphens: Optional[bool] = None
    error_message: Optional[str] = None

@dataclass
class Transformation:
    type: str
    source_field: str
    target_field: str
    mapping_file: str
    default_value: Optional[str] = None

@dataclass
class Section:
    name: str
    start_line: int
    end_line: int
    rules: List[Rule]
    transformations: Optional[List[Transformation]] = None
    
    def __post_init__(self):
        """Initialize optional fields if None."""
        if self.transformations is None:
            self.transformations = []

class Config:
    """Configuration class for FlatForge."""
    
    def __init__(self, config_path: str):
        """Initialize configuration from a YAML file.
        
        Args:
            config_path (str): Path to the YAML configuration file
        """
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            
        # Load file settings
        self.file_settings = FileSettings(**config_data['file_settings'])
        
        # Load sections
        self.sections = []
        for section_data in config_data['sections']:
            rules = [Rule(**rule) for rule in section_data.get('rules', [])]
            transformations = [Transformation(**trans) for trans in section_data.get('transformations', [])]
            section = Section(
                name=section_data['name'],
                start_line=section_data['start_line'],
                end_line=section_data['end_line'],
                rules=rules,
                transformations=transformations
            )
            self.sections.append(section)
            
        # Load global rules
        self.global_rules = [Rule(**rule) for rule in config_data.get('global_rules', [])] 