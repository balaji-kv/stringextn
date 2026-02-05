def mask_email(email: str) -> str:
    """Mask an email address for privacy by hiding most of the local part.

    Replaces most characters in the local part (before @) with asterisks,
    keeping only the first character visible. The domain part remains unchanged.
    Useful for displaying email addresses in logs or UI without full exposure.

    Args:
        email: A valid email address string containing exactly one @ symbol.

    Returns:
        The masked email with format: [first_char]***@[domain]

    Raises:
        ValueError: If the email does not contain exactly one @ symbol.
        IndexError: If the local part (before @) is empty.

    Edge cases:
        - Single character email local part returns "***@domain".
        - Email with no domain part after @ raises ValueError.
        - Email with multiple @ symbols raises ValueError.
        - No validation is performed on email format beyond @ requirement.
    """
    name, domain = email.split("@")
    return name[0] + "***@" + domain

def mask_phone(phone: str) -> str:
    """Mask a phone number for privacy by hiding all but the last 4 digits.

    Replaces all but the final 4 characters with asterisks. Useful for displaying
    phone numbers in logs or UI while maintaining minimal identifier information.

    Args:
        phone: A phone number string (any length, typically 10+ digits).

    Returns:
        The masked phone number with format: ****[last_4_chars]

    Raises:
        None

    Edge cases:
        - Phone number with 4 or fewer characters returns the original string unchanged.
        - Phone number with 5 characters returns one asterisk plus last 4 chars.
        - No validation is performed on phone format; any string is accepted.
        - Special characters and spaces are preserved (treated as regular characters).
    """
    return "*" * (len(phone) - 4) + phone[-4:]
