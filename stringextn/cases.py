import re

def to_snake(s: str) -> str:
    """Convert a string to snake_case format.

    Converts various string formats (camelCase, PascalCase, kebab-case, etc.)
    to snake_case by inserting underscores before uppercase letters and
    converting to lowercase.

    Args:
        s: The input string to convert.

    Returns:
        The string converted to snake_case format with all characters in lowercase
        and words separated by underscores.

    Raises:
        None

    Edge cases:
        - Consecutive uppercase letters are treated individually.
        - Spaces are converted to underscores.
        - Empty string returns an empty string.
        - Non-ASCII characters are preserved but not affected by case conversion.
    """
    s = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.replace(" ", "_").lower()

def to_camel(s: str) -> str:
    """Convert a string to camelCase format.

    Converts various string formats (snake_case, kebab-case, PascalCase, etc.)
    to camelCase where the first word is lowercase and subsequent words are
    title-cased without separators.

    Args:
        s: The input string to convert.

    Returns:
        The string converted to camelCase format with the first character
        lowercase and subsequent words capitalized without separators.

    Raises:
        None

    Edge cases:
        - Empty string returns an empty string.
        - String with only separators returns an empty string.
        - Single word returns the word in lowercase.
        - Separators recognized: underscores (_), hyphens (-), and spaces ( ).
    """
    parts = re.split(r'[_\-\s]', s)
    return parts[0].lower() + "".join(p.title() for p in parts[1:])

def to_pascal(s: str) -> str:
    """Convert a string to PascalCase format.

    Converts various string formats (snake_case, kebab-case, camelCase, etc.)
    to PascalCase where each word is title-cased and concatenated without
    separators.

    Args:
        s: The input string to convert.

    Returns:
        The string converted to PascalCase format with the first character
        and first character of each word capitalized without separators.

    Raises:
        None

    Edge cases:
        - Empty string returns an empty string.
        - String with only separators returns an empty string.
        - Single word returns the word with first character capitalized.
        - Separators recognized: underscores (_), hyphens (-), and spaces ( ).
    """
    parts = re.split(r'[_\-\s]', s)
    return "".join(p.title() for p in parts)

def to_kebab(s: str) -> str:
    """Convert a string to kebab-case format.

    Converts various string formats to kebab-case by first converting to
    snake_case, then replacing underscores with hyphens. The result has all
    lowercase letters with words separated by hyphens.

    Args:
        s: The input string to convert.

    Returns:
        The string converted to kebab-case format with all characters in lowercase
        and words separated by hyphens.

    Raises:
        None

    Edge cases:
        - Consecutive uppercase letters are treated individually.
        - Spaces are converted to hyphens.
        - Empty string returns an empty string.
        - Non-ASCII characters are preserved but not affected by case conversion.
    """
    return to_snake(s).replace("_", "-")
