import unittest

from libs.email import normalize_email, is_email_valid


class Email(unittest.TestCase):

    def test_is_email_valid_successful(self):
        self.assertTrue(is_email_valid("email@example.com"))
        self.assertTrue(is_email_valid("Bob_O'Reilly+tag@example.com"))
        self.assertTrue(is_email_valid("Bob_O'Reilly+tag@mail.co.uk"))
        self.assertTrue(is_email_valid("example.mail.1234@mail.co.uk"))

    def test_is_email_not_valid(self):
        self.assertFalse(is_email_valid(""))
        self.assertFalse(is_email_valid("email"))
        self.assertFalse(is_email_valid("@mail.com"))
        self.assertFalse(is_email_valid("example@mail.com,"))

    def test_email_normalize_successful(self):
        email = "test@EMAIL.com"
        normalized_mail = normalize_email(email)
        self.assertEqual(normalized_mail, email.lower())

    def test_email_normalize_return_empty(self):
        email = ""
        normalized_mail = normalize_email(email)
        self.assertEqual(normalized_mail, email.lower())
