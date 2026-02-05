def contains_any(s: str, items) -> bool:
    """Check if a string contains any of the given items.

    Returns True if the string contains at least one of the items in the
    provided iterable. Uses substring matching for string items.

    Args:
        s: The string to search in.
        items: An iterable of items to check for in the string.

    Returns:
        True if the string contains any of the items, False otherwise.

    Raises:
        TypeError: If items is not iterable.

    Edge cases:
        - Empty items iterable returns False.
        - Empty string only returns True if items contains empty string.
        - Case-sensitive substring matching.
        - Matching is performed using the 'in' operator.
    """
    return any(i in s for i in items)

def contains_all(s: str, items) -> bool:
    """Check if a string contains all of the given items.

    Returns True if the string contains every item in the provided iterable.
    Uses substring matching for string items. Order does not matter.

    Args:
        s: The string to search in.
        items: An iterable of items to check for in the string.

    Returns:
        True if the string contains all of the items, False otherwise.

    Raises:
        TypeError: If items is not iterable.

    Edge cases:
        - Empty items iterable returns True.
        - Empty string only returns True if items is empty.
        - Case-sensitive substring matching.
        - Order of items in the string does not matter.
        - Matching is performed using the 'in' operator.
    """
    return all(i in s for i in items)
