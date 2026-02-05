"""Test suite for stringextn.slug slugify function.

Validates slug generation for basic text, special characters, Unicode,
HTML cleaning, edge cases, and real-world scenarios.
"""

import pytest
from stringextn.slug import slugify


class TestSlugifyBasic:
    """Basic test cases for slugify function"""

    def test_simple_lowercase_text(self):
        """Test slugifying simple lowercase text"""
        # Converts spaces to hyphens and lowercases.
        result = slugify("hello world")
        assert result == "hello-world"

    def test_simple_uppercase_text(self):
        """Test slugifying simple uppercase text"""
        # Uppercase is normalized to lowercase.
        result = slugify("Hello World")
        assert result == "hello-world"

    def test_mixed_case_text(self):
        """Test slugifying mixed case text"""
        # Mixed case is normalized to lowercase.
        result = slugify("HeLLo WoRLd")
        assert result == "hello-world"

    def test_single_word(self):
        """Test slugifying single word"""
        # Single word should remain unchanged.
        result = slugify("hello")
        assert result == "hello"

    def test_empty_string(self):
        """Test slugifying empty string"""
        # Empty input should return empty output.
        result = slugify("")
        assert result == ""

    def test_only_spaces(self):
        """Test slugifying string with only spaces"""
        # Whitespace-only input should produce empty output.
        result = slugify("   ")
        assert result == ""

    def test_multiple_spaces_between_words(self):
        """Test handling multiple spaces between words"""
        # Multiple spaces collapse into a single hyphen.
        result = slugify("hello    world")
        assert result == "hello-world"

    def test_text_with_numbers(self):
        """Test slugifying text with numbers"""
        # Numbers are preserved.
        result = slugify("hello 123 world")
        assert result == "hello-123-world"

    def test_text_starting_with_number(self):
        """Test slugifying text starting with number"""
        # Leading numbers are preserved.
        result = slugify("123 hello")
        assert result == "123-hello"

    def test_text_ending_with_number(self):
        """Test slugifying text ending with number"""
        # Trailing numbers are preserved.
        result = slugify("hello 123")
        assert result == "hello-123"

    def test_consecutive_numbers(self):
        """Test consecutive numbers in text"""
        # Consecutive digits remain intact.
        result = slugify("hello 12345 world")
        assert result == "hello-12345-world"


class TestSlugifySpecialCharacters:
    """Test cases with special characters"""

    def test_text_with_hyphens(self):
        """Test text already containing hyphens"""
        # Existing hyphens are preserved.
        result = slugify("hello-world")
        assert result == "hello-world"

    def test_text_with_underscores(self):
        """Test text with underscores"""
        # Underscores become hyphens.
        result = slugify("hello_world")
        assert result == "hello-world"

    def test_text_with_dots(self):
        """Test text with dots"""
        # Dots are treated as separators.
        result = slugify("hello.world")
        assert result == "hello-world"

    def test_text_with_commas(self):
        """Test text with commas"""
        # Commas are treated as separators.
        result = slugify("hello, world")
        assert result == "hello-world"

    def test_text_with_exclamation(self):
        """Test text with exclamation marks"""
        # Punctuation is removed/converted to hyphens.
        result = slugify("hello! world!")
        assert result == "hello-world"

    def test_text_with_question_mark(self):
        """Test text with question marks"""
        # Question marks are treated as separators.
        result = slugify("hello? world?")
        assert result == "hello-world"

    def test_text_with_parentheses(self):
        """Test text with parentheses"""
        # Parentheses are removed/treated as separators.
        result = slugify("hello (world)")
        assert result == "hello-world"

    def test_text_with_brackets(self):
        """Test text with brackets"""
        # Brackets are treated as separators.
        result = slugify("hello [world]")
        assert result == "hello-world"

    def test_text_with_quotes(self):
        """Test text with quotes"""
        # Quotes are removed/treated as separators.
        result = slugify('hello "world"')
        assert result == "hello-world"

    def test_text_with_apostrophe(self):
        """Test text with apostrophes"""
        # Apostrophes split words into separate tokens.
        result = slugify("don't worry")
        # Apostrophe is treated as a word separator
        assert result == "don-t-worry"

    def test_text_with_ampersand(self):
        """Test text with ampersand"""
        # Ampersands are treated as separators.
        result = slugify("hello & world")
        assert result == "hello-world"

    def test_text_with_at_symbol(self):
        """Test text with @ symbol"""
        # At-sign is treated as separator.
        result = slugify("hello@world")
        assert result == "hello-world"

    def test_text_with_hashtag(self):
        """Test text with hashtag"""
        # Hash symbol is removed; text remains.
        result = slugify("#hello world")
        assert result == "hello-world"

    def test_text_with_percent(self):
        """Test text with percent sign"""
        # Percent sign is removed; numbers preserved.
        result = slugify("50% off")
        assert result == "50-off"

    def test_text_with_dollar_sign(self):
        """Test text with dollar sign"""
        # Currency symbol is removed; numbers preserved.
        result = slugify("$100 price")
        assert result == "100-price"

    def test_text_with_plus(self):
        """Test text with plus sign"""
        # Plus signs are treated as separators.
        result = slugify("1 + 1 = 2")
        assert result == "1-1-2"

    def test_text_with_equals(self):
        """Test text with equals sign"""
        # Equals sign is treated as separator.
        result = slugify("a = b")
        assert result == "a-b"

    def test_text_with_asterisk(self):
        """Test text with asterisk"""
        # Asterisks are treated as separators.
        result = slugify("5 * 5 = 25")
        assert result == "5-5-25"

    def test_text_with_slash(self):
        """Test text with forward slash"""
        # Slashes are treated as separators.
        result = slugify("hello/world")
        assert result == "hello-world"

    def test_text_with_backslash(self):
        """Test text with backslash"""
        # Backslashes are treated as separators.
        result = slugify("hello\\world")
        assert result == "hello-world"

    def test_text_with_pipe(self):
        """Test text with pipe character"""
        # Pipes are treated as separators.
        result = slugify("hello|world")
        assert result == "hello-world"

    def test_text_with_tilde(self):
        """Test text with tilde"""
        # Tildes are treated as separators.
        result = slugify("hello~world")
        assert result == "hello-world"

    def test_text_with_caret(self):
        """Test text with caret"""
        # Carets are treated as separators.
        result = slugify("hello^world")
        assert result == "hello-world"

    def test_text_with_backtick(self):
        """Test text with backtick"""
        # Backticks are treated as separators.
        result = slugify("hello`world")
        assert result == "hello-world"

    def test_multiple_special_characters(self):
        """Test text with multiple special characters"""
        # Multiple punctuation collapses to single hyphen.
        result = slugify("hello!!!@@@###world")
        assert result == "hello-world"


class TestSlugifyUnicode:
    """Test cases with unicode characters"""

    def test_accented_characters(self):
        """Test unicode accented characters"""
        # Unicode is normalized; accents may be removed.
        result = slugify("café")
        # clean_text normalizes unicode, so accents might be decomposed
        assert isinstance(result, str)
        assert "cafe" in result or "café" in result.replace("-", "")

    def test_unicode_multiple_words(self):
        """Test multiple words with unicode"""
        # Unicode words should still produce a slug.
        result = slugify("café latté")
        assert "-" in result or "cafe" in result

    def test_chinese_characters(self):
        """Test Chinese characters"""
        # Non-latin characters are stripped by alphanumeric filter.
        result = slugify("你好世界")
        # Chinese characters should be removed (not alphanumeric)
        assert result == ""

    def test_arabic_characters(self):
        """Test Arabic characters"""
        # Non-latin characters are stripped.
        result = slugify("السلام")
        # Arabic characters should be removed
        assert result == ""

    def test_hebrew_characters(self):
        """Test Hebrew characters"""
        # Non-latin characters are stripped.
        result = slugify("שלום")
        # Hebrew characters should be removed
        assert result == ""

    def test_mixed_ascii_and_unicode(self):
        """Test mixed ASCII and unicode"""
        # ASCII text should survive Unicode normalization.
        result = slugify("hello café")
        assert "hello" in result

    def test_emoji_removal(self):
        """Test emoji characters are removed"""
        # Emoji are removed by clean_text.
        result = slugify("hello 😀 world")
        assert result == "hello-world"

    def test_multiple_emoji(self):
        """Test multiple emoji"""
        # Emoji-only input should yield empty slug.
        result = slugify("😀 😎 🌍")
        assert result == ""

    def test_greek_characters(self):
        """Test Greek characters"""
        # Non-latin characters are stripped.
        result = slugify("Ελληνικά")
        # Greek characters should be removed
        assert result == ""


class TestSlugifyHtmlAndCleaning:
    """Test cases with HTML and content requiring cleaning"""

    def test_html_tags_removed(self):
        """Test HTML tags are removed"""
        # HTML tags should be stripped before slugging.
        result = slugify("<p>hello world</p>")
        assert result == "hello-world"

    def test_html_entities(self):
        """Test HTML entities are handled"""
        # Entities are unescaped then normalized.
        result = slugify("hello&nbsp;world")
        # &nbsp; is unescaped to non-breaking space, then normalized
        assert "hello" in result and "world" in result

    def test_script_tags_removed(self):
        """Test script tags are removed"""
        # Script tags should be removed by cleaning.
        result = slugify("<script>alert('xss')</script>")
        # Should be cleaned
        assert "script" not in result

    def test_style_tags_removed(self):
        """Test style tags are removed"""
        # Style tags should be removed by cleaning.
        result = slugify("<style>body { color: red; }</style>")
        # Should be cleaned
        assert "style" not in result

    def test_nested_html_tags(self):
        """Test nested HTML tags"""
        # Nested tags should be stripped leaving text.
        result = slugify("<div><p>hello <strong>world</strong></p></div>")
        assert result == "hello-world"

    def test_html_comments_removed(self):
        """Test HTML comments are removed"""
        # Comments are removed without adding separators.
        result = slugify("hello<!-- comment -->world")
        # Comments are removed but no space is added between text
        assert result == "helloworld"

    def test_multiple_spaces_from_html(self):
        """Test multiple spaces from HTML are normalized"""
        # Multiple spaces should collapse to a single hyphen.
        result = slugify("<p>hello   world</p>")
        assert result == "hello-world"

    def test_newlines_and_tabs_removed(self):
        """Test newlines and tabs are handled"""
        # Whitespace characters are normalized to hyphens.
        result = slugify("hello\nworld\ttest")
        assert result == "hello-world-test"


class TestSlugifyEmojiAndCleaning:
    """Test emoji handling through clean_text"""

    def test_emoji_with_text(self):
        """Test emoji mixed with text"""
        # Emoji should be removed but words preserved.
        result = slugify("hello 😀 world 😎")
        assert result == "hello-world"

    def test_emoji_only(self):
        """Test emoji only"""
        # Emoji-only input should return empty slug.
        result = slugify("😀😎🌍")
        assert result == ""

    def test_emoji_at_start(self):
        """Test emoji at start of string"""
        # Leading emoji should be removed.
        result = slugify("😀 hello")
        assert result == "hello"

    def test_emoji_at_end(self):
        """Test emoji at end of string"""
        # Trailing emoji should be removed.
        result = slugify("hello 😀")
        assert result == "hello"


class TestSlugifyEdgeCases:
    """Edge cases and boundary conditions"""

    def test_very_long_string(self):
        """Test with very long string"""
        # Edge case: long input should produce predictable slug.
        long_text = "hello world " * 1000
        result = slugify(long_text)
        # Pattern repeats 1000 times with trailing space, so 'hello-world-' repeats
        # Last iteration has trailing space that becomes empty after cleanup
        expected = "hello-world-" * 999 + "hello-world"
        assert result == expected

    def test_only_special_characters(self):
        """Test string with only special characters"""
        # Non-alphanumeric input should be stripped to empty.
        result = slugify("!@#$%^&*()")
        assert result == ""

    def test_only_numbers(self):
        """Test string with only numbers"""
        # Numeric-only input should be preserved.
        result = slugify("123456789")
        assert result == "123456789"

    def test_numbers_and_special_chars_only(self):
        """Test numbers with special characters"""
        # Numbers should remain; separators become hyphens.
        result = slugify("123-456-789")
        assert result == "123-456-789"

    def test_consecutive_hyphens(self):
        """Test text that would create consecutive hyphens"""
        # Multiple separators should collapse to a single hyphen.
        result = slugify("hello---world")
        # Multiple special chars become single hyphen
        assert result == "hello-world"

    def test_leading_special_characters(self):
        """Test leading special characters"""
        # Leading separators should be stripped.
        result = slugify("!!!hello")
        assert result == "hello"

    def test_trailing_special_characters(self):
        """Test trailing special characters"""
        # Trailing separators should be stripped.
        result = slugify("hello!!!")
        assert result == "hello"

    def test_leading_and_trailing_special_chars(self):
        """Test both leading and trailing special characters"""
        # Leading/trailing separators should be stripped.
        result = slugify("!!!hello!!!")
        assert result == "hello"

    def test_leading_numbers(self):
        """Test leading numbers are preserved"""
        # Leading numbers are retained.
        result = slugify("123abc")
        assert result == "123abc"

    def test_trailing_numbers(self):
        """Test trailing numbers are preserved"""
        # Trailing numbers are retained.
        result = slugify("abc123")
        assert result == "abc123"

    def test_single_character_string(self):
        """Test single character"""
        # Single character should remain unchanged.
        result = slugify("a")
        assert result == "a"

    def test_single_number(self):
        """Test single number"""
        # Single digit should remain unchanged.
        result = slugify("5")
        assert result == "5"

    def test_single_special_character(self):
        """Test single special character"""
        # Single special char should be stripped.
        result = slugify("!")
        assert result == ""

    def test_hyphen_only(self):
        """Test hyphen only"""
        # Hyphen-only should be stripped to empty.
        result = slugify("-")
        assert result == ""

    def test_whitespace_variations(self):
        """Test various whitespace"""
        # Mixed whitespace should collapse to single hyphen.
        result = slugify("hello \t\n world")
        assert result == "hello-world"


class TestSlugifyRealWorldScenarios:
    """Real-world usage scenarios"""

    def test_blog_post_title(self):
        """Test blog post title slugification"""
        # Converts title to URL-friendly slug.
        title = "How to Build a Web App in 2024!"
        result = slugify(title)
        assert result == "how-to-build-a-web-app-in-2024"

    def test_product_name(self):
        """Test product name slugification"""
        # Preserves numbers and lowercases product names.
        name = "iPhone 15 Pro Max"
        result = slugify(name)
        assert result == "iphone-15-pro-max"

    def test_article_title_with_punctuation(self):
        """Test article title with punctuation"""
        # Removes punctuation and lowercases.
        title = "Breaking: New Discovery in Science!"
        result = slugify(title)
        assert result == "breaking-new-discovery-in-science"

    def test_url_friendly_conversion(self):
        """Test URL-friendly conversion"""
        # Removes special characters for URL safety.
        text = "User Profile & Settings (Updated)"
        result = slugify(text)
        assert result == "user-profile-settings-updated"

    def test_document_filename(self):
        """Test document filename conversion"""
        # Converts filename to slug with extension retained.
        filename = "Q4 2024 Financial Report.pdf"
        result = slugify(filename)
        assert result == "q4-2024-financial-report-pdf"

    def test_email_subject_line(self):
        """Test email subject line"""
        # Removes punctuation and lowercases.
        subject = "Meeting Tomorrow @ 3PM - URGENT!"
        result = slugify(subject)
        assert result == "meeting-tomorrow-3pm-urgent"

    def test_twitter_hashtag_text(self):
        """Test twitter-like text with hashtags"""
        # Removes hash symbols and lowercases.
        text = "#Python #WebDevelopment #Programming"
        result = slugify(text)
        assert result == "python-webdevelopment-programming"

    def test_product_category_path(self):
        """Test category path for URL"""
        # Removes ampersand, keeps words.
        category = "Electronics & Computers"
        result = slugify(category)
        assert result == "electronics-computers"

    def test_user_display_name(self):
        """Test user display name"""
        # Apostrophe splits words; parentheses removed.
        name = "John O'Brien (Developer)"
        result = slugify(name)
        # Apostrophe is treated as a separator
        assert result == "john-o-brien-developer"

    def test_technical_term(self):
        """Test technical term with special notation"""
        # Special characters removed, digits preserved.
        term = "C++ Programming (v2.0)"
        result = slugify(term)
        assert result == "c-programming-v2-0"

    def test_search_query(self):
        """Test search query"""
        # Punctuation removed; words preserved.
        query = "how to make sushi? (beginner)"
        result = slugify(query)
        assert result == "how-to-make-sushi-beginner"

    def test_academic_title(self):
        """Test academic title"""
        # Dots removed, words preserved.
        title = "Ph.D. in Computer Science (2024)"
        result = slugify(title)
        assert result == "ph-d-in-computer-science-2024"

    def test_currency_amount(self):
        """Test currency amount in text"""
        # Currency symbols removed, numbers preserved.
        text = "Price: $99.99 (Save 50%!)"
        result = slugify(text)
        assert result == "price-99-99-save-50"

    def test_mathematical_expression_in_text(self):
        """Test mathematical expression in text"""
        # Operators removed; digits preserved.
        text = "2 + 2 = 4 is basic math"
        result = slugify(text)
        assert result == "2-2-4-is-basic-math"

    def test_time_format_in_text(self):
        """Test time format in text"""
        # Colons removed; digits preserved.
        text = "Meeting at 3:30 PM today"
        result = slugify(text)
        assert result == "meeting-at-3-30-pm-today"

    def test_date_format_in_text(self):
        """Test date format in text"""
        # Date separators preserved as hyphens.
        text = "Meeting on 2024-12-25"
        result = slugify(text)
        assert result == "meeting-on-2024-12-25"


class TestSlugifyConsistency:
    """Test consistency and idempotence"""

    def test_consistent_repeated_calls(self):
        """Test same input produces same output"""
        # Output should be stable across calls.
        text = "Hello World! 123"
        result1 = slugify(text)
        result2 = slugify(text)
        assert result1 == result2

    def test_idempotence_on_slug(self):
        """Test that slugifying a slug returns same slug"""
        # Edge case: slugifying an existing slug should be stable.
        text = "hello-world-123"
        result = slugify(text)
        # Since hyphen gets converted, this might not be perfectly idempotent
        # but multiple runs should be consistent
        result2 = slugify(result)
        assert result == result2

    def test_repeated_slugification(self):
        """Test repeated slugification"""
        # Multiple passes should be consistent.
        text = "Hello World!"
        result1 = slugify(text)
        result2 = slugify(result1)
        result3 = slugify(result2)
        assert result1 == result2 == result3


class TestSlugifyLowercase:
    """Test lowercase conversion"""

    def test_all_uppercase_converted(self):
        """Test all uppercase is converted to lowercase"""
        # Uppercase should be lowercased.
        result = slugify("HELLO WORLD")
        assert result == "hello-world"
        assert result.islower()

    def test_mixed_case_converted_to_lowercase(self):
        """Test mixed case is converted to lowercase"""
        # Mixed case should be lowercased.
        result = slugify("HeLLo WoRLd")
        assert result == "hello-world"
        assert result.islower()

    def test_numbers_preserved_as_is(self):
        """Test numbers are preserved"""
        # Numbers should remain unchanged.
        result = slugify("Hello123World456")
        assert "123" in result
        assert "456" in result

    def test_no_uppercase_in_result(self):
        """Test result contains no uppercase letters"""
        # Result should be entirely lowercase.
        result = slugify("The QUICK Brown FOX Jumps")
        assert result.islower()


class TestSlugifyAlphanumericFilter:
    """Test alphanumeric character filtering"""

    def test_only_alphanumeric_and_hyphens(self):
        """Test result contains only alphanumeric and hyphens"""
        # Output should contain only a-z, 0-9, and hyphens.
        result = slugify("hello@world!test#case$sample%")
        # Should only contain a-z, 0-9, and hyphens
        assert all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in result)

    def test_consecutive_special_chars_become_single_hyphen(self):
        """Test consecutive special characters become single hyphen"""
        # Consecutive separators should collapse to one hyphen.
        result = slugify("hello!!!@@@###world")
        assert "---" not in result
        assert result == "hello-world"

    def test_hyphen_replacement_pattern(self):
        """Test that non-alphanumeric sequences become single hyphen"""
        # Non-alphanumeric sequences should become a single hyphen.
        result = slugify("a!@#$%^&*()b")
        assert result == "a-b"
        assert result.count("-") == 1


class TestSlugifyStripBehavior:
    """Test leading/trailing hyphen stripping"""

    def test_leading_hyphens_stripped(self):
        """Test leading hyphens are stripped"""
        # Leading hyphens should be removed.
        result = slugify("---hello")
        assert not result.startswith("-")

    def test_trailing_hyphens_stripped(self):
        """Test trailing hyphens are stripped"""
        # Trailing hyphens should be removed.
        result = slugify("hello---")
        assert not result.endswith("-")

    def test_leading_and_trailing_hyphens_stripped(self):
        """Test both leading and trailing hyphens stripped"""
        # Both ends should be stripped of hyphens.
        result = slugify("---hello---")
        assert not result.startswith("-")
        assert not result.endswith("-")

    def test_internal_hyphens_preserved(self):
        """Test internal hyphens are preserved"""
        # Internal hyphens should remain.
        result = slugify("hello-world-test")
        assert result == "hello-world-test"

    def test_internal_hyphen_from_special_chars(self):
        """Test internal hyphens from special char conversion"""
        # Special characters should turn into internal hyphens.
        result = slugify("hello@world-test")
        assert "hello" in result
        assert "world" in result
        assert "test" in result


class TestSlugifyComplexScenarios:
    """Complex combined scenarios"""

    def test_everything_combined(self):
        """Test complex string with all features"""
        # HTML, punctuation, numbers, and symbols should be normalized.
        text = "  <p>Hello, World! (2024) - $99.99 & More!</p>  "
        result = slugify(text)
        assert result == "hello-world-2024-99-99-more"

    def test_html_plus_unicode_plus_special_chars(self):
        """Test HTML, unicode, and special chars combined"""
        # Unicode normalization should still allow slug creation.
        text = "<p>café résumé @ 50%!</p>"
        result = slugify(text)
        assert "cafe" in result or "café" in result.replace("-", "")

    def test_multiple_transformations_in_sequence(self):
        """Test that all transformations apply correctly"""
        # Edge case: multiple transformations in sequence should be stable.
        text = "  HELLO @#$ WORLD !!!  "
        result = slugify(text)
        # Should be: stripped, cleaned, lowercased, special chars removed/replaced
        assert result == "hello-world"
        assert result.islower()
        assert not result.startswith("-")
        assert not result.endswith("-")

    def test_url_slug_generation(self):
        """Test generating URL-safe slug"""
        # Output should be URL-safe and alphanumeric/hyphen only.
        title = "My First Blog Post! (Updated v2.0)"
        result = slugify(title)
        # Should be suitable for URL
        assert result.replace("-", "").replace("2", "").replace("0", "").isalpha() or "2" in result or "0" in result
        assert all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in result)

    def test_slug_for_file_naming(self):
        """Test slug suitable for file naming"""
        # Output should avoid filesystem-forbidden characters.
        filename = "Document (Draft) - v1.2.3.pdf"
        result = slugify(filename)
        # Should be file system safe
        assert not any(c in result for c in '<>:"|?*\\')


class TestSlugifyPerformance:
    """Performance and stress test scenarios"""

    def test_very_long_string_with_many_spaces(self):
        """Test very long string"""
        # Edge case: long inputs should still return a slug.
        text = " hello world " * 1000
        result = slugify(text)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_very_long_string_with_special_chars(self):
        """Test long string with special characters"""
        # Edge case: punctuation-only input may yield empty slug.
        text = "!@#$%^&*() " * 500
        result = slugify(text)
        # Should either be empty or contain only hyphens that get stripped
        assert isinstance(result, str)

    def test_alternating_text_and_special_chars(self):
        """Test alternating text and special chars"""
        # Alternating text and separators should yield hyphenated output.
        text = "a!b@c#d$e%"
        result = slugify(text)
        assert result == "a-b-c-d-e"

    def test_large_unicode_string(self):
        """Test large unicode string"""
        # Large Unicode input should still return a slug string.
        text = "café " * 1000
        result = slugify(text)
        assert isinstance(result, str)
