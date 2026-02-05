from difflib import SequenceMatcher

def similarity(a: str, b: str) -> float:
    """Calculate the similarity ratio between two strings.

    Computes a similarity score between 0 and 1 using SequenceMatcher from
    the difflib module. The ratio represents the proportion of matching
    characters and sequences. Result is rounded to 3 decimal places.

    Args:
        a: The first string to compare.
        b: The second string to compare.

    Returns:
        A float between 0 and 1 representing the similarity ratio, rounded to
        3 decimal places. 1.0 indicates identical strings, 0.0 indicates no similarity.

    Raises:
        None

    Edge cases:
        - Empty strings: two empty strings return 1.0 (identical).
        - One empty string: similarity depends on the other string's length.
        - Case-sensitive comparison: 'abc' and 'ABC' are treated as different.
        - Whitespace is significant: leading/trailing spaces affect the result.
        - The function uses longest contiguous matching subsequences for comparison.
    """
    return round(SequenceMatcher(None, a, b).ratio(), 3)
