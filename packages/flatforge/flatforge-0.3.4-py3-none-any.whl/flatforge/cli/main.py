"""
CLI main module for FlatForge.

This module contains the main CLI entry point for FlatForge.
"""
import sys
from typing import Optional

import click
import yaml
from tqdm import tqdm

from flatforge.core import ConfigError, ProcessorError, FileFormat
from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor, ConversionProcessor, CounterProcessor
from flatforge.validators import ConfigValidator


@click.group()
@click.version_option()
def main():
    """FlatForge - A library for validating and transforming flat files."""
    pass


@main.command()
@click.option('--config', '-c', required=True, help='Path to the configuration file.')
@click.option('--input', '-i', required=True, help='Path to the input file.')
@click.option('--output', '-o', required=True, help='Path to the output file.')
@click.option('--errors', '-e', help='Path to the error file.')
@click.option('--chunk-size', required=False, type=int, default=0, 
              help='Process file in chunks of this size (for large files). Default is 0 (no chunking).')
@click.option('--show-progress', is_flag=True, help='Show progress bar when processing large files')
def validate(config: str, input: str, output: str, errors: Optional[str] = None, chunk_size: int = 0, show_progress: bool = False):
    """Validate a file against a schema."""
    try:
        # Parse the configuration
        file_format = FileFormat.from_yaml(config)
        
        # Create a processor
        processor = ValidationProcessor(file_format)
        
        # Process the file
        if chunk_size > 0:
            # Use chunked processing for large files
            with tqdm(total=100, disable=not show_progress) as progress_bar:
                def update_progress(processed, total):
                    if total > 0:
                        progress_bar.update(int(100 * processed / total) - progress_bar.n)
                    
                result = processor.process_chunked(input, output, errors, chunk_size, update_progress)
        else:
            # Use standard processing
            result = processor.process(input, output, errors)
        
        # Print the result
        click.echo(f"Total records: {result.total_records}")
        click.echo(f"Valid records: {result.valid_records}")
        click.echo(f"Error count: {result.error_count}")
        
        # Return a non-zero exit code if there were errors
        if result.error_count > 0:
            sys.exit(1)
            
    except (ConfigError, ProcessorError) as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--config', required=True, help='Path to the configuration file to validate')
@click.option('--schema', required=False, help='Path to a custom JSON schema file')
def validate_config(config, schema):
    """Validate a configuration file without processing any data."""
    try:
        click.echo(f"Validating configuration file: {config}")
        
        # Create validator - pass the schema parameter if provided
        validator = ConfigValidator.from_file(config, schema_file=schema) if schema else ConfigValidator.from_file(config)
        
        # Validate the configuration
        is_valid = validator.validate()
        
        if is_valid:
            click.secho("✓ Configuration is valid!", fg="green")
            return 0
        else:
            click.secho("✗ Configuration contains errors:", fg="red")
            for i, error in enumerate(validator.errors, 1):
                click.echo(f"  {i}. {error}")
            # Use sys.exit(1) instead of return 1 to ensure proper exit code in both CLI and tests
            sys.exit(1)
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg="red", err=True)
        sys.exit(1)


@main.command()
@click.option('--input-config', '-ic', required=True, help='Path to the input configuration file.')
@click.option('--output-config', '-oc', required=True, help='Path to the output configuration file.')
@click.option('--mapping', required=False, help='Path to the mapping configuration file')
@click.option('--input', '-i', required=True, help='Path to the input file.')
@click.option('--output', '-o', required=True, help='Path to the output file.')
@click.option('--errors', '-e', help='Path to the error file.')
@click.option('--chunk-size', required=False, type=int, default=0, 
              help='Process file in chunks of this size (for large files). Default is 0 (no chunking).')
@click.option('--show-progress', is_flag=True, help='Show progress bar when processing large files')
def convert(input_config: str, output_config: str, mapping: Optional[str] = None, 
           input: str = None, output: str = None, errors: Optional[str] = None,
           chunk_size: int = 0, show_progress: bool = False):
    """Convert a file from one format to another."""
    try:
        # Parse the configurations
        input_format = FileFormat.from_yaml(input_config)
        output_format = FileFormat.from_yaml(output_config)
        
        # Load the mapping if provided
        mapping_config = None
        if mapping:
            with open(mapping, 'r') as f:
                mapping_config = yaml.safe_load(f)
        
        # Create a processor
        processor = ConversionProcessor(input_format, output_format, mapping_config)
        
        # Process the file
        if chunk_size > 0:
            # Use chunked processing for large files
            with tqdm(total=100, disable=not show_progress) as progress_bar:
                def update_progress(processed, total):
                    if total > 0:
                        progress_bar.update(int(100 * processed / total) - progress_bar.n)
                    
                result = processor.process_chunked(input, output, errors, chunk_size, update_progress)
        else:
            # Use standard processing
            result = processor.process(input, output, errors)
        
        # Print the result
        click.echo(f"Total records: {result.total_records}")
        click.echo(f"Valid records: {result.valid_records}")
        click.echo(f"Error count: {result.error_count}")
        
        # Return a non-zero exit code if there were errors
        if result.error_count > 0:
            sys.exit(1)
            
    except (ConfigError, ProcessorError) as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--config', '-c', required=True, help='Path to the configuration file.')
@click.option('--input', '-i', required=True, help='Path to the input file.')
@click.option('--output', '-o', help='Path to the output file.')
@click.option('--chunk-size', required=False, type=int, default=0, 
              help='Process file in chunks of this size (for large files). Default is 0 (no chunking).')
@click.option('--show-progress', is_flag=True, help='Show progress bar when processing large files')
def count(config: str, input: str, output: Optional[str] = None, chunk_size: int = 0, show_progress: bool = False):
    """Count records in a file."""
    try:
        # Parse the configuration
        file_format = FileFormat.from_yaml(config)
        
        # Create a processor
        processor = CounterProcessor(file_format)
        
        # Process the file
        if chunk_size > 0:
            # Use chunked processing for large files
            with tqdm(total=100, disable=not show_progress) as progress_bar:
                def update_progress(processed, total):
                    if total > 0:
                        progress_bar.update(int(100 * processed / total) - progress_bar.n)
                    
                result = processor.process_chunked(input, output, None, chunk_size, update_progress)
        else:
            # Use standard processing
            result = processor.process(input, output)
            
        # Print the result
        click.echo(f"Total records: {result.total_records}")
        click.echo(f"Valid records: {result.valid_records}")
        click.echo(f"Error count: {result.error_count}")
        
    except (ConfigError, ProcessorError) as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main() 