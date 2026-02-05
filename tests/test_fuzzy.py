"""Test suite for stringextn.fuzzy similarity function.

Validates similarity scoring across basic cases, edge conditions, and
real-world scenarios using difflib-based ratios.
"""

import pytest
from stringextn.fuzzy import similarity


class TestSimilarityBasic:
    """Basic test cases for similarity function"""

    def test_identical_strings(self):
        """Test similarity of identical strings"""
        # Identical inputs should return 1.0.
        assert similarity("hello", "hello") == 1.0

    def test_completely_different_strings(self):
        """Test similarity of completely different strings"""
        # Completely different strings should return 0.0.
        assert similarity("abc", "xyz") == 0.0

    def test_empty_strings(self):
        """Test similarity of both empty strings"""
        # Two empty strings are identical.
        assert similarity("", "") == 1.0

    def test_empty_vs_non_empty(self):
        """Test similarity of empty vs non-empty string"""
        # Empty vs non-empty should be 0.0.
        assert similarity("", "hello") == 0.0

    def test_non_empty_vs_empty(self):
        """Test similarity of non-empty vs empty string"""
        # Non-empty vs empty should be 0.0.
        assert similarity("hello", "") == 0.0

    def test_case_sensitive(self):
        """Test that similarity is case sensitive"""
        # Case differences reduce similarity below 1.0.
        result = similarity("Hello", "hello")
        assert result < 1.0  # Should not be identical
        assert result > 0.0  # But still similar

    def test_single_character_identical(self):
        """Test single identical character"""
        # Same single character should be 1.0.
        assert similarity("a", "a") == 1.0

    def test_single_character_different(self):
        """Test single different characters"""
        # Different single characters should be 0.0.
        assert similarity("a", "b") == 0.0

    def test_partial_match_beginning(self):
        """Test partial match at beginning"""
        # Prefix overlap should yield a partial score.
        result = similarity("hello", "helloworld")
        assert 0.0 < result < 1.0

    def test_partial_match_end(self):
        """Test partial match at end"""
        # Suffix overlap should yield a partial score.
        result = similarity("world", "helloworld")
        assert 0.0 < result < 1.0

    def test_partial_match_middle(self):
        """Test partial match in middle"""
        # Mid-string overlap should yield a partial score.
        result = similarity("ll", "hello")
        assert 0.0 < result < 1.0


class TestSimilarityCommonPrefixSuffix:
    """Test cases with common prefixes and suffixes"""

    def test_common_prefix_long(self):
        """Test strings with common long prefix"""
        # Long shared prefix should yield high partial similarity.
        result = similarity("hello123", "hello456")
        assert 0.5 < result < 1.0

    def test_common_suffix_long(self):
        """Test strings with common long suffix"""
        # Long shared suffix should yield high partial similarity.
        result = similarity("test123", "best123")
        assert 0.5 < result < 1.0

    def test_common_prefix_and_suffix(self):
        """Test strings with common prefix and suffix"""
        # Shared prefix and suffix should yield a high partial score.
        result = similarity("helloworld", "helloXXXworld")
        assert 0.5 < result < 1.0

    def test_one_word_prefix_another(self):
        """Test where one string is prefix of another"""
        # Prefix relation should yield a partial score.
        result = similarity("car", "carbon")
        assert 0.5 < result < 1.0

    def test_one_word_suffix_another(self):
        """Test where one string is suffix of another"""
        # Suffix relation should yield a partial score.
        result = similarity("ing", "testing")
        assert 0.5 < result < 1.0


class TestSimilaritySubstrings:
    """Test cases with various substrings"""

    def test_exact_substring_match(self):
        """Test exact substring"""
        # Substring containment should yield a partial score.
        result = similarity("hello", "helloxyz")
        assert 0.5 < result < 1.0

    def test_substring_scattered(self):
        """Test substring with scattered characters"""
        # Scattered character overlap should yield a partial score.
        result = similarity("cat", "caught")
        assert 0.3 < result < 1.0

    def test_complete_overlap_different_order(self):
        """Test strings with same characters but different order"""
        # Same characters in different order should still be partially similar.
        result = similarity("abc", "bac")
        # abc and bac should have some similarity
        assert 0.0 < result < 1.0

    def test_anagram_detection(self):
        """Test anagram-like strings"""
        # Anagram-like strings should score higher than unrelated strings.
        result1 = similarity("listen", "silent")
        result2 = similarity("abc", "def")
        # Anagrams should have higher similarity than completely different
        assert result1 > result2


class TestSimilarityWithNumbers:
    """Test cases with numbers"""

    def test_numeric_identical(self):
        """Test identical numeric strings"""
        # Identical numeric strings should be 1.0.
        assert similarity("123", "123") == 1.0

    def test_numeric_different(self):
        """Test different numeric strings"""
        # Different numeric strings should be 0.0.
        result = similarity("123", "456")
        assert result == 0.0

    def test_numeric_partial_match(self):
        """Test partial numeric match"""
        # Shared prefix should yield a partial score.
        result = similarity("12345", "12399")
        assert 0.5 < result < 1.0

    def test_alphanumeric_mix(self):
        """Test alphanumeric mix"""
        # Shared alphabetic prefix should yield a partial score.
        result = similarity("abc123", "abc456")
        assert 0.4 < result < 1.0

    def test_numeric_substring(self):
        """Test numeric substring"""
        # Substring containment should yield a partial score.
        result = similarity("123", "123456")
        assert 0.3 < result < 1.0


class TestSimilarityWithSpecialCharacters:
    """Test cases with special characters"""

    def test_special_characters_identical(self):
        """Test identical special characters"""
        # Identical special characters should be 1.0.
        assert similarity("!@#$", "!@#$") == 1.0

    def test_special_characters_different(self):
        """Test different special characters"""
        # Different special characters should be 0.0.
        result = similarity("!@#", "$%^")
        assert result == 0.0

    def test_mixed_alphanumeric_special(self):
        """Test mix of alphanumeric and special"""
        # Identical mixed strings should be 1.0.
        result = similarity("hello@world", "hello@world")
        assert result == 1.0

    def test_special_partial_match(self):
        """Test special characters partial match"""
        # Partial overlap should yield a partial score.
        result = similarity("!@#", "!@#$%")
        assert 0.5 < result < 1.0

    def test_urls_similar(self):
        """Test similar URLs"""
        # Same domain/path prefix should yield high similarity.
        result = similarity(
            "https://example.com/page1",
            "https://example.com/page2"
        )
        assert 0.7 < result < 1.0

    def test_urls_different_domain(self):
        """Test URLs with different domains"""
        # Different domains reduce similarity but shared path keeps partial score.
        result = similarity(
            "https://example.com/page",
            "https://different.com/page"
        )
        assert 0.5 < result < 1.0

    def test_email_similarity(self):
        """Test email similarity"""
        # Different usernames with same domain should be partially similar.
        result = similarity(
            "user1@example.com",
            "user2@example.com"
        )
        assert 0.7 < result < 1.0


class TestSimilarityWithWhitespace:
    """Test cases with whitespace"""

    def test_spaces_identical(self):
        """Test identical strings with spaces"""
        # Identical whitespace should yield 1.0.
        assert similarity("hello world", "hello world") == 1.0

    def test_spaces_different_count(self):
        """Test different number of spaces"""
        # Extra spaces reduce similarity but stay high.
        result = similarity("hello world", "hello  world")
        assert 0.8 < result < 1.0

    def test_leading_trailing_spaces(self):
        """Test leading/trailing spaces difference"""
        # Leading/trailing spaces reduce similarity but keep partial match.
        result = similarity("hello", " hello ")
        assert 0.5 < result < 1.0

    def test_tabs_vs_spaces(self):
        """Test tabs vs spaces"""
        # Tabs vs spaces should yield a partial match.
        result = similarity("hello\tworld", "hello world")
        assert 0.7 < result < 1.0

    def test_newlines_in_string(self):
        """Test newlines in strings"""
        # Newlines vs spaces should yield a partial match.
        result = similarity("hello\nworld", "hello world")
        assert 0.8 < result < 1.0

    def test_multiple_whitespace_types(self):
        """Test multiple whitespace types"""
        # Mixed whitespace should still yield a partial match.
        result = similarity("hello world", "hello  \t\n  world")
        assert 0.5 < result < 1.0


class TestSimilaritySymmetry:
    """Test symmetry property: similarity(a,b) == similarity(b,a)"""

    def test_symmetry_identical(self):
        """Test symmetry with identical strings"""
        # Similarity should be symmetric for identical inputs.
        assert similarity("hello", "hello") == similarity("hello", "hello")

    def test_symmetry_different(self):
        """Test symmetry with different strings"""
        # Similarity should be symmetric for different inputs.
        assert similarity("hello", "world") == similarity("world", "hello")

    def test_symmetry_partial(self):
        """Test symmetry with partial matches"""
        # Similarity should be symmetric for partial matches.
        assert similarity("abc", "abcdef") == similarity("abcdef", "abc")

    def test_symmetry_single_char(self):
        """Test symmetry with single characters"""
        # Similarity should be symmetric for length differences.
        assert similarity("a", "abc") == similarity("abc", "a")

    def test_symmetry_empty_strings(self):
        """Test symmetry with empty strings"""
        # Similarity should be symmetric when one side is empty.
        assert similarity("", "hello") == similarity("hello", "")

    def test_symmetry_complex_strings(self):
        """Test symmetry with complex strings"""
        # Similarity should be symmetric for complex inputs.
        s1 = "The quick brown fox jumps"
        s2 = "A quick brown dog runs"
        assert similarity(s1, s2) == similarity(s2, s1)


class TestSimilarityRange:
    """Test that similarity values are in valid range [0, 1]"""

    def test_similarity_range_identical(self):
        """Test result is 1.0 for identical strings"""
        # Identical strings should return the upper bound.
        result = similarity("test", "test")
        assert result == 1.0

    def test_similarity_range_completely_different(self):
        """Test result is 0.0 for completely different strings"""
        # Completely different strings should return the lower bound.
        result = similarity("aaa", "bbb")
        assert result == 0.0

    def test_similarity_range_bounds_lower(self):
        """Test result is >= 0"""
        # Score should not go below 0.0.
        result = similarity("xyz", "abc")
        assert result >= 0.0

    def test_similarity_range_bounds_upper(self):
        """Test result is <= 1.0"""
        # Score should not exceed 1.0.
        result = similarity("hello", "world")
        assert result <= 1.0

    def test_similarity_precision(self):
        """Test result is rounded to 3 decimal places"""
        # Rounded output should have at most 3 decimal places.
        result = similarity("hello", "hallo")
        # Should be rounded to 3 decimal places
        assert isinstance(result, float)
        # Check that it has at most 3 decimal places
        str_result = str(result)
        if '.' in str_result:
            decimals = len(str_result.split('.')[1])
            assert decimals <= 3


class TestSimilarityLongStrings:
    """Test cases with long strings"""

    def test_long_identical_strings(self):
        """Test very long identical strings"""
        # Identical long strings should be 1.0.
        long_str = "a" * 1000
        assert similarity(long_str, long_str) == 1.0

    def test_long_completely_different_strings(self):
        """Test very long completely different strings"""
        # Completely different long strings should be 0.0.
        str1 = "a" * 1000
        str2 = "b" * 1000
        assert similarity(str1, str2) == 0.0

    def test_long_strings_partial_match(self):
        """Test long strings with partial match"""
        # Small localized differences should keep score near 0.5.
        str1 = "a" * 500 + "hello" + "b" * 500
        str2 = "a" * 500 + "world" + "b" * 500
        result = similarity(str1, str2)
        # Only 5 chars different out of ~1010, similarity is about 0.499
        assert result >= 0.49

    def test_long_strings_single_char_diff(self):
        """Test long strings differing by single character"""
        # One-character difference should be near 1.0.
        str1 = "a" * 500 + "hello" + "b" * 500
        str2 = "a" * 500 + "hallo" + "b" * 500
        result = similarity(str1, str2)
        assert 0.99 < result < 1.0


class TestSimilarityRealWorldScenarios:
    """Real-world usage scenarios"""

    def test_typo_detection_single_char(self):
        """Test detecting typo with single character difference"""
        # Single-character typo should yield high similarity.
        result = similarity("hello", "hallo")
        assert result >= 0.8

    def test_typo_detection_swapped_chars(self):
        """Test detecting typo with swapped characters"""
        # Transposed characters should still yield high similarity.
        result = similarity("python", "pyhton")
        assert result > 0.8

    def test_spelling_variations_uk_vs_us(self):
        """Test spelling variations"""
        # Spelling variants should yield a partial score.
        result = similarity("colour", "color")
        assert 0.6 < result < 1.0

    def test_product_name_matching(self):
        """Test product name similarity"""
        # Exact product name match should be 1.0.
        result = similarity("iPhone 12 Pro", "iPhone 12 Pro")
        assert result == 1.0

    def test_product_name_similar_models(self):
        """Test similar product models"""
        # Similar model names should yield a high partial score.
        result = similarity("iPhone 12 Pro", "iPhone 13 Pro")
        assert result > 0.8

    def test_business_name_matching(self):
        """Test business name matching"""
        # Related names should yield a partial score.
        result = similarity("Google Inc.", "Google Incorporated")
        assert 0.6 < result < 1.0

    def test_address_similarity(self):
        """Test address similarity"""
        # Small address changes should yield a high similarity.
        result = similarity(
            "123 Main Street, New York, NY 10001",
            "123 Main Street, New York, NY 10002"
        )
        assert result > 0.9

    def test_phone_number_similarity(self):
        """Test phone number similarity"""
        # Single-digit difference should yield a high similarity.
        result = similarity("555-1234", "555-1235")
        assert result > 0.8

    def test_username_matching(self):
        """Test username matching"""
        # Exact username match should be 1.0.
        result = similarity("john_doe", "john_doe")
        assert result == 1.0

    def test_username_similar_typo(self):
        """Test username with typo"""
        # Small typo should yield high similarity.
        result = similarity("john_doe", "john_doo")
        assert result > 0.8

    def test_sentence_similarity(self):
        """Test sentence similarity"""
        # One-word difference should still yield a high similarity.
        result = similarity(
            "The quick brown fox",
            "The quick brown dog"
        )
        assert result > 0.8

    def test_paragraph_similarity(self):
        """Test paragraph similarity"""
        # Minor word changes in long text should keep similarity high.
        text1 = "The quick brown fox jumps over the lazy dog"
        text2 = "The quick brown fox jumps over the sleepy dog"
        result = similarity(text1, text2)
        assert result > 0.9

    def test_search_query_matching(self):
        """Test search query matching"""
        # Exact query match should be 1.0.
        result = similarity("python programming", "python programming")
        assert result == 1.0

    def test_search_query_partial(self):
        """Test search query partial match"""
        # Partial query overlap should yield a partial score.
        result = similarity("python", "python programming")
        assert 0.4 < result < 1.0

    def test_duplicate_content_detection(self):
        """Test duplicate content detection"""
        # Identical content should be 1.0.
        text = "This is a test document"
        result = similarity(text, text)
        assert result == 1.0

    def test_near_duplicate_detection(self):
        """Test near-duplicate detection"""
        # Minor punctuation difference should still be very high.
        text1 = "This is a test document"
        text2 = "This is a test document."
        result = similarity(text1, text2)
        assert result > 0.95


class TestSimilarityEdgeCases:
    """Edge cases and boundary conditions"""

    def test_unicode_characters(self):
        """Test with unicode characters"""
        # Identical Unicode strings should be 1.0.
        result = similarity("café", "café")
        assert result == 1.0

    def test_unicode_different(self):
        """Test different unicode characters"""
        # Minor Unicode differences should yield a partial score.
        result = similarity("café", "cafe")
        assert 0.7 < result < 1.0

    def test_emoji_identical(self):
        """Test identical emojis"""
        # Identical emoji strings should be 1.0.
        result = similarity("😀😀", "😀😀")
        assert result == 1.0

    def test_emoji_different(self):
        """Test different emojis"""
        # Different emoji should not exceed 1.0 and may be low.
        result = similarity("😀", "😎")
        assert result >= 0.0  # Emojis might or might not be similar

    def test_mixed_script_languages(self):
        """Test mixed script languages"""
        # Identical mixed-script strings should be 1.0.
        result = similarity("hello世界", "hello世界")
        assert result == 1.0

    def test_hebrew_characters(self):
        """Test Hebrew characters"""
        # Identical Hebrew strings should be 1.0.
        result = similarity("שלום", "שלום")
        assert result == 1.0

    def test_arabic_characters(self):
        """Test Arabic characters"""
        # Identical Arabic strings should be 1.0.
        result = similarity("السلام", "السلام")
        assert result == 1.0

    def test_repeated_patterns(self):
        """Test repeated patterns"""
        # Identical repeated patterns should be 1.0.
        result = similarity("aaaa", "aaaa")
        assert result == 1.0

    def test_alternating_patterns(self):
        """Test alternating patterns"""
        # Identical alternating patterns should be 1.0.
        result = similarity("abab", "abab")
        assert result == 1.0

    def test_very_short_strings_one_char(self):
        """Test very short strings - one character"""
        # Identical single character should be 1.0.
        assert similarity("a", "a") == 1.0

    def test_very_short_strings_one_char_different(self):
        """Test very short strings - different single character"""
        # Different single characters should be 0.0.
        assert similarity("a", "b") == 0.0


class TestSimilarityConsistency:
    """Test consistency of similarity function"""

    def test_consistency_repeated_calls(self):
        """Test same call returns same result"""
        # Same inputs should yield identical results across calls.
        result1 = similarity("hello", "world")
        result2 = similarity("hello", "world")
        assert result1 == result2

    def test_consistency_multiple_similar_pairs(self):
        """Test consistency across similar pairs"""
        # Similar pluralization should yield similar high scores.
        results = [
            similarity("cat", "cats"),
            similarity("dog", "dogs"),
            similarity("bird", "birds")
        ]
        # All should be similar length differences
        assert all(r > 0.7 for r in results)

    def test_consistency_character_similarity_property(self):
        """Test property: single char difference decreases similarity"""
        # One-character extension should be more similar than unrelated strings.
        base = "hello"
        result1 = similarity(base, base + "x")
        result2 = similarity(base, "xyz")
        # Adding one char to base should be more similar than completely different
        assert result1 > result2


class TestSimilarityBoundaryValues:
    """Test boundary conditions"""

    def test_max_similarity(self):
        """Test maximum possible similarity"""
        # Any string should be perfectly similar to itself.
        for test_str in ["", "a", "hello", "x" * 100]:
            assert similarity(test_str, test_str) == 1.0

    def test_min_similarity_different_lengths(self):
        """Test minimum similarity with different length strings"""
        # Completely different strings should yield 0.0.
        result = similarity("a", "bbbbb")
        assert result == 0.0

    def test_min_similarity_same_length(self):
        """Test minimum similarity with same length strings"""
        # Same-length but different strings should yield 0.0.
        result = similarity("aaaaa", "bbbbb")
        assert result == 0.0

    def test_similar_long_vs_short(self):
        """Test similarity of very different length strings"""
        # Length mismatch should yield a partial score, not 0 or 1.
        result = similarity("a", "aaaaaaaaaa")
        assert 0.0 < result < 1.0

    def test_near_identical_strings(self):
        """Test near-identical strings"""
        # Single-character difference should keep similarity high.
        str1 = "abcdefghij"
        str2 = "abcdefghix"
        result = similarity(str1, str2)
        assert result >= 0.9


class TestSimilarityCommonCases:
    """Common use case scenarios"""

    def test_exact_match_expected(self):
        """Test exact match is 1.0"""
        # Exact match should be 1.0.
        assert similarity("exact", "exact") == 1.0

    def test_no_match_expected(self):
        """Test no match has low similarity"""
        # Unrelated strings should yield a low score.
        result = similarity("hello", "world")
        assert result < 0.5

    def test_percentage_conversion(self):
        """Test converting result to percentage"""
        # Percentage should remain within 0 to 100.
        result = similarity("hello", "hallo")
        percentage = result * 100
        assert 0 <= percentage <= 100

    def test_threshold_based_matching(self):
        """Test threshold-based similarity matching"""
        # Threshold should accept similar strings and reject dissimilar ones.
        threshold = 0.75
        pairs = [
            ("hello", "hallo"),
            ("python", "pyhton"),
            ("test", "xyz")
        ]
        similarities = [similarity(a, b) for a, b in pairs]
        # First two should exceed threshold
        assert similarities[0] >= threshold
        assert similarities[1] >= threshold
        assert similarities[2] < threshold

    def test_ranking_by_similarity(self):
        """Test ranking candidates by similarity"""
        # Best match should rank first by highest similarity.
        reference = "python"
        candidates = ["python", "pyton", "java", "pytho", "c++"]
        similarities = [(c, similarity(reference, c)) for c in candidates]
        # Sort by similarity descending
        sorted_sims = sorted(similarities, key=lambda x: x[1], reverse=True)
        # Best match should be first
        assert sorted_sims[0][0] == "python"
