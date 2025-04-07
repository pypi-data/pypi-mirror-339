"""
CLI module for FlatForge.

This module contains the CLI interface for FlatForge.
"""

from flatforge.cli.main import main

__all__ = ['main']

# For backward compatibility
cli = main

if __name__ == '__main__':
    main() 