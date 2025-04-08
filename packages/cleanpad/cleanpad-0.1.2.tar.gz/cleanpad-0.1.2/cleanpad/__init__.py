"""
cleanpad - Text Cleaner & Formatter

A versatile Python library for cleaning and formatting messy text, particularly useful 
for handling copy-pasted content with unwanted formatting.
"""

from .core import (
    CleanPad,
    clean_whitespace,
    clean_line_breaks,
    remove_emojis,
    clean_bullet_points,
    to_list,
    to_dict,
    remove_html_tags,
    normalize_quotes,
    remove_urls,
    remove_special_chars,
    extract_numbers,
    normalize_spacing,
    try_parse_data,
    standardize_line_endings,
    clean_indentation,
    normalize_characters
)

__version__ = "0.1.0"
__all__ = [
    'CleanPad',
    'clean_whitespace',
    'clean_line_breaks',
    'remove_emojis',
    'clean_bullet_points',
    'to_list',
    'to_dict',
    'remove_html_tags',
    'normalize_quotes',
    'remove_urls',
    'remove_special_chars',
    'extract_numbers',
    'normalize_spacing',
    'try_parse_data',
    'standardize_line_endings',
    'clean_indentation',
    'normalize_characters'
]