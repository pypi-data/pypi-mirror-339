import re
import unicodedata
import string
import ast
import json
from typing import List, Dict, Union, Optional, Any


class CleanPad:
    """Main class for text cleaning and formatting operations."""

    @staticmethod
    def clean_whitespace(text: str) -> str:
        """
        Normalize whitespace by replacing multiple spaces with a single space
        and strip leading/trailing whitespace.
        
        Args:
            text (str): Input text with potential whitespace issues
            
        Returns:
            str: Text with normalized whitespace
        """
        result = re.sub(r'\s+', ' ', text)
        return result.strip()
    
    @staticmethod
    def clean_line_breaks(text: str, preserve_paragraphs: bool = True) -> str:
        """
        Clean excessive line breaks while optionally preserving paragraph breaks.
        
        Args:
            text (str): Input text with potential excessive line breaks
            preserve_paragraphs (bool): If True, keep paragraph separation (double line breaks)
            
        Returns:
            str: Text with cleaned line breaks
        """
        if preserve_paragraphs:
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        else:
            text = re.sub(r'\n+', ' ', text)
        
        return CleanPad.clean_whitespace(text)
    
    @staticmethod
    def remove_emojis(text: str) -> str:
        """
        Remove all emoji characters from text.
        
        Args:
            text (str): Input text that may contain emojis
            
        Returns:
            str: Text with emojis removed
        """
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # geometric shapes
            "\U0001F800-\U0001F8FF"  # supplemental arrows
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "\U0001FA00-\U0001FA6F"  # chess symbols
            "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
            "\U00002702-\U000027B0"  # dingbats
            "\U000024C2-\U0001F251" 
            "]+", flags=re.UNICODE)
        
        return emoji_pattern.sub('', text)
    
    @staticmethod
    def clean_bullet_points(text: str, bullet_replacement: str = "") -> str:
        """
        Clean common bullet point formats (•, -, *, etc.) from text.
        
        Args:
            text (str): Input text with bullet points
            bullet_replacement (str): String to replace bullets with (default empty string)
            
        Returns:
            str: Text with bullet points removed or replaced
        """
        bullet_pattern = r'^\s*[•\-\*\>\+\◦\‣\⁃\⦿\⦾\⁌\⁍]+'
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            cleaned_line = re.sub(bullet_pattern, bullet_replacement, line)
            cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
    
    @staticmethod
    def to_list(text: str, strip_items: bool = True) -> List[str]:
        """
        Convert text that appears list-like into an actual Python list.
        Works with comma-separated, newline-separated, or bullet-pointed text.
        
        Args:
            text (str): Input text with list-like format
            strip_items (bool): Whether to strip whitespace from list items
            
        Returns:
            List[str]: A Python list containing each item as a string
        """
        if '\n' in text and ('•' in text or '-' in text or '*' in text):
            text = CleanPad.clean_bullet_points(text)
            items = [line for line in text.split('\n') if line.strip()]
        elif text.count('\n') > text.count(','):
            items = text.split('\n')
        else:
            items = text.split(',')
        
        if strip_items:
            items = [item.strip() for item in items]
        
        return [item for item in items if item]
    
    @staticmethod
    def to_dict(text: str) -> Dict[str, str]:
        """
        Convert text with key-value pairs into a Python dictionary.
        Supports formats like "key: value" or "key = value" on separate lines.
        
        Args:
            text (str): Input text with key-value structure
            
        Returns:
            Dict[str, str]: A Python dictionary with the extracted key-value pairs
        """
        result = {}
        delimiter = ':' if text.count(':') > text.count('=') else '='
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line or delimiter not in line:
                continue
                
            parts = line.split(delimiter, 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                result[key] = value
                
        return result
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        Remove HTML tags from text.
        
        Args:
            text (str): Input text that may contain HTML tags
            
        Returns:
            str: Text with HTML tags removed
        """
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def normalize_quotes(text: str) -> str:
        """
        Normalize various quote styles to standard straight quotes.
        
        Args:
            text (str): Input text with potentially varying quote styles
            
        Returns:
            str: Text with normalized quotes
        """
        text = re.sub(r'['']', "'", text)
        text = re.sub(r'[""]', '"', text)
        return text
    
    @staticmethod
    def remove_urls(text: str, replacement: str = "") -> str:
        """
        Remove URLs from text.
        
        Args:
            text (str): Input text that may contain URLs
            replacement (str): String to replace URLs with
            
        Returns:
            str: Text with URLs removed or replaced
        """
        url_pattern = r'https?://[^\s]+'
        return re.sub(url_pattern, replacement, text)
    
    @staticmethod
    def remove_special_chars(text: str, keep: Optional[str] = None) -> str:
        """
        Remove special characters, keeping only letters, numbers, and specified chars.
        
        Args:
            text (str): Input text
            keep (str, optional): Additional characters to keep
            
        Returns:
            str: Text with special characters removed
        """
        allowed = string.ascii_letters + string.digits + string.whitespace
        if keep:
            allowed += keep
            
        return ''.join(c for c in text if c in allowed)
    
    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        """
        Extract all numbers from text.
        
        Args:
            text (str): Input text containing numbers
            
        Returns:
            List[float]: List of extracted numbers
        """
        number_pattern = r'-?\d+(?:\.\d+)?'
        matches = re.findall(number_pattern, text)
        return [float(num) for num in matches]
    
    @staticmethod
    def normalize_spacing(text: str) -> str:
        """
        Normalize spacing around punctuation according to common style rules.
        
        Args:
            text (str): Input text with potentially inconsistent spacing
            
        Returns:
            str: Text with normalized spacing
        """
        text = re.sub(r'\s+([,.;:!?)])', r'\1', text)
        text = re.sub(r'([,.;:!?])([^\s,.;:!?)])', r'\1 \2', text)
        text = re.sub(r'\(\s+', '(', text)
        text = re.sub(r'\s+\)', ')', text)
        return text
    
    @staticmethod
    def try_parse_data(text: str) -> Union[List, Dict, str]:
        """
        Attempt to parse text as JSON, Python literal, or other structured data.
        
        Args:
            text (str): Input text that might be structured data
            
        Returns:
            Union[List, Dict, str]: Parsed data structure or original string if parsing fails
        """
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
            
        try:
            return ast.literal_eval(text)
        except (SyntaxError, ValueError):
            pass
            
        if ':' in text or '=' in text:
            try:
                return CleanPad.to_dict(text)
            except Exception:
                pass
                
        try:
            return CleanPad.to_list(text)
        except Exception:
            pass
            
        return text
    
    @staticmethod
    def standardize_line_endings(text: str, ending: str = '\n') -> str:
        """
        Standardize all line endings to a consistent format.
        
        Args:
            text (str): Input text with potentially mixed line endings
            ending (str): Target line ending ('\n', '\r\n', or '\r')
            
        Returns:
            str: Text with standardized line endings
        """
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        if ending != '\n':
            text = text.replace('\n', ending)
        return text
    
    @staticmethod
    def clean_indentation(text: str) -> str:
        """
        Clean inconsistent indentation.
        
        Args:
            text (str): Input text with potentially inconsistent indentation
            
        Returns:
            str: Text with cleaned indentation
        """
        lines = text.split('\n')
        prefix_length = float('inf')
        
        for line in lines:
            if line.strip():
                spaces = len(line) - len(line.lstrip())
                prefix_length = min(prefix_length, spaces)
                
        if prefix_length > 0 and prefix_length != float('inf'):
            cleaned_lines = [line[prefix_length:] if line.strip() else line for line in lines]
            return '\n'.join(cleaned_lines)
        
        return text
    
    @staticmethod
    def normalize_characters(text: str) -> str:
        """
        Normalize Unicode characters to their closest ASCII equivalent.
        
        Args:
            text (str): Input text with potentially non-ASCII characters
            
        Returns:
            str: Text with normalized characters
        """
        return ''.join(
            c for c in unicodedata.normalize('NFKD', text)
            if not unicodedata.combining(c)
        )


# Create convenience functions at module level
clean_whitespace = CleanPad.clean_whitespace
clean_line_breaks = CleanPad.clean_line_breaks
remove_emojis = CleanPad.remove_emojis
clean_bullet_points = CleanPad.clean_bullet_points
to_list = CleanPad.to_list
to_dict = CleanPad.to_dict
remove_html_tags = CleanPad.remove_html_tags
normalize_quotes = CleanPad.normalize_quotes
remove_urls = CleanPad.remove_urls
remove_special_chars = CleanPad.remove_special_chars
extract_numbers = CleanPad.extract_numbers
normalize_spacing = CleanPad.normalize_spacing
try_parse_data = CleanPad.try_parse_data
standardize_line_endings = CleanPad.standardize_line_endings
clean_indentation = CleanPad.clean_indentation
normalize_characters = CleanPad.normalize_characters