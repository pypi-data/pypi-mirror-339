"""
Global rules package for FlatForge.

This package contains all global rules used for validating entire files.
"""
from flatforge.rules.global_rules.count import CountRule
from flatforge.rules.global_rules.sum import SumRule
from flatforge.rules.global_rules.checksum import ChecksumRule
from flatforge.rules.global_rules.uniqueness import UniquenessRule
from flatforge.rules.global_rules.factory import GlobalRuleFactory

__all__ = [
    'CountRule',
    'SumRule',
    'ChecksumRule',
    'UniquenessRule',
    'GlobalRuleFactory',
] 