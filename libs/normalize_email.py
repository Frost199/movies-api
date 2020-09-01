"""
Normalise an email module
"""


def normalize_email(email):
    """
    Normalize the email address by lower casing the domain part of it.
    this helper was from the django normalize email function in BaseUserManager
    https://github.com/django/django/blob/master/django/contrib/auth/base_user.py#L19-L31
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = email_name + '@' + domain_part.lower()
    return email
