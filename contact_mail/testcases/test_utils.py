from django.test import TestCase
from contact_mail.utils import *


class UtilsTest(TestCase):
    def test_valid_email(self):
        self.assertTrue(check_email('test@mail.com'))

    def test_invalid_email(self):
        self.assertFalse(check_email('123com.pl'))

    def test_valid_number(self):
        self.assertEqual(check_if_unsigned_int(2),2)

    def test_invalid_number(self):
        self.assertEqual(check_if_unsigned_int(-2), None)
