"""
Normalise an email module
"""
import re


def is_email_valid(email: str) -> bool:
    """
    check if an email is a valid type
    Args:
        email: Email string to check

    Returns:
        bool
    """
    if re.match("[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email):
        return True
    else:
        return False


def normalize_email(email):
    """
    Normalize the email address by lower casing the domain part of it.
    this helper was from the django normalize email function in BaseUserManager
    https://github.com/django/django/blob/master/django/contrib/auth/base_user.py#L19-L31
    """
    email = email or ''
    if is_email_valid(email):
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email
    return email
