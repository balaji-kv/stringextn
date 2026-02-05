# stringextn

A pragmatic, zero-dependency Python library for practical string manipulation and text cleaning. `stringextn` provides battle-tested utilities for case conversion, HTML/emoji removal, substring matching, fuzzy comparison, security masking, URL slug generation, and multi-string replacement—all designed with real-world edge cases in mind.

## Installation

Install via pip:

```bash
pip install stringextn
```

Requires Python 3.8 or higher. No external dependencies.

## Quick Start

```python
from stringextn import (
    to_snake, to_camel, to_pascal, to_kebab,
    clean_text, remove_html, remove_emoji,
    contains_any, contains_all,
    similarity,
    multi_replace,
    mask_email, mask_phone,
    slugify
)

# Case conversion
to_snake("myVariableName")        # "my_variable_name"
to_camel("my_variable_name")      # "myVariableName"
to_pascal("my-variable-name")     # "MyVariableName"
to_kebab("myVariableName")        # "my-variable-name"

# Text cleaning
clean_text("<p>Hello &amp; goodbye!</p>")  # "Hello & goodbye!"
remove_html("<div>Content</div>")          # "Content"
remove_emoji("Hello 👋 World 🌍")         # "Hello  World "

# Substring matching
contains_any("hello world", ["world", "foo"])   # True
contains_all("hello world", ["hello", "world"]) # True

# Fuzzy string matching
similarity("kitten", "sitting")  # 0.571

# Multi-replace
multi_replace("abc abc abc", {"a": "X", "b": "Y"})  # "XYc XYc XYc"

# Privacy masking
mask_email("user@example.com")  # "u***@example.com"
mask_phone("5551234567")        # "****1234"

# URL-safe slugs
slugify("Hello, World! ✨")  # "hello-world"
```

## Features

### Case Conversion
- **`to_snake(s)`** – Converts to snake_case
- **`to_camel(s)`** – Converts to camelCase
- **`to_pascal(s)`** – Converts to PascalCase
- **`to_kebab(s)`** – Converts to kebab-case

Supports mixed input formats (camelCase, PascalCase, kebab-case, snake_case, space-separated).

### Text Cleaning
- **`clean_text(s)`** – Comprehensive cleaning pipeline: HTML entity unescaping, tag removal, emoji removal, Unicode normalization, and whitespace normalization
- **`remove_html(s)`** – Strips HTML/XML tags
- **`remove_emoji(s)`** – Removes emoji characters
- **`normalize_spaces(s)`** – Collapses whitespace and trims
- **`normalize_unicode(s)`** – Applies NFKD normalization for consistent character representation

### Substring Operations
- **`contains_any(s, items)`** – Returns True if string contains any item
- **`contains_all(s, items)`** – Returns True if string contains all items

Case-sensitive substring matching using Python's `in` operator.

### Fuzzy Matching
- **`similarity(a, b)`** – Returns similarity score (0.0–1.0) using difflib's SequenceMatcher
  - 1.0 = identical strings
  - 0.0 = no similarity
  - Rounded to 3 decimal places

### String Replacement
- **`multi_replace(s, mapping)`** – Performs simultaneous multi-string replacement
  - All keys are treated as literal strings (regex special chars auto-escaped)
  - Non-cascading: each substring is replaced exactly once

### Security & Privacy
- **`mask_email(email)`** – Hides all but first character of email local part
  - Format: `u***@example.com`
  - Raises `ValueError` if email doesn't contain exactly one `@`
- **`mask_phone(phone)`** – Hides all but last 4 digits
  - Format: `****1234`

### URL Slugs
- **`slugify(s)`** – Generates URL-safe slugs
  - Cleans text, lowercases, replaces non-alphanumeric with hyphens
  - Strips leading/trailing hyphens
  - Example: `"Hello, World! ✨"` → `"hello-world"`

## Performance & Behavior Notes

### Unicode Handling
- **NFKD Normalization**: The `clean_text()` and `slugify()` functions apply NFKD (Compatibility Decomposition) normalization, which:
  - Decomposes accented characters (é → e + ´)
  - Applies compatibility mappings (ﬁ → fi)
  - Ensures consistent character representation across different input encodings
- Emoji removal uses Unicode ranges and handles most emoticons and symbols; complex emoji sequences (skin tones, zero-width-joiner) may not be fully removed
- Non-ASCII characters in `to_snake()` and `to_camel()` are preserved but not affected by case conversion

### Edge Cases
- **Empty strings**: Most functions return empty strings; `contains_all("", [])` returns True (vacuous truth)
- **Whitespace**: Leading/trailing whitespace is preserved in case conversion; use `normalize_spaces()` first if needed
- **Consecutive separators**: `multi_replace()` and `slugify()` handle consecutive delimiters correctly (collapsed in slugs, replaced individually in multi_replace)
- **Special regex characters**: `multi_replace()` automatically escapes all regex special characters in mapping keys
- **Email masking**: No format validation; only checks for single `@` symbol
- **Phone masking**: Works with any string; no validation of format

### Performance
- All functions use compiled regular expressions or built-in operations for efficiency
- No external dependencies; pure Python implementation
- Suitable for high-volume text processing in APIs and data pipelines

## Testing

Run the test suite with pytest:

```bash
pytest tests/
```

## License

MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome. Please ensure all tests pass and add tests for new functionality.

---

**Package**: stringextn v1.0.0  
**GitHub**: [stringextn](https://github.com/balaji-kv/stringextn)
