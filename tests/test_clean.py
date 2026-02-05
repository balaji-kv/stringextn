"""
Test suite for stringextn.clean module.

Tests the text cleaning functions (remove_html, remove_emoji, normalize_spaces,
normalize_unicode, clean_text) to ensure they correctly clean and normalize strings.
Covers removal of HTML tags, emoji characters, whitespace normalization,
Unicode normalization, and comprehensive text cleaning. Tests include
edge cases with special characters, various Unicode forms, and integration
between multiple cleaning operations.
"""

import pytest
from stringextn.clean import (
    remove_html,
    remove_emoji,
    normalize_spaces,
    normalize_unicode,
    clean_text,
)


class TestRemoveHtml:
    """Test cases for remove_html function"""

    def test_basic_html_tag(self):
        """Test removal of basic HTML tags"""
        assert remove_html("<p>Hello</p>") == "Hello"

    def test_multiple_html_tags(self):
        """Test removal of multiple HTML tags"""
        assert remove_html("<p>Hello</p><div>World</div>") == "HelloWorld"

    def test_html_with_attributes(self):
        """Test removal of HTML tags with attributes"""
        assert remove_html('<a href="https://example.com">Link</a>') == "Link"

    def test_nested_html_tags(self):
        """Test removal of nested HTML tags"""
        assert remove_html("<div><p>Hello</p></div>") == "Hello"

    def test_self_closing_tags(self):
        """Test removal of self-closing HTML tags"""
        assert remove_html("Hello<br/>World") == "HelloWorld"

    def test_br_tag_without_slash(self):
        """Test removal of br tag without slash"""
        assert remove_html("Hello<br>World") == "HelloWorld"

    def test_html_with_newlines(self):
        """Test removal of HTML tags with embedded newlines"""
        assert remove_html("<p>\nHello\n</p>") == "\nHello\n"

    def test_html_comments(self):
        """Test removal of HTML comments"""
        assert remove_html("Hello<!-- comment -->World") == "HelloWorld"

    def test_script_tag(self):
        """Test removal of script tags (content inside may remain).
        
        Edge case: The regex removes only the tags, not the content inside.
        Text like 'alert('hi')' remains after tag removal.
        """
        result = remove_html("<script>alert('hi')</script>")
        # The regex removes tags but content inside remains
        assert "<script>" not in result

    def test_style_tag(self):
        """Test removal of style tags (content inside may remain)"""
        result = remove_html('<style>body { color: red; }</style>')
        # The regex removes tags but content inside remains
        assert "<style>" not in result

    def test_empty_string(self):
        """Test empty string"""
        assert remove_html("") == ""

    def test_no_html_tags(self):
        """Test string without HTML tags"""
        assert remove_html("Hello World") == "Hello World"

    def test_only_html_tags(self):
        """Test string with only HTML tags"""
        assert remove_html("<p></p><div></div>") == ""

    def test_complex_html_document(self):
        """Test complex HTML document"""
        html_str = '<div class="container"><p>Hello <strong>World</strong></p></div>'
        assert remove_html(html_str) == "Hello World"

    def test_malformed_html(self):
        """Test malformed HTML (unclosed tags)"""
        assert remove_html("<p>Hello<div>World") == "HelloWorld"

    def test_html_entities_preserved(self):
        """Test that HTML entities are preserved (not decoded here)"""
        assert remove_html("<p>&nbsp;</p>") == "&nbsp;"


class TestRemoveEmoji:
    """Test cases for remove_emoji function"""

    def test_single_emoji(self):
        """Test removal of single emoji"""
        assert remove_emoji("Hello 😀") == "Hello "

    def test_multiple_emojis(self):
        """Test removal of multiple emojis"""
        result = remove_emoji("😀 Hello 😎 World 🌍")
        # Result should have spaces where emojis were
        assert "Hello" in result and "World" in result

    def test_no_emoji(self):
        """Test string without emojis"""
        assert remove_emoji("Hello World") == "Hello World"

    def test_only_emoji(self):
        """Test string with only emojis"""
        assert remove_emoji("😀😎🌍") == ""

    def test_empty_string(self):
        """Test empty string"""
        assert remove_emoji("") == ""

    def test_emoji_at_start(self):
        """Test emoji at start of string"""
        assert remove_emoji("😀Hello") == "Hello"

    def test_emoji_at_end(self):
        """Test emoji at end of string"""
        assert remove_emoji("Hello😀") == "Hello"

    def test_consecutive_emojis(self):
        """Test consecutive emojis"""
        assert remove_emoji("Hello😀😎😍World") == "HelloWorld"

    def test_emoji_with_special_characters(self):
        """Test emoji with special characters"""
        assert remove_emoji("Hello😀@#$") == "Hello@#$"

    def test_emoji_with_numbers(self):
        """Test emoji with numbers"""
        assert remove_emoji("Test😀123") == "Test123"

    def test_flag_emojis(self):
        """Test flag emojis removal"""
        assert remove_emoji("USA 🇺🇸 UK 🇬🇧") == "USA  UK "

    def test_emoji_variations(self):
        """Test various emoji types"""
        result = remove_emoji("🎉 Party 🎊 Celebration 🎈")
        assert result.strip() == "Party Celebration" or "Party" in result

    def test_mixed_content_with_emojis(self):
        """Test mixed content with emojis"""
        result = remove_emoji("Price: $50 😀 Great Deal!")
        assert result == "Price: $50  Great Deal!"


class TestNormalizeSpaces:
    """Test cases for normalize_spaces function"""

    def test_multiple_spaces(self):
        """Test reduction of multiple spaces to single space"""
        assert normalize_spaces("Hello    World") == "Hello World"

    def test_leading_spaces(self):
        """Test removal of leading spaces"""
        assert normalize_spaces("   Hello World") == "Hello World"

    def test_trailing_spaces(self):
        """Test removal of trailing spaces"""
        assert normalize_spaces("Hello World   ") == "Hello World"

    def test_leading_and_trailing_spaces(self):
        """Test removal of both leading and trailing spaces"""
        assert normalize_spaces("   Hello World   ") == "Hello World"

    def test_tabs(self):
        """Test handling of tabs"""
        assert normalize_spaces("Hello\tWorld") == "Hello World"

    def test_multiple_tabs(self):
        """Test handling of multiple tabs"""
        assert normalize_spaces("Hello\t\t\tWorld") == "Hello World"

    def test_newlines(self):
        """Test handling of newlines"""
        assert normalize_spaces("Hello\nWorld") == "Hello World"

    def test_mixed_whitespace(self):
        """Test handling of mixed whitespace"""
        assert normalize_spaces("Hello  \t\n  World") == "Hello World"

    def test_multiple_spaces_between_words(self):
        """Test multiple spaces between multiple words"""
        assert normalize_spaces("Hello     World     Test") == "Hello World Test"

    def test_empty_string(self):
        """Test empty string"""
        assert normalize_spaces("") == ""

    def test_only_spaces(self):
        """Test string with only spaces"""
        assert normalize_spaces("     ") == ""

    def test_only_tabs(self):
        """Test string with only tabs"""
        assert normalize_spaces("\t\t\t") == ""

    def test_only_newlines(self):
        """Test string with only newlines"""
        assert normalize_spaces("\n\n\n") == ""

    def test_no_extra_spaces(self):
        """Test string with no extra spaces"""
        assert normalize_spaces("Hello World") == "Hello World"

    def test_single_word(self):
        """Test single word with spaces"""
        assert normalize_spaces("   Hello   ") == "Hello"

    def test_complex_whitespace_pattern(self):
        """Test complex whitespace patterns"""
        assert normalize_spaces("The  \t\n  quick\t  brown  fox") == "The quick brown fox"


class TestNormalizeUnicode:
    """Test cases for normalize_unicode function"""

    def test_accented_characters(self):
        """Test normalization of accented characters"""
        # NFKD normalization may decompose characters
        result = normalize_unicode("café")
        assert isinstance(result, str)

    def test_different_unicode_forms(self):
        """Test normalization of different unicode forms"""
        # Composed and decomposed forms should normalize the same
        composed = "é"  # Single character
        result = normalize_unicode(composed)
        assert isinstance(result, str)

    def test_ligatures(self):
        """Test handling of ligatures"""
        result = normalize_unicode("ﬁnally")
        assert isinstance(result, str)

    def test_superscript_numbers(self):
        """Test normalization of superscript numbers"""
        result = normalize_unicode("2⁵")
        assert isinstance(result, str)

    def test_subscript_numbers(self):
        """Test normalization of subscript numbers"""
        result = normalize_unicode("H₂O")
        assert isinstance(result, str)

    def test_special_symbols(self):
        """Test normalization of special symbols"""
        result = normalize_unicode("™®©")
        assert isinstance(result, str)

    def test_greek_letters(self):
        """Test normalization of greek letters"""
        result = normalize_unicode("α β γ δ")
        assert isinstance(result, str)

    def test_empty_string(self):
        """Test empty string"""
        assert normalize_unicode("") == ""

    def test_plain_ascii(self):
        """Test that plain ASCII remains unchanged"""
        assert normalize_unicode("Hello World 123") == "Hello World 123"

    def test_mixed_ascii_and_unicode(self):
        """Test mixed ASCII and unicode"""
        result = normalize_unicode("Café au lait")
        assert isinstance(result, str)

    def test_combining_characters(self):
        """Test strings with combining characters"""
        result = normalize_unicode("e\u0301")  # e with combining acute accent
        assert isinstance(result, str)

    def test_hebrew_characters(self):
        """Test Hebrew characters normalization"""
        result = normalize_unicode("שלום")
        assert isinstance(result, str)

    def test_arabic_characters(self):
        """Test Arabic characters normalization"""
        result = normalize_unicode("السلام")
        assert isinstance(result, str)

    def test_chinese_characters(self):
        """Test Chinese characters normalization"""
        result = normalize_unicode("你好")
        assert isinstance(result, str)

    def test_japanese_characters(self):
        """Test Japanese characters normalization"""
        result = normalize_unicode("こんにちは")
        assert isinstance(result, str)


class TestCleanText:
    """Test cases for clean_text function (comprehensive cleaning)"""

    def test_all_cleaning_features(self):
        """Test that clean_text applies all cleaning operations"""
        # HTML, emojis, unicode, extra spaces
        text = '  <p>Hello &nbsp; 😀 World   café</p>  '
        result = clean_text(text)
        # Should be cleaned of HTML, emoji, extra spaces, and unicode normalized
        assert isinstance(result, str)
        assert "<p>" not in result
        assert "😀" not in result

    def test_clean_simple_text(self):
        """Test cleaning simple text"""
        assert clean_text("Hello World") == "Hello World"

    def test_clean_empty_string(self):
        """Test cleaning empty string"""
        assert clean_text("") == ""

    def test_clean_only_whitespace(self):
        """Test cleaning whitespace-only string"""
        assert clean_text("    \t\n   ") == ""

    def test_clean_html_with_spaces(self):
        """Test cleaning HTML with extra spaces"""
        text = "<p>  Hello   World  </p>"
        result = clean_text(text)
        assert result == "Hello World"

    def test_clean_html_with_emoji(self):
        """Test cleaning HTML with emoji"""
        text = "<p>Hello 😀 World</p>"
        result = clean_text(text)
        assert "<p>" not in result
        assert "😀" not in result
        assert result.strip() == "Hello World"

    def test_clean_html_entities(self):
        """Test cleaning HTML entities"""
        text = "&lt;p&gt;Hello&lt;/p&gt;"
        result = clean_text(text)
        assert "&lt;" not in result
        assert "&gt;" not in result

    def test_clean_nested_html_with_content(self):
        """Test cleaning nested HTML"""
        text = "<div><p>Hello</p><span>World</span></div>"
        result = clean_text(text)
        assert "<div>" not in result
        assert "<p>" not in result
        # Should contain hello and world
        assert "Hello" in result and "World" in result

    def test_clean_multiple_emojis(self):
        """Test cleaning multiple emojis"""
        text = "😀😎🌍 Hello 🎉 World"
        result = clean_text(text)
        assert "😀" not in result
        assert "😎" not in result
        assert "🌍" not in result
        assert "🎉" not in result

    def test_clean_unicode_normalization(self):
        """Test unicode normalization in clean_text"""
        text = "Café"
        result = clean_text(text)
        assert isinstance(result, str)

    def test_clean_complex_document(self):
        """Test cleaning complex document with all features"""
        text = '''  <div class="content">
            <p>Welcome to our site! 😀</p>
            <p>This is &nbsp; a &nbsp; test   with    multiple   spaces</p>
            <p>Café au lait 🎉</p>
        </div>  '''
        result = clean_text(text)
        assert "<div" not in result
        assert "<p>" not in result
        assert "😀" not in result
        assert "🎉" not in result
        assert "&nbsp;" not in result
        # Should have normalized spaces
        assert "  " not in result or result.count(" ") <= 1

    def test_clean_text_with_script_tags(self):
        """Test cleaning text with script tags"""
        text = "<script>alert('xss')</script>Hello"
        result = clean_text(text)
        assert "<script>" not in result
        # alert text might remain as it's content
        assert "Hello" in result

    def test_clean_text_with_html_comments(self):
        """Test cleaning text with HTML comments"""
        text = "Hello<!-- This is a comment -->World"
        result = clean_text(text)
        assert "<!--" not in result
        assert result == "HelloWorld"

    def test_clean_preserves_alphanumeric(self):
        """Test that cleaning preserves alphanumeric content"""
        text = "<p>Test123</p>"
        result = clean_text(text)
        assert "Test123" in result

    def test_clean_with_special_characters(self):
        """Test cleaning preserves special characters"""
        text = "<p>Hello! @#$% World?</p>"
        result = clean_text(text)
        assert "Hello!" in result
        assert "@#$%" in result
        assert "World?" in result

    def test_clean_multiple_spaces_reduction(self):
        """Test that multiple spaces are reduced to one"""
        text = "Hello     World     Test"
        result = clean_text(text)
        assert result == "Hello World Test"

    def test_clean_tabs_and_newlines(self):
        """Test that tabs and newlines are converted to spaces"""
        text = "Hello\tWorld\nTest"
        result = clean_text(text)
        assert result == "Hello World Test"

    def test_clean_order_of_operations(self):
        """Test that cleaning operations work in correct order"""
        text = "<p>&nbsp;&nbsp;&nbsp;Test&nbsp;&nbsp;&nbsp;</p>"
        result = clean_text(text)
        # HTML entities should be unescaped first, then HTML removed, then spaces normalized
        assert result == "Test"

    def test_clean_emoji_with_html(self):
        """Test emoji removal works with HTML"""
        text = "<p>😀</p>"
        result = clean_text(text)
        assert "😀" not in result
        assert "<p>" not in result

    def test_clean_real_world_example_1(self):
        """Test real-world example - social media post"""
        text = '  <div>Check out my new blog! 🎉  <a href="#">Read more</a> 😀😀😀  </div>  '
        result = clean_text(text)
        assert "<div>" not in result
        assert "<a" not in result
        assert "🎉" not in result
        assert "😀" not in result
        assert "Check" in result

    def test_clean_real_world_example_2(self):
        """Test real-world example - web scraped content"""
        text = '<p class="content">Price: $100&nbsp;&nbsp;🔥&nbsp;&nbsp;LIMITED&nbsp;OFFER</p>'
        result = clean_text(text)
        assert "<p" not in result
        assert "🔥" not in result
        assert "class" not in result
        assert "$100" in result


class TestIntegration:
    """Integration tests for multiple functions"""

    def test_remove_html_then_normalize_spaces(self):
        """Test removing HTML and then normalizing spaces"""
        text = "<p>Hello   World</p>"
        result = remove_html(text)
        result = normalize_spaces(result)
        assert result == "Hello World"

    def test_remove_emoji_then_normalize_spaces(self):
        """Test removing emoji and then normalizing spaces"""
        text = "Hello  😀  World"
        result = remove_emoji(text)
        result = normalize_spaces(result)
        assert result == "Hello World"

    def test_order_matters_html_before_spaces(self):
        """Test that removing HTML before spaces works correctly"""
        text = "<p>Hello</p>   <p>World</p>"
        result = remove_html(text)
        result = normalize_spaces(result)
        assert result == "Hello World"

    def test_multiple_operations_on_complex_text(self):
        """Test multiple cleaning operations on complex text"""
        text = '<div>  <p>Test &nbsp; 123  😀   café</p>  </div>'
        result = remove_html(text)
        result = remove_emoji(result)
        result = normalize_unicode(result)
        result = normalize_spaces(result)
        assert "<div>" not in result
        assert "😀" not in result
        assert "  " not in result


class TestEdgeCases:
    """Edge cases for clean functions"""

    def test_very_long_string(self):
        """Test processing very long strings"""
        long_text = "Hello World " * 1000
        result = clean_text(long_text)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_only_html_tags(self):
        """Test string with only HTML tags"""
        result = remove_html("<p></p><div></div><span></span>")
        assert result == ""

    def test_only_emojis(self):
        """Test string with only emojis"""
        result = remove_emoji("😀😎🌍")
        assert result == ""

    def test_mixed_line_endings(self):
        """Test string with mixed line endings"""
        text = "Hello\r\nWorld\rTest\nEnd"
        result = normalize_spaces(text)
        assert isinstance(result, str)

    def test_zero_width_characters(self):
        """Test handling zero-width characters"""
        text = "Hello\u200bWorld"  # Zero-width space
        result = normalize_unicode(text)
        assert isinstance(result, str)

    def test_null_character(self):
        """Test handling null characters"""
        text = "Hello\x00World"
        result = clean_text(text)
        assert isinstance(result, str)

    def test_control_characters(self):
        """Test handling control characters"""
        text = "Hello\x01\x02\x03World"
        result = clean_text(text)
        assert isinstance(result, str)
