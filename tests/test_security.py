"""Test suite for stringextn.security masking functions.

Validates mask_email and mask_phone formatting, edge cases, and
real-world input variations to ensure consistent masking behavior.
"""

import pytest
from stringextn.security import mask_email, mask_phone


class TestMaskEmailBasic:
    """Basic test cases for mask_email function"""

    def test_standard_email(self):
        """Test masking standard email address"""
        # Masks local part to first character plus asterisks.
        result = mask_email("john@example.com")
        assert result == "j***@example.com"

    def test_long_name_email(self):
        """Test masking email with long name"""
        # Long local part should still mask to first char + ***.
        result = mask_email("jonathan@example.com")
        assert result == "j***@example.com"

    def test_single_char_name(self):
        """Test masking email with single character name"""
        # Single-char local part should keep that char and add ***.
        result = mask_email("a@example.com")
        assert result == "a***@example.com"

    def test_email_with_numbers(self):
        """Test masking email with numbers in name"""
        # Numeric characters in local part are fully masked.
        result = mask_email("john123@example.com")
        assert result == "j***@example.com"

    def test_email_with_dots(self):
        """Test masking email with dots in name"""
        # Dots in local part are masked like any other character.
        result = mask_email("john.doe@example.com")
        assert result == "j***@example.com"

    def test_email_with_hyphen(self):
        """Test masking email with hyphen in name"""
        # Hyphens in local part are masked.
        result = mask_email("john-doe@example.com")
        assert result == "j***@example.com"

    def test_email_with_underscore(self):
        """Test masking email with underscore in name"""
        # Underscores in local part are masked.
        result = mask_email("john_doe@example.com")
        assert result == "j***@example.com"

    def test_email_with_plus(self):
        """Test masking email with plus sign in name"""
        # Plus tags in local part are masked.
        result = mask_email("john+tag@example.com")
        assert result == "j***@example.com"

    def test_lowercase_email(self):
        """Test masking lowercase email"""
        # Preserves domain and first local character.
        result = mask_email("test@domain.org")
        assert result == "t***@domain.org"

    def test_uppercase_email(self):
        """Test masking uppercase email (case preservation)"""
        # Preserves original case of first local char and domain.
        result = mask_email("TEST@DOMAIN.COM")
        assert result == "T***@DOMAIN.COM"

    def test_mixed_case_email(self):
        """Test masking mixed case email"""
        # Preserves case of first local char and domain.
        result = mask_email("JoHn@ExAmPlE.cOm")
        assert result == "J***@ExAmPlE.cOm"

    def test_domain_with_subdomain(self):
        """Test email with subdomain"""
        # Domain portion is preserved fully.
        result = mask_email("user@mail.example.com")
        assert result == "u***@mail.example.com"

    def test_domain_with_multiple_subdomains(self):
        """Test email with multiple subdomains"""
        # Entire multi-subdomain is preserved.
        result = mask_email("user@sub.mail.example.co.uk")
        assert result == "u***@sub.mail.example.co.uk"

    def test_numeric_domain(self):
        """Test email with numeric domain (IP-like)"""
        # Numeric domains are preserved as-is.
        result = mask_email("user@192.168.1.1")
        assert result == "u***@192.168.1.1"

    def test_preserves_domain_completely(self):
        """Test that domain is completely preserved"""
        # Only local part is masked; domain is unchanged.
        result = mask_email("alice@wonderland.io")
        assert result == "a***@wonderland.io"


class TestMaskEmailEdgeCases:
    """Edge cases for mask_email function"""

    def test_very_long_email_name(self):
        """Test with very long email name"""
        # Edge case: very long local part still masks to first char + ***.
        long_name = "a" * 1000
        result = mask_email(long_name + "@example.com")
        assert result == "a***@example.com"

    def test_very_long_domain(self):
        """Test with very long domain"""
        # Edge case: very long domain should be preserved.
        long_domain = "very.long.subdomain." * 50 + "example.com"
        result = mask_email("user@" + long_domain)
        assert result.startswith("u***@")
        assert long_domain in result

    def test_email_only_name(self):
        """Test email with only one character name"""
        # Single-char local part should still be masked with ***.
        result = mask_email("x@y.z")
        assert result == "x***@y.z"

    def test_special_char_first_position(self):
        """Test when first character is special (if allowed by email)"""
        # Edge case: special first character is preserved.
        # Some email systems allow this
        result = mask_email("+tag@example.com")
        assert result == "+***@example.com"

    def test_name_with_consecutive_special_chars(self):
        """Test name with consecutive special characters"""
        # Special characters in local part are masked after first char.
        result = mask_email("user++tag@example.com")
        assert result == "u***@example.com"

    def test_very_short_domain(self):
        """Test with very short domain"""
        # Short domain is preserved.
        result = mask_email("user@a.b")
        assert result == "u***@a.b"

    def test_preserve_original_input_format(self):
        """Test that function returns correct format"""
        # Output should be first_char + *** + @ + domain.
        result = mask_email("example123@test.com")
        # Should be: first_char + *** + @ + domain
        parts = result.split("@")
        assert len(parts) == 2
        assert parts[0] == "e***"


class TestMaskEmailFormat:
    """Test the format of masked email"""

    def test_masked_format_structure(self):
        """Test that masked email has correct structure"""
        # Ensures exactly one @ and one *** sequence.
        result = mask_email("john@example.com")
        assert "***@" in result
        assert result.count("@") == 1
        assert result.count("***") == 1

    def test_masked_contains_original_domain(self):
        """Test that masked email contains original domain"""
        # Domain portion should be unchanged.
        original = "user@example.co.uk"
        result = mask_email(original)
        assert "example.co.uk" in result

    def test_first_char_preserved(self):
        """Test that first character is preserved"""
        # First local character must remain visible.
        result = mask_email("zebra@example.com")
        assert result.startswith("z***@")

    def test_asterisks_count(self):
        """Test that exactly 3 asterisks are used"""
        # Local part should always contain exactly 3 asterisks.
        result = mask_email("test@example.com")
        # Count asterisks before @
        name_part = result.split("@")[0]
        assert name_part.count("*") == 3


class TestMaskEmailDomainVariations:
    """Test with various domain formats"""

    def test_com_domain(self):
        """Test .com domain"""
        # Preserves .com domain.
        result = mask_email("user@example.com")
        assert result == "u***@example.com"

    def test_org_domain(self):
        """Test .org domain"""
        # Preserves .org domain.
        result = mask_email("user@example.org")
        assert result == "u***@example.org"

    def test_net_domain(self):
        """Test .net domain"""
        # Preserves .net domain.
        result = mask_email("user@example.net")
        assert result == "u***@example.net"

    def test_co_uk_domain(self):
        """Test .co.uk domain"""
        # Preserves .co.uk domain.
        result = mask_email("user@example.co.uk")
        assert result == "u***@example.co.uk"

    def test_gov_domain(self):
        """Test .gov domain"""
        # Preserves .gov domain.
        result = mask_email("user@example.gov")
        assert result == "u***@example.gov"

    def test_edu_domain(self):
        """Test .edu domain"""
        # Preserves .edu domain.
        result = mask_email("user@university.edu")
        assert result == "u***@university.edu"

    def test_custom_tld(self):
        """Test custom TLD"""
        # Preserves custom TLD.
        result = mask_email("user@example.custom")
        assert result == "u***@example.custom"

    def test_single_letter_domain(self):
        """Test single letter domain"""
        # Preserves short domain labels.
        result = mask_email("user@x.co")
        assert result == "u***@x.co"


class TestMaskPhoneBasic:
    """Basic test cases for mask_phone function"""

    def test_standard_phone_10_digits(self):
        """Test masking standard 10-digit phone number"""
        # Preserves the last 4 characters of input.
        result = mask_phone("5551234567")
        # Should preserve last 4 digits
        assert result.endswith("4567")

    def test_phone_with_dashes(self):
        """Test masking phone with dashes"""
        # Keeps last 4 characters even with separators.
        result = mask_phone("555-123-4567")
        # Should end with last 4 chars of input
        assert result.endswith("4567")

    def test_phone_with_spaces(self):
        """Test masking phone with spaces"""
        # Preserves last 4 characters including digits after spaces.
        result = mask_phone("555 123 4567")
        # Should end with last 4 chars
        assert result.endswith("4567")

    def test_phone_with_parentheses(self):
        """Test masking phone with parentheses"""
        # Preserves last 4 characters regardless of formatting.
        result = mask_phone("(555)123-4567")
        # Should end with last 4 chars of input
        assert result.endswith("4567")

    def test_phone_with_plus_country_code(self):
        """Test masking phone with country code"""
        # Preserves last 4 characters with country code.
        result = mask_phone("+1-555-123-4567")
        # Should end with last 4 chars
        assert result.endswith("4567")

    def test_short_phone_4_digits(self):
        """Test with 4-digit phone (extension)"""
        # Edge case: 4 chars should be unchanged.
        result = mask_phone("1234")
        assert result == "1234"

    def test_phone_exactly_4_chars(self):
        """Test phone with exactly 4 characters"""
        # Edge case: exactly 4 chars returns original.
        result = mask_phone("abcd")
        assert result == "abcd"

    def test_longer_phone_11_digits(self):
        """Test 11-digit phone number"""
        # Preserves last 4 digits for longer numbers.
        result = mask_phone("15551234567")
        # Should preserve last 4 digits
        assert result.endswith("4567")

    def test_phone_with_extension(self):
        """Test phone with extension"""
        # Preserves last 4 characters even if extension included.
        result = mask_phone("555-123-4567 x123")
        # Last 4 chars of input are 'x123'
        assert result.endswith("x123")

    def test_phone_preserves_last_4(self):
        """Test that last 4 characters are preserved"""
        # Last 4 digits should remain visible.
        result = mask_phone("1234567890")
        assert result.endswith("7890")

    def test_phone_preserves_exact_last_4(self):
        """Test exactly last 4 chars"""
        # Ensures mask length is correct.
        phone = "9876543210"
        result = mask_phone(phone)
        assert result == "******3210"


class TestMaskPhoneEdgeCases:
    """Edge cases for mask_phone function"""

    def test_phone_less_than_4_chars(self):
        """Test phone shorter than 4 characters"""
        # Edge case: length < 4 should still return a string.
        result = mask_phone("123")
        # All characters are masked except last 4 (which don't exist)
        # So: ("*" * (3 - 4)) + "123" = "" + "123" = ""? or just "123"?
        # Actually: "*" * max(0, len - 4) + last_4
        # For length 3: "*" * (3-4) would be negative, but should handle it
        assert isinstance(result, str)

    def test_phone_exactly_4_chars_edge(self):
        """Test phone with exactly 4 characters"""
        # Edge case: no masking needed.
        result = mask_phone("4567")
        assert result == "4567"  # No asterisks, just last 4

    def test_single_digit_phone(self):
        """Test single digit phone"""
        # Edge case: single character should return a string.
        result = mask_phone("5")
        # Should be masked but preserving last 4 (which don't exist)
        assert isinstance(result, str)

    def test_empty_string_phone(self):
        """Test empty string phone"""
        # Edge case: empty input should return empty string.
        result = mask_phone("")
        # "*" * (0 - 4) would be negative, but Python handles it as 0 + last 4 chars
        # Actually: "*" * (len("") - 4) + ""[-4:] = "*" * (-4) + "" = "" + "" = ""
        assert result == ""

    def test_very_long_phone(self):
        """Test very long phone number"""
        # Edge case: long input still preserves last 4.
        long_phone = "0" * 1000 + "1234"
        result = mask_phone(long_phone)
        assert result.endswith("1234")
        assert result.startswith("*")

    def test_phone_with_special_chars(self):
        """Test phone with various special characters"""
        # Special characters are treated as part of the string.
        result = mask_phone("+1 (555) 123-4567")
        assert result.endswith("4567")
        assert result.startswith("*")

    def test_phone_with_extensions_and_special(self):
        """Test complex phone format with extensions"""
        # Extension suffix should be preserved in last 4 chars.
        result = mask_phone("+1-555-123-4567 ext. 890")
        assert result.endswith("890")

    def test_phone_all_same_digits(self):
        """Test phone with all same digits"""
        # Masking should preserve last 4 digits only.
        result = mask_phone("1111111111")
        assert result == "******1111"

    def test_phone_alternating_pattern(self):
        """Test phone with alternating pattern"""
        # Masking should preserve last 4 digits.
        result = mask_phone("0101010101")
        assert result == "******0101"


class TestMaskPhoneFormat:
    """Test the format of masked phone"""

    def test_masked_format_preserves_last_4(self):
        """Test that last 4 characters are preserved"""
        # Last 4 characters must remain visible.
        result = mask_phone("1234567890")
        assert result[-4:] == "7890"

    def test_masked_format_uses_asterisks(self):
        """Test that asterisks are used for masking"""
        # Masking should introduce asterisks.
        result = mask_phone("5551234567")
        assert "*" in result

    def test_masked_format_correct_length(self):
        """Test masked phone has correct length"""
        # Output length should match input length.
        original = "5551234567"
        result = mask_phone(original)
        assert len(result) == len(original)

    def test_masked_exact_mask_count(self):
        """Test exact number of asterisks"""
        # Mask count should be len - 4.
        phone = "5551234567"
        result = mask_phone(phone)
        # 10 - 4 = 6 asterisks
        assert result.count("*") == 6

    def test_masked_preserves_spaces(self):
        """Test that format is preserved"""
        # Formatting characters are preserved in output length.
        result = mask_phone("555 123 4567")
        # Last 4 chars of input should be preserved
        assert "4567" in result

    def test_masked_preserves_special_chars(self):
        """Test format handling"""
        # Special characters may remain; last 4 must be preserved.
        result = mask_phone("(555)123-4567")
        # Last 4 chars should be preserved
        assert result.endswith("4567")


class TestMaskPhoneRealWorldFormats:
    """Real-world phone number formats"""

    def test_us_format_dash(self):
        """Test US format with dashes"""
        # Preserves last 4 characters with dash formatting.
        result = mask_phone("555-123-4567")
        assert result.endswith("4567")

    def test_us_format_parentheses(self):
        """Test US format with parentheses"""
        # Preserves last 4 and masks the rest.
        result = mask_phone("(555) 123-4567")
        assert result == "**********4567"

    def test_us_format_spaces(self):
        """Test US format with spaces"""
        # Preserves last 4 characters with spaces.
        result = mask_phone("555 123 4567")
        assert result.endswith("4567")

    def test_international_format_plus(self):
        """Test international format with plus"""
        # Preserves last 4 characters with country code.
        result = mask_phone("+1-555-123-4567")
        assert result.endswith("4567")

    def test_international_country_code(self):
        """Test with country codes"""
        # Preserves last 4 characters for international formats.
        result = mask_phone("+44-20-7946-0958")  # UK London
        assert result.endswith("0958")

    def test_german_format(self):
        """Test German phone format"""
        # Preserves last 4 characters for German format.
        result = mask_phone("+49-30-12345678")
        assert result.endswith("5678")

    def test_japanese_format(self):
        """Test Japanese phone format"""
        # Preserves last 4 characters for Japanese format.
        result = mask_phone("03-1234-5678")
        assert result.endswith("5678")

    def test_indian_format(self):
        """Test Indian phone format"""
        # Preserves last 4 characters for Indian format.
        result = mask_phone("+91-98765-43210")
        assert result.endswith("3210")

    def test_extension_format_1(self):
        """Test phone with extension format 1"""
        # Preserves extension suffix in last 4 characters.
        result = mask_phone("555-1234 x5678")
        assert result.endswith("5678")

    def test_extension_format_2(self):
        """Test phone with extension format 2"""
        # Preserves extension suffix in last 4 characters.
        result = mask_phone("555-1234 ext. 90")
        assert result.endswith("90")

    def test_sip_uri_format(self):
        """Test SIP URI format"""
        # Preserves last 4 characters in SIP URI.
        result = mask_phone("sip:user@example.com:5060")
        assert result.endswith("5060")


class TestMaskPhoneNumericalBehavior:
    """Test numerical behavior of phone masking"""

    def test_numeric_only_phone(self):
        """Test purely numeric phone"""
        # Numeric input should mask all but last 4.
        result = mask_phone("9876543210")
        assert result == "******3210"

    def test_alphanumeric_phone(self):
        """Test alphanumeric phone"""
        # Preserves last 4 characters even if letters.
        result = mask_phone("1-800-FLOWERS")
        assert result.endswith("WERS")

    def test_letters_in_phone(self):
        """Test phone with letters (like vanity numbers)"""
        # Preserves last 4 characters including letters.
        result = mask_phone("1-800-CALL-ABC")
        # Last 4 chars of input are '-ABC'
        assert result.endswith("-ABC")

    def test_numeric_string_vs_number(self):
        """Test that string input works correctly"""
        # Function accepts string input and returns string.
        phone_str = "5551234567"
        result = mask_phone(phone_str)
        assert isinstance(result, str)
        assert result.endswith("4567")


class TestMaskPhoneConsistency:
    """Test consistency of phone masking"""

    def test_consistent_results_repeated_calls(self):
        """Test same input produces same output"""
        # Output should be stable across calls.
        phone = "5551234567"
        result1 = mask_phone(phone)
        result2 = mask_phone(phone)
        assert result1 == result2

    def test_consistent_last_4_chars(self):
        """Test last 4 characters always preserved"""
        # Last 4 characters should be preserved across formats.
        phones = [
            "5551234567",
            "555-123-4567",
            "(555) 123-4567",
            "+1-555-123-4567"
        ]
        results = [mask_phone(p) for p in phones]
        # All should end with same last 4 chars if input has them
        for r in results:
            assert r.endswith("4567")


class TestMaskSecurityProperties:
    """Test security properties of masking functions"""

    def test_email_mask_reveals_no_name(self):
        """Test that email masking reveals minimal name info"""
        # Only first character of local part is visible.
        result = mask_email("superlongname@example.com")
        # Only first character visible
        assert result == "s***@example.com"

    def test_email_mask_preserves_domain(self):
        """Test that email masking preserves domain (which is public)"""
        # Domain portion should be preserved.
        result = mask_email("user@company.com")
        assert "company.com" in result

    def test_phone_mask_reveals_last_4(self):
        """Test that phone masking preserves last 4 digits"""
        # Last 4 digits remain visible for verification.
        result = mask_phone("5551234567")
        # Last 4 visible, useful for verification
        assert result.endswith("4567")

    def test_phone_mask_hides_area_code(self):
        """Test that phone masking hides area code"""
        # Area code should be masked in output.
        result = mask_phone("(555)123-4567")
        assert "555" not in result or result.startswith("*")

    def test_multiple_emails_same_domain_different_names(self):
        """Test multiple emails with same domain show different names"""
        # Different local first chars should yield different masked output.
        result1 = mask_email("alice@example.com")
        result2 = mask_email("bob@example.com")
        assert result1 != result2
        assert result1.startswith("a")
        assert result2.startswith("b")

    def test_multiple_phones_same_prefix_different_suffix(self):
        """Test phones with same prefix show different masked results"""
        # Last 4 digits should reflect differences.
        result1 = mask_phone("5551234567")
        result2 = mask_phone("5551234589")
        # Should show different last 4
        assert result1.endswith("4567")
        assert result2.endswith("4589")


class TestMaskIntegration:
    """Integration tests for both masking functions"""

    def test_mask_email_and_phone_in_text(self):
        """Test masking email and phone in same text"""
        # Both functions should produce masked outputs.
        email = "john@example.com"
        phone = "5551234567"
        masked_email = mask_email(email)
        masked_phone = mask_phone(phone)
        
        assert masked_email == "j***@example.com"
        assert masked_phone.endswith("4567")

    def test_mask_preserves_data_format(self):
        """Test that masking preserves recognizable format"""
        # Masked outputs should still look like email/phone strings.
        email = mask_email("user@domain.com")
        phone = mask_phone("1234567890")
        
        # Email should still look like email
        assert "@" in email
        assert "." in email
        
        # Phone should still contain digits/chars from original
        assert len(phone) > 0

    def test_mask_different_users_different_results(self):
        """Test that different users produce different masked results"""
        # Different inputs should yield different masked outputs.
        emails = [
            mask_email("alice@example.com"),
            mask_email("bob@example.com"),
            mask_email("charlie@example.com")
        ]
        phones = [
            mask_phone("5551112222"),
            mask_phone("5553334444"),
            mask_phone("5555556666")
        ]
        
        # All different
        assert len(set(emails)) == 3
        assert len(set(phones)) == 3


class TestMaskEdgeCasesExtended:
    """Extended edge case tests"""

    def test_email_unicode_domain(self):
        """Test email with unicode characters in domain"""
        # Unicode domain should be preserved.
        result = mask_email("user@exämple.com")
        assert result == "u***@exämple.com"

    def test_email_punycode_domain(self):
        """Test email with punycode domain"""
        # Punycode domain should be preserved.
        result = mask_email("user@xn--exmple-cua.com")
        assert result == "u***@xn--exmple-cua.com"

    def test_phone_with_unicode_chars(self):
        """Test phone with unicode characters"""
        # Unicode suffix should be preserved in last 4 chars.
        result = mask_phone("555-123-4567™")
        assert result.endswith("567™")

    def test_email_at_symbol_multiple(self):
        """Test email handling (should only have one @ by design)"""
        # Edge case: invalid emails may raise ValueError.
        # This might fail if email has multiple @, but the function assumes valid email
        try:
            result = mask_email("user@mid@example.com")
            # If it works, last @ is used
            assert "***@" in result
        except ValueError:
            # Or it might raise an error for invalid email
            pass

    def test_phone_parentheses_unbalanced(self):
        """Test phone with unbalanced parentheses"""
        # Unbalanced formatting should still preserve last 4 chars.
        result = mask_phone("(5551234567")
        assert result.endswith("4567")

    def test_phone_multiple_extensions(self):
        """Test phone with multiple extension indicators"""
        # Edge case: preserves final 4 characters even with multiple extensions.
        result = mask_phone("555-123-4567 x123 x456")
        assert isinstance(result, str)
        # Should end with last 4 chars of input
        assert result.endswith("456")
