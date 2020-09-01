import unittest

from libs.normalize_email import normalize_email


class EmailNormalize(unittest.TestCase):
    def test_email_normalize_successful(self):
        email = "test@EMAIL.com"
        normalized_mail = normalize_email(email)
        self.assertEqual(normalized_mail, email.lower())

    def test_email_normalize_return_empty(self):
        email = ""
        normalized_mail = normalize_email(email)
        self.assertEqual(normalized_mail, email.lower())
