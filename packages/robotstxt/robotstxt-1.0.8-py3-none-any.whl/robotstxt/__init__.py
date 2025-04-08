"""
robotstxt package - A Python package for processing and validating robots.txt files.

This package provides functionality for:
- Processing robots.txt files
- Validating robots.txt directives
- Matching URLs against robots.txt rules
"""

from .robots_processing import (
    select_group,
    get_url_path,
    is_valid_url
)

from .processor import (
    RobotsFile,
    Sitemap,
    compare_robots_files,
    hash_generator
)

# Maintain backward compatibility with previous alias
robots_file = RobotsFile

from .validation import (
    RobotsValidator,
    ValidationMessage
)

from .directive_match import (
    pattern_match
)

# Make these available at the package level
__all__ = [
    'select_group',
    'get_url_path',
    'is_valid_url',
    'RobotsFile',
    'robots_file',  # Maintain backward compatibility
    'Sitemap',
    'compare_robots_files',
    'hash_generator',
    'RobotsValidator',
    'ValidationMessage',
    'pattern_match'
]