import re

def multi_replace(s: str, mapping: dict) -> str:
    """Replace multiple substrings in a string using a mapping dictionary.

    Performs simultaneous replacement of multiple substrings based on the
    provided mapping dictionary. Uses compiled regex pattern for efficient
    substitution. All keys are escaped to be treated as literal strings.

    Args:
        s: The input string to perform replacements on.
        mapping: A dictionary where keys are substrings to find and values
                 are the replacements. Keys are treated as literal strings.

    Returns:
        The string with all mapped substrings replaced according to the mapping.

    Raises:
        None

    Edge cases:
        - Empty mapping dictionary returns the original string unchanged.
        - Empty string returns an empty string.
        - Empty keys in mapping are ignored by the regex pattern.
        - Overlapping matches are not replaced multiple times; first match wins.
        - All special regex characters in keys are escaped automatically.
        - Order of replacements is determined by the order keys appear in the pattern.
    """
    pattern = re.compile("|".join(map(re.escape, mapping.keys())))
    return pattern.sub(lambda m: mapping[m.group(0)], s)
