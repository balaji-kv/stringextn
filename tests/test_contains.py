"""Test suite for stringextn.contains module.

Validates contains_any and contains_all behavior across typical usage,
edge cases, and real-world scenarios using substring-based matching.
"""

import pytest
from stringextn.contains import contains_any, contains_all


class TestContainsAny:
    """Test cases for contains_any function"""

    def test_single_item_found(self):
        """Test finding a single item that exists"""
        # Expects True when at least one item is present in the string.
        assert contains_any("hello world", ["hello"]) is True

    def test_single_item_not_found(self):
        """Test single item that doesn't exist"""
        # Expects False when no items are present.
        assert contains_any("hello world", ["xyz"]) is False

    def test_multiple_items_first_found(self):
        """Test multiple items with first one found"""
        # Expects True if any item matches (first item matches here).
        assert contains_any("hello world", ["hello", "xyz"]) is True

    def test_multiple_items_last_found(self):
        """Test multiple items with last one found"""
        # Expects True if any item matches (last item matches here).
        assert contains_any("hello world", ["xyz", "world"]) is True

    def test_multiple_items_middle_found(self):
        """Test multiple items with middle one found"""
        # Expects True when any substring matches, regardless of position.
        assert contains_any("hello world", ["xyz", "o w", "abc"]) is True

    def test_multiple_items_none_found(self):
        """Test multiple items with none found"""
        # Expects False when no items match.
        assert contains_any("hello world", ["xyz", "abc", "def"]) is False

    def test_all_items_found(self):
        """Test all items are found"""
        # Expects True because at least one item matches (both match here).
        assert contains_any("hello world", ["hello", "world"]) is True

    def test_empty_items_list(self):
        """Test with empty items list"""
        # Expects False when there are no items to match.
        assert contains_any("hello world", []) is False

    def test_empty_string(self):
        """Test with empty string"""
        # Expects False when the haystack is empty and items are non-empty.
        assert contains_any("", ["hello"]) is False

    def test_empty_string_and_empty_items(self):
        """Test with both empty string and empty items list"""
        # Expects False when there are no items to match.
        assert contains_any("", []) is False

    def test_case_sensitive(self):
        """Test that search is case sensitive"""
        # Expects False because case-sensitive substring does not match.
        assert contains_any("Hello World", ["hello"]) is False

    def test_case_sensitive_match(self):
        """Test case sensitive match"""
        # Expects True when the exact case matches.
        assert contains_any("Hello World", ["Hello"]) is True

    def test_substring_matching(self):
        """Test that it finds substrings"""
        # Expects True because substring matching is used.
        assert contains_any("hello world", ["ll", "ld"]) is True

    def test_substring_not_found(self):
        """Test substring not found"""
        # Expects False when substrings are absent.
        assert contains_any("hello world", ["xyz"]) is False

    def test_space_in_search(self):
        """Test searching for items with spaces"""
        # Expects True when a spaced substring appears in the string.
        assert contains_any("hello world test", ["o w", "world test"]) is True

    def test_special_characters(self):
        """Test with special characters"""
        # Expects True for literal substring matching of special characters.
        assert contains_any("hello@world#test", ["@world"]) is True

    def test_special_characters_not_found(self):
        """Test special characters not found"""
        # Expects False when special character substring is absent.
        assert contains_any("hello world", ["@"]) is False

    def test_numbers_in_string(self):
        """Test with numbers"""
        # Expects True when numeric substrings are present.
        assert contains_any("test123abc", ["123", "abc"]) is True

    def test_numbers_not_found(self):
        """Test numbers not found"""
        # Expects False when numeric substring is absent.
        assert contains_any("hello world", ["123"]) is False

    def test_single_character_search(self):
        """Test single character search"""
        # Expects True when a single character substring is present.
        assert contains_any("hello", ["o"]) is True

    def test_single_character_not_found(self):
        """Test single character not found"""
        # Expects False when the character is not present.
        assert contains_any("hello", ["z"]) is False

    def test_whole_string_as_item(self):
        """Test entire string as search item"""
        # Expects True when the full string matches.
        assert contains_any("hello", ["hello"]) is True

    def test_whole_string_as_item_not_found(self):
        """Test entire string as search item but longer"""
        # Expects False when the item is longer than the string.
        assert contains_any("hello", ["hello world"]) is False

    def test_newline_character(self):
        """Test with newline character"""
        # Expects True when the newline character is present.
        assert contains_any("hello\nworld", ["\n"]) is True

    def test_tab_character(self):
        """Test with tab character"""
        # Expects True when the tab character is present.
        assert contains_any("hello\tworld", ["\t"]) is True

    def test_unicode_characters(self):
        """Test with unicode characters"""
        # Expects True for exact Unicode substring match.
        assert contains_any("café", ["café"]) is True

    def test_unicode_not_found(self):
        """Test unicode not found"""
        # Expects False when the Unicode character is absent.
        assert contains_any("hello", ["é"]) is False

    def test_items_with_duplicates(self):
        """Test items list with duplicates"""
        # Expects True when any duplicate item matches.
        assert contains_any("hello world", ["hello", "hello", "world"]) is True

    def test_long_search_string(self):
        """Test with very long search string"""
        # Expects True when the long string contains the target substring.
        long_string = "a" * 10000 + "hello" + "b" * 10000
        assert contains_any(long_string, ["hello"]) is True

    def test_many_items_first_match(self):
        """Test with many items and first matches"""
        # Expects True when the first item matches in a large list.
        items = ["x" + str(i) for i in range(100)]
        items[0] = "hello"
        assert contains_any("hello world", items) is True

    def test_many_items_last_match(self):
        """Test with many items and last matches"""
        # Expects True when the last item matches in a large list.
        items = ["x" + str(i) for i in range(100)]
        items[-1] = "world"
        assert contains_any("hello world", items) is True

    def test_many_items_no_match(self):
        """Test with many items and no matches"""
        # Expects False when none of the items match.
        items = ["x" + str(i) for i in range(100)]
        assert contains_any("hello world", items) is False

    def test_empty_string_in_items(self):
        """Test with empty string in items list"""
        # Edge case: Empty string is always contained in any string.
        assert contains_any("hello", [""]) is True

    def test_empty_string_in_items_with_other_items(self):
        """Test empty string in items with other items"""
        # Empty string is always contained in any string
        assert contains_any("hello", ["", "xyz"]) is True

    def test_items_as_tuple(self):
        """Test with items as tuple instead of list"""
        # Expects True when iterable is a tuple.
        assert contains_any("hello world", ("hello", "xyz")) is True

    def test_items_as_generator(self):
        """Test with items as generator"""
        # Expects True when iterable is a generator.
        items = (x for x in ["hello", "xyz"])
        assert contains_any("hello world", items) is True

    def test_overlapping_items(self):
        """Test with overlapping search items"""
        # Expects True when any overlapping substring matches.
        assert contains_any("hello", ["hel", "ell", "llo"]) is True

    def test_prefix_and_suffix(self):
        """Test with prefix and suffix patterns"""
        # Expects True when any item matches regardless of position.
        assert contains_any("hello world", ["hello", "world"]) is True

    def test_word_boundaries_not_respected(self):
        """Test that word boundaries are not respected"""
        # contains_any does substring matching, not word matching
        assert contains_any("hello world", ["llo"]) is True

    def test_repeated_characters(self):
        """Test with repeated characters"""
        # Expects True when repeated sequence is found.
        assert contains_any("aaabbbccc", ["bbb"]) is True

    def test_consecutive_search_items(self):
        """Test searching for consecutive character groups"""
        # Expects True when any of the substrings match.
        assert contains_any("hello world", ["hel", "llo", "o w", "wor"]) is True


class TestContainsAll:
    """Test cases for contains_all function"""

    def test_single_item_found(self):
        """Test finding a single item that exists"""
        # Expects True when the required item is present.
        assert contains_all("hello world", ["hello"]) is True

    def test_single_item_not_found(self):
        """Test single item that doesn't exist"""
        # Expects False when any required item is missing.
        assert contains_all("hello world", ["xyz"]) is False

    def test_multiple_items_all_found(self):
        """Test multiple items all found"""
        # Expects True when all required items are present.
        assert contains_all("hello world", ["hello", "world"]) is True

    def test_multiple_items_one_missing(self):
        """Test multiple items with one missing"""
        # Expects False when at least one required item is missing.
        assert contains_all("hello world", ["hello", "xyz"]) is False

    def test_multiple_items_all_missing(self):
        """Test multiple items all missing"""
        # Expects False when none of the required items are present.
        assert contains_all("hello world", ["xyz", "abc"]) is False

    def test_empty_items_list(self):
        """Test with empty items list"""
        # Edge case: all() on empty iterable returns True.
        assert contains_all("hello world", []) is True

    def test_empty_string(self):
        """Test with empty string"""
        # Expects False when the haystack is empty and items are non-empty.
        assert contains_all("", ["hello"]) is False

    def test_empty_string_and_empty_items(self):
        """Test with both empty string and empty items list"""
        # Edge case: empty items list returns True even with empty string.
        assert contains_all("", []) is True

    def test_case_sensitive(self):
        """Test that search is case sensitive"""
        # Expects False for case mismatch.
        assert contains_all("Hello World", ["hello"]) is False

    def test_case_sensitive_match(self):
        """Test case sensitive match"""
        # Expects True for exact case matches.
        assert contains_all("Hello World", ["Hello", "World"]) is True

    def test_substring_matching(self):
        """Test that it finds substrings"""
        # Expects True when all substrings are present.
        assert contains_all("hello world", ["ll", "ld"]) is True

    def test_substring_not_found(self):
        """Test substring not found"""
        # Expects False when any substring is absent.
        assert contains_all("hello world", ["xyz"]) is False

    def test_space_in_search(self):
        """Test searching for items with spaces"""
        # Expects True when all spaced substrings are present.
        assert contains_all("hello world test", ["o w", "test"]) is True

    def test_space_in_search_not_all_found(self):
        """Test space search with not all found"""
        # Expects False when a required spaced substring is missing.
        assert contains_all("hello world", ["o w", "xyz"]) is False

    def test_special_characters(self):
        """Test with special characters"""
        # Expects True for literal matches containing special characters.
        assert contains_all("hello@world#test", ["@world", "#test"]) is True

    def test_special_characters_not_all_found(self):
        """Test special characters not all found"""
        # Expects False when any special-character substring is missing.
        assert contains_all("hello world", ["@", "#"]) is False

    def test_numbers_in_string(self):
        """Test with numbers"""
        # Expects True when all numeric substrings are present.
        assert contains_all("test123abc", ["123", "abc"]) is True

    def test_numbers_not_all_found(self):
        """Test numbers not all found"""
        # Expects False when required numeric substrings are missing.
        assert contains_all("hello world", ["123", "456"]) is False

    def test_single_character_search(self):
        """Test single character search"""
        # Expects True when required character is present.
        assert contains_all("hello", ["o"]) is True

    def test_single_character_not_found(self):
        """Test single character not found"""
        # Expects False when required character is absent.
        assert contains_all("hello", ["z"]) is False

    def test_whole_string_as_item(self):
        """Test entire string as search item"""
        # Expects True when the full string matches.
        assert contains_all("hello", ["hello"]) is True

    def test_whole_string_as_item_not_found(self):
        """Test entire string as search item but longer"""
        # Expects False when item is longer than the string.
        assert contains_all("hello", ["hello world"]) is False

    def test_newline_character(self):
        """Test with newline character"""
        # Expects True when newline is required and present.
        assert contains_all("hello\nworld", ["\n"]) is True

    def test_tab_character(self):
        """Test with tab character"""
        # Expects True when tab is required and present.
        assert contains_all("hello\tworld", ["\t"]) is True

    def test_unicode_characters(self):
        """Test with unicode characters"""
        # Expects True when all Unicode substrings are present.
        assert contains_all("café latté", ["café", "latté"]) is True

    def test_unicode_not_all_found(self):
        """Test unicode not all found"""
        # Expects False when any Unicode substring is missing.
        assert contains_all("hello", ["é", "à"]) is False

    def test_items_with_duplicates(self):
        """Test items list with duplicates"""
        # Expects True when all unique required items are present.
        assert contains_all("hello world", ["hello", "hello", "world"]) is True

    def test_items_with_duplicates_not_all_found(self):
        """Test items with duplicates not all found"""
        # Expects False when a required item is missing.
        assert contains_all("hello", ["hello", "hello", "xyz"]) is False

    def test_long_search_string(self):
        """Test with very long search string"""
        # Expects True when all required substrings appear in long input.
        long_string = "a" * 10000 + "hello" + "b" * 10000 + "world" + "c" * 10000
        assert contains_all(long_string, ["hello", "world"]) is True

    def test_many_items_all_found(self):
        """Test with many items all found"""
        # Expects True when all required items are present in large input.
        long_string = "".join([str(i) for i in range(100)])
        items = [str(i) for i in range(0, 50)]
        assert contains_all(long_string, items) is True

    def test_many_items_some_not_found(self):
        """Test with many items some not found"""
        # Expects False when at least one required item is missing.
        items = ["x" + str(i) for i in range(100)]
        assert contains_all("hello world", items) is False

    def test_empty_string_in_items(self):
        """Test with empty string in items list"""
        # Edge case: Empty string is always contained in any string.
        assert contains_all("hello", [""]) is True

    def test_empty_string_in_items_with_other_items(self):
        """Test empty string in items with other items"""
        # Edge case: Empty string does not prevent matching other items.
        assert contains_all("hello", ["", "hello"]) is True

    def test_empty_string_in_items_with_missing_item(self):
        """Test empty string in items with missing item"""
        # Empty string is always contained, but "xyz" is not
        assert contains_all("hello", ["", "xyz"]) is False

    def test_items_as_tuple(self):
        """Test with items as tuple instead of list"""
        # Expects True when iterable is a tuple.
        assert contains_all("hello world", ("hello", "world")) is True

    def test_items_as_generator(self):
        """Test with items as generator"""
        # Expects True when iterable is a generator.
        items = (x for x in ["hello", "world"])
        assert contains_all("hello world", items) is True

    def test_overlapping_items(self):
        """Test with overlapping search items"""
        # Expects True when all overlapping substrings are present.
        assert contains_all("hello", ["hel", "ell", "llo"]) is True

    def test_non_overlapping_items(self):
        """Test with non-overlapping items"""
        # Expects True when all required items appear in the string.
        assert contains_all("hello world", ["hello", "world"]) is True

    def test_prefix_and_suffix(self):
        """Test with prefix and suffix patterns"""
        # Expects True when all required items are present regardless of position.
        assert contains_all("hello world", ["hello", "world"]) is True

    def test_word_boundaries_not_respected(self):
        """Test that word boundaries are not respected"""
        # Expects True because substring matching ignores word boundaries.
        assert contains_all("hello world", ["llo", "wor"]) is True

    def test_repeated_characters(self):
        """Test with repeated characters"""
        # Expects True when all repeated sequences are present.
        assert contains_all("aaabbbccc", ["aaa", "bbb", "ccc"]) is True

    def test_repeated_characters_not_all_found(self):
        """Test repeated characters not all found"""
        # Expects False when one required sequence is missing.
        assert contains_all("aaabbb", ["aaa", "bbb", "ccc"]) is False

    def test_consecutive_search_items(self):
        """Test searching for consecutive character groups"""
        # Expects True when all required substrings are present.
        assert contains_all("hello world", ["hel", "wor"]) is True

    def test_order_independent(self):
        """Test that order of items doesn't matter"""
        # Expects True even when items are out of order.
        assert contains_all("hello world", ["world", "hello"]) is True

    def test_case_differences_fail(self):
        """Test that case differences cause failure"""
        # Expects False for case mismatches.
        assert contains_all("Hello World", ["hello", "world"]) is False

    def test_whitespace_items(self):
        """Test with whitespace in items"""
        # Expects True when all whitespace-containing substrings are present.
        assert contains_all("hello world test", ["hello world", "world test"]) is True

    def test_whitespace_items_not_all(self):
        """Test whitespace items not all found"""
        # Expects False when any required whitespace substring is missing.
        assert contains_all("hello world", ["hello world", "world xyz"]) is False


class TestComparisonBetweenFunctions:
    """Test comparisons between contains_any and contains_all"""

    def test_any_vs_all_single_found(self):
        """Test both return True when single item found"""
        # Expects both functions to succeed when the item exists.
        assert contains_any("hello", ["hello"]) is True
        assert contains_all("hello", ["hello"]) is True

    def test_any_vs_all_single_not_found(self):
        """Test both return False when single item not found"""
        # Expects both functions to fail when the item is missing.
        assert contains_any("hello", ["xyz"]) is False
        assert contains_all("hello", ["xyz"]) is False

    def test_any_multiple_one_found_vs_all(self):
        """Test difference with multiple items - one found"""
        # Expects contains_any True while contains_all False.
        items = ["hello", "xyz"]
        assert contains_any("hello world", items) is True
        assert contains_all("hello world", items) is False

    def test_any_vs_all_multiple_all_found(self):
        """Test both return True when all items found"""
        # Expects both functions True when all items match.
        items = ["hello", "world"]
        assert contains_any("hello world", items) is True
        assert contains_all("hello world", items) is True

    def test_any_vs_all_empty_items(self):
        """Test behavior with empty items"""
        # Edge case: contains_any False, contains_all True with empty items.
        assert contains_any("hello", []) is False
        assert contains_all("hello", []) is True

    def test_any_vs_all_empty_string(self):
        """Test behavior with empty string"""
        # Expects False for both when string is empty and items are non-empty.
        assert contains_any("", ["hello"]) is False
        assert contains_all("", ["hello"]) is False

    def test_any_with_none_found_vs_all(self):
        """Test when none of multiple items found"""
        # Expects both functions to return False when no items match.
        items = ["xyz", "abc", "def"]
        assert contains_any("hello", items) is False
        assert contains_all("hello", items) is False

    def test_any_first_found_vs_all(self):
        """Test any returns True if first found (even if others missing)"""
        # Expects contains_any True and contains_all False when only one matches.
        items = ["hello", "xyz", "abc"]
        assert contains_any("hello world", items) is True
        assert contains_all("hello world", items) is False


class TestRealWorldScenarios:
    """Real-world usage scenarios"""

    def test_validate_password_contains_requirements_any(self):
        """Test checking if password contains any special character"""
        # Expects True when any required special character appears.
        special_chars = ["!", "@", "#", "$", "%"]
        assert contains_any("myPassword123!", special_chars) is True

    def test_validate_password_contains_requirements_all(self):
        """Test checking if password contains all required types"""
        # Expects False for literal substring placeholders, True for actual chars.
        password = "Abc123!@#"
        requirements = ["A-Z", "0-9", "!@"]
        # Note: this isn't perfect since it's looking for exact substrings
        assert contains_all(password, requirements) is False  # "A-Z" not found as substring
        assert contains_all(password, ["A", "1", "!"]) is True

    def test_search_tags_any(self):
        """Test searching for any of multiple tags"""
        # Expects True when any tag exists in content.
        post_content = "#python #coding #tutorial"
        tags = ["#javascript", "#python", "#ruby"]
        assert contains_any(post_content, tags) is True

    def test_search_tags_all(self):
        """Test checking if content has all required tags"""
        # Expects True when all required tags are present.
        post_content = "#python #coding #tutorial"
        required_tags = ["#python", "#coding"]
        assert contains_all(post_content, required_tags) is True

    def test_filter_emails_any_domain(self):
        """Test finding emails from any domain"""
        # Expects True when any domain substring matches.
        email = "user@gmail.com"
        domains = ["@yahoo.com", "@gmail.com", "@outlook.com"]
        assert contains_any(email, domains) is True

    def test_filter_emails_all_parts(self):
        """Test email contains all necessary parts"""
        # Expects True when required parts like '@' and '.' are present.
        email = "user@gmail.com"
        parts = ["@", "."]
        assert contains_all(email, parts) is True

    def test_content_warning_any_keyword(self):
        """Test if content contains any warning keyword"""
        # Expects True when any keyword is present.
        text = "This is a warning message"
        keywords = ["error", "warning", "critical"]
        assert contains_any(text, keywords) is True

    def test_content_filter_all_keywords(self):
        """Test if content must contain all keywords"""
        # Expects True when all keywords are present.
        text = "This is a critical error warning"
        keywords = ["critical", "error", "warning"]
        assert contains_all(text, keywords) is True

    def test_url_validation(self):
        """Test checking if URL contains protocol"""
        # Expects True when any protocol substring matches.
        url = "https://example.com"
        protocols = ["http://", "https://", "ftp://"]
        assert contains_any(url, protocols) is True

    def test_file_extension_check(self):
        """Test checking for any allowed file extension"""
        # Expects True when any extension matches.
        filename = "document.pdf"
        extensions = [".pdf", ".doc", ".docx"]
        assert contains_any(filename, extensions) is True

    def test_filename_validation_all_parts(self):
        """Test filename has all required parts"""
        # Expects True when all required parts are present.
        filename = "report_2024_final.pdf"
        parts = ["_", ".", "pdf"]
        assert contains_all(filename, parts) is True

    def test_log_message_severity(self):
        """Test log message contains severity level"""
        # Expects True when any severity marker is present.
        log_msg = "[ERROR] Database connection failed"
        severity_levels = ["[INFO]", "[DEBUG]", "[ERROR]"]
        assert contains_any(log_msg, severity_levels) is True

    def test_code_quality_checks_any(self):
        """Test code contains any bad patterns"""
        # Expects True when any forbidden pattern appears.
        code = "var x = eval(input);"
        bad_patterns = ["eval(", "exec(", "compile("]
        assert contains_any(code, bad_patterns) is True

    def test_html_validation(self):
        """Test HTML contains required tags"""
        # Expects True when all required tags are present.
        html = "<html><head><title>Page</title></head><body></body></html>"
        required_tags = ["<html>", "<body>"]
        assert contains_all(html, required_tags) is True

    def test_string_localization_search(self):
        """Test string contains any locale indicator"""
        # Expects True when any accented character is present.
        text = "Café résumé naïve"
        special_chars = ["é", "ï"]
        assert contains_any(text, special_chars) is True


class TestPerformance:
    """Performance-related test cases"""

    def test_short_string_single_item(self):
        """Test with short string and single item"""
        # Expects True for exact match on short input.
        assert contains_any("hello", ["hello"]) is True

    def test_medium_string_medium_items(self):
        """Test with medium string and medium items"""
        # Expects True when a matching item exists in a medium list.
        items = [f"item{i}" for i in range(50)]
        items[25] = "hello"
        assert contains_any("hello world", items) is True

    def test_short_circuit_behavior_any(self):
        """Test that contains_any short circuits on first match"""
        # Expects True without needing to evaluate later items.
        items = ["hello", "should_not_be_checked"]
        # Should return True without checking second item
        assert contains_any("hello world", items) is True

    def test_early_termination_all(self):
        """Test that contains_all can terminate early on missing item"""
        # Expects False when a required item is missing, without full scan.
        items = ["world", "missing_item"]
        # Should return False without checking all items
        assert contains_all("hello world", items) is False
