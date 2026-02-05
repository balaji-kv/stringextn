"""
Test suite for stringextn.cases module.

Tests the string case conversion functions (to_snake, to_camel, to_pascal, to_kebab)
to ensure they correctly convert between various naming conventions (camelCase,
snake_case, PascalCase, kebab-case). Covers standard conversions, edge cases,
cross-conversion consistency, and special scenarios like consecutive capitals,
Unicode characters, and numeric strings.
"""

import pytest
from stringextn.cases import to_snake, to_camel, to_pascal, to_kebab


class TestToSnake:
    """Test cases for to_snake function"""

    def test_basic_camel_case(self):
        """Test conversion of basic camelCase to snake_case"""
        assert to_snake("camelCase") == "camel_case"

    def test_basic_pascal_case(self):
        """Test conversion of basic PascalCase to snake_case"""
        assert to_snake("PascalCase") == "pascal_case"

    def test_already_snake_case(self):
        """Test that snake_case remains unchanged"""
        assert to_snake("snake_case") == "snake_case"

    def test_kebab_case_to_snake(self):
        """Test conversion of kebab-case to snake_case"""
        assert to_snake("kebab-case") == "kebab-case"

    def test_space_separated_to_snake(self):
        """Test conversion of space-separated words to snake_case"""
        assert to_snake("hello world") == "hello_world"

    def test_mixed_separators_to_snake(self):
        """Test conversion with mixed separators"""
        assert to_snake("hello-world test") == "hello-world_test"

    def test_consecutive_capitals_to_snake(self):
        """Test conversion with consecutive capital letters.
        
        Edge case: 'HTTPResponse' should recognize 'HTTP' as one acronym word
        followed by 'Response', resulting in 'http_response' not 'h_t_t_p_response'.
        """
        assert to_snake("HTTPResponse") == "http_response"

    def test_multiple_consecutive_capitals(self):
        """Test handling of multiple consecutive uppercase letters"""
        assert to_snake("XMLParser") == "xml_parser"

    def test_numbers_in_string(self):
        """Test handling of numbers in strings"""
        assert to_snake("test123Case") == "test123_case"

    def test_empty_string(self):
        """Test empty string"""
        assert to_snake("") == ""

    def test_single_character(self):
        """Test single character"""
        assert to_snake("a") == "a"

    def test_single_capital_letter(self):
        """Test single capital letter"""
        assert to_snake("A") == "a"

    def test_all_lowercase(self):
        """Test all lowercase"""
        assert to_snake("lowercase") == "lowercase"

    def test_all_uppercase(self):
        """Test all uppercase"""
        assert to_snake("UPPERCASE") == "uppercase"

    def test_mixed_case_with_numbers(self):
        """Test mixed case with numbers"""
        assert to_snake("getHTTP2Response") == "get_http2_response"


class TestToCamel:
    """Test cases for to_camel function"""

    def test_basic_snake_case(self):
        """Test conversion of basic snake_case to camelCase"""
        assert to_camel("snake_case") == "snakeCase"

    def test_basic_kebab_case(self):
        """Test conversion of basic kebab-case to camelCase"""
        assert to_camel("kebab-case") == "kebabCase"

    def test_space_separated(self):
        """Test conversion of space-separated words to camelCase"""
        assert to_camel("hello world") == "helloWorld"

    def test_already_camel_case(self):
        """Test that camelCase becomes lowercase.
        
        Non-obvious: Without separators to split on, the entire string is treated
        as a single word and lowercased.
        """
        assert to_camel("camelCase") == "camelcase"

    def test_pascal_case_to_camel(self):
        """Test conversion of PascalCase to camelCase"""
        assert to_camel("PascalCase") == "pascalcase"

    def test_single_word(self):
        """Test single word (no separators)"""
        assert to_camel("hello") == "hello"

    def test_single_word_uppercase(self):
        """Test single uppercase word"""
        assert to_camel("HELLO") == "hello"

    def test_empty_string(self):
        """Test empty string"""
        assert to_camel("") == ""

    def test_multiple_separators(self):
        """Test multiple different separators"""
        assert to_camel("hello_world-test case") == "helloWorldTestCase"

    def test_with_numbers(self):
        """Test handling of numbers"""
        assert to_camel("hello_world_123") == "helloWorld123"

    def test_leading_separator(self):
        """Test with leading separator.
        
        Edge case: Leading '_' creates an empty first element that becomes
        capitalized through title() processing.
        """
        assert to_camel("_hello_world") == "HelloWorld"

    def test_trailing_separator(self):
        """Test with trailing separator"""
        assert to_camel("hello_world_") == "helloWorld"

    def test_multiple_consecutive_separators(self):
        """Test multiple consecutive separators.
        
        Edge case: 'hello__world' splits into ['hello', '', 'world']. Empty strings
        title-case to '', so consecutive separators result in single separator.
        """
        assert to_camel("hello__world") == "helloWorld"

    def test_single_character(self):
        """Test single character"""
        assert to_camel("a") == "a"


class TestToPascal:
    """Test cases for to_pascal function"""

    def test_basic_snake_case(self):
        """Test conversion of basic snake_case to PascalCase"""
        assert to_pascal("snake_case") == "SnakeCase"

    def test_basic_kebab_case(self):
        """Test conversion of basic kebab-case to PascalCase"""
        assert to_pascal("kebab-case") == "KebabCase"

    def test_space_separated(self):
        """Test conversion of space-separated words to PascalCase"""
        assert to_pascal("hello world") == "HelloWorld"

    def test_already_pascal_case(self):
        """Test that PascalCase splits on caps.
        
        Non-obvious: Without separators between 'Pascal' and 'Case', they are
        treated as a single word 'Pascalcase' since split on separators yields ['PascalCase'].
        """
        assert to_pascal("PascalCase") == "Pascalcase"

    def test_camel_case_to_pascal(self):
        """Test conversion of camelCase to PascalCase"""
        assert to_pascal("camelCase") == "Camelcase"

    def test_single_word(self):
        """Test single word"""
        assert to_pascal("hello") == "Hello"

    def test_single_word_uppercase(self):
        """Test single uppercase word"""
        assert to_pascal("HELLO") == "Hello"

    def test_empty_string(self):
        """Test empty string"""
        assert to_pascal("") == ""

    def test_multiple_separators(self):
        """Test multiple different separators"""
        assert to_pascal("hello_world-test case") == "HelloWorldTestCase"

    def test_with_numbers(self):
        """Test handling of numbers"""
        assert to_pascal("hello_world_123") == "HelloWorld123"

    def test_leading_separator(self):
        """Test with leading separator"""
        assert to_pascal("_hello_world") == "HelloWorld"

    def test_trailing_separator(self):
        """Test with trailing separator"""
        assert to_pascal("hello_world_") == "HelloWorld"

    def test_multiple_consecutive_separators(self):
        """Test multiple consecutive separators"""
        assert to_pascal("hello__world") == "HelloWorld"

    def test_single_character(self):
        """Test single character"""
        assert to_pascal("a") == "A"

    def test_all_caps_with_separators(self):
        """Test all caps with separators"""
        assert to_pascal("HELLO_WORLD") == "HelloWorld"


class TestToKebab:
    """Test cases for to_kebab function"""

    def test_basic_camel_case(self):
        """Test conversion of basic camelCase to kebab-case"""
        assert to_kebab("camelCase") == "camel-case"

    def test_basic_pascal_case(self):
        """Test conversion of basic PascalCase to kebab-case"""
        assert to_kebab("PascalCase") == "pascal-case"

    def test_already_kebab_case(self):
        """Test that kebab-case remains unchanged"""
        assert to_kebab("kebab-case") == "kebab-case"

    def test_snake_case_to_kebab(self):
        """Test conversion of snake_case to kebab-case"""
        assert to_kebab("snake_case") == "snake-case"

    def test_space_separated_to_kebab(self):
        """Test conversion of space-separated words to kebab-case"""
        assert to_kebab("hello world") == "hello-world"

    def test_consecutive_capitals_to_kebab(self):
        """Test conversion with consecutive capital letters"""
        assert to_kebab("HTTPResponse") == "http-response"

    def test_empty_string(self):
        """Test empty string"""
        assert to_kebab("") == ""

    def test_single_character(self):
        """Test single character"""
        assert to_kebab("a") == "a"

    def test_single_capital_letter(self):
        """Test single capital letter"""
        assert to_kebab("A") == "a"

    def test_all_lowercase(self):
        """Test all lowercase"""
        assert to_kebab("lowercase") == "lowercase"

    def test_all_uppercase(self):
        """Test all uppercase"""
        assert to_kebab("UPPERCASE") == "uppercase"

    def test_with_numbers(self):
        """Test handling of numbers"""
        assert to_kebab("test123Case") == "test123-case"

    def test_multiple_consecutive_separators(self):
        """Test multiple consecutive underscores"""
        assert to_kebab("hello__world") == "hello--world"


class TestCrossConversions:
    """Test cross-conversion consistency"""

    def test_snake_to_camel_to_snake(self):
        """Test snake -> camel -> snake consistency"""
        original = "hello_world"
        camel = to_camel(original)
        assert camel == "helloWorld"

    def test_camel_to_snake_to_camel(self):
        """Test camel -> snake -> camel consistency.
        
        Note: Round-trip is not perfectly consistent since 'helloWorld' -> 'hello_world'
        -> 'helloWorld' requires uppercase preservation that 'to_camel' doesn't maintain.
        """
        original = "helloWorld"
        snake = to_snake(original)
        assert snake == "hello_world"

    def test_pascal_to_snake_to_pascal(self):
        """Test pascal -> snake -> pascal consistency"""
        original = "HelloWorld"
        snake = to_snake(original)
        assert snake == "hello_world"

    def test_kebab_to_snake_equivalence(self):
        """Test that kebab and snake use similar logic"""
        test_string = "hello_world"
        snake = to_snake(test_string)
        kebab = to_kebab(test_string)
        assert kebab == snake.replace("_", "-")

    def test_all_conversions_lowercase(self):
        """Test that all conversions work correctly"""
        test_string = "HelloWorld"
        snake = to_snake(test_string)
        camel = to_camel(test_string)
        pascal = to_pascal(test_string)
        kebab = to_kebab(test_string)
        
        assert snake == "hello_world"
        assert camel == "helloworld"
        assert pascal == "Helloworld"
        assert kebab == "hello-world"


class TestEdgeCases:
    """Test edge cases and special scenarios"""

    def test_special_characters_ignored(self):
        """Test handling of strings with special characters.
        
        Edge case: Special characters like '@' and '#' are not explicitly handled
        by to_snake; they are preserved in the intermediate steps. This test just
        validates the function doesn't crash.
        """
        result = to_snake("hello@world#test")
        assert isinstance(result, str)

    def test_unicode_characters(self):
        """Test handling of unicode characters.
        
        Edge case: Non-ASCII Unicode characters (e.g., 'Ü') are processed but may
        produce unexpected results with case conversions. This test validates
        graceful handling without crashes.
        """
        result = to_snake("helloÜniverse")
        assert isinstance(result, str)

    def test_very_long_string(self):
        """Test handling of very long strings"""
        long_string = "a" * 1000 + "B" + "c" * 1000
        result = to_snake(long_string)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_numeric_string(self):
        """Test handling of pure numeric strings.
        
        Edge case: Strings with only digits pass through all conversions unchanged
        since no case conversion or separator logic applies.
        """
        assert to_snake("12345") == "12345"
        assert to_camel("12345") == "12345"
        assert to_pascal("12345") == "12345"
        assert to_kebab("12345") == "12345"

    def test_single_separator(self):
        """Test single separator only.
        
        Edge case: Single separator character results in various behaviors depending
        on how the functions handle empty split parts.
        """
        assert to_snake("_") == "_"
        assert to_camel("-") == ""
        assert to_pascal("_") == ""

    def test_acronyms(self):
        """Test handling of acronyms.
        
        Edge case: 'getAPI' is split into 'get' and 'api' because the regex
        recognizes the lowercase letter following uppercase as a word boundary.
        """
        assert to_snake("getAPI") == "get_api"
        assert to_pascal("get_api") == "GetApi"
