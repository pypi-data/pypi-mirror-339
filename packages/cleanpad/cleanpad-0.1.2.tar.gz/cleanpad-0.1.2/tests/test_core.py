import unittest
from cleanpad.core import CleanPad


class TestCleanPad(unittest.TestCase):
    def setUp(self):
        self.cp = CleanPad()

    def test_clean_whitespace(self):
        self.assertEqual(self.cp.clean_whitespace("  hello   world  "), "hello world")
        self.assertEqual(self.cp.clean_whitespace("\ttext\nwith\nwhitespace\t"), "text with whitespace")
    
    def test_clean_line_breaks(self):
        text = "Line1\n\nLine2\n\n\nLine3"
        self.assertEqual(self.cp.clean_line_breaks(text), "Line1\n\nLine2\n\nLine3")
        self.assertEqual(self.cp.clean_line_breaks(text, False), "Line1 Line2 Line3")
    
    def test_remove_emojis(self):
        self.assertEqual(self.cp.remove_emojis("Hello 😊 World"), "Hello  World")
        self.assertEqual(self.cp.remove_emojis("No emojis here"), "No emojis here")
    
    def test_clean_bullet_points(self):
        bullet_text = "• Item1\n- Item2\n* Item3"
        self.assertEqual(self.cp.clean_bullet_points(bullet_text), "Item1\nItem2\nItem3")
    
    def test_to_list(self):
        self.assertEqual(self.cp.to_list("a,b,c"), ["a", "b", "c"])
        self.assertEqual(self.cp.to_list("one\ntwo\nthree"), ["one", "two", "three"])
    
    def test_to_dict(self):
        dict_text = "key1: value1\nkey2=value2"
        self.assertEqual(self.cp.to_dict(dict_text), {"key1": "value1", "key2": "value2"})
    
    def test_remove_html_tags(self):
        self.assertEqual(self.cp.remove_html_tags("<p>Hello</p>"), "Hello")
    
    def test_normalize_quotes(self):
        self.assertEqual(self.cp.normalize_quotes("“smart quotes”"), '"smart quotes"')
    
    def test_remove_urls(self):
        self.assertEqual(self.cp.remove_urls("Visit https://example.com"), "Visit ")
    
    def test_remove_special_chars(self):
        self.assertEqual(self.cp.remove_special_chars("Hello!@# World", "!"), "Hello! World")
    
    def test_extract_numbers(self):
        self.assertEqual(self.cp.extract_numbers("1, 2.5, -3"), [1.0, 2.5, -3.0])
    
    def test_normalize_spacing(self):
        self.assertEqual(self.cp.normalize_spacing("Hello ,world ."), "Hello, world.")
    
    def test_try_parse_data(self):
        self.assertEqual(self.cp.try_parse_data("[1, 2, 3]"), [1, 2, 3])
        self.assertEqual(self.cp.try_parse_data('{"a": 1}'), {"a": 1})
    
    def test_standardize_line_endings(self):
        self.assertEqual(self.cp.standardize_line_endings("a\r\nb\rc"), "a\nb\nc")
    
    def test_clean_indentation(self):
        indented = "    line1\n    line2"
        self.assertEqual(self.cp.clean_indentation(indented), "line1\nline2")
    
    def test_normalize_characters(self):
        self.assertEqual(self.cp.normalize_characters("café"), "cafe")


if __name__ == '__main__':
    unittest.main()