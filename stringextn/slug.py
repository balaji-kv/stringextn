import re
from .clean import clean_text

def slugify(s: str) -> str:
    """Convert a string to a URL-friendly slug format.

    Converts a string into a slug suitable for URLs by cleaning text,
    converting to lowercase, replacing non-alphanumeric characters with hyphens,
    and removing leading/trailing hyphens. Useful for generating URL-safe identifiers
    from titles or descriptions.

    Args:
        s: The input string to convert to a slug.

    Returns:
        A URL-friendly slug with lowercase alphanumeric characters separated
        by hyphens, with no leading or trailing hyphens.

    Raises:
        None

    Edge cases:
        - Empty string returns an empty string.
        - String with only special characters returns an empty string.
        - Consecutive special characters are collapsed into a single hyphen.
        - Leading/trailing hyphens are removed via strip.
        - HTML tags and emoji are removed by clean_text.
        - Unicode characters are normalized before conversion.
        - Spaces are converted to hyphens as part of the non-alphanumeric replacement.
    """
    s = clean_text(s).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')
