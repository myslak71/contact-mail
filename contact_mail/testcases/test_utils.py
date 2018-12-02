from django.test import TestCase

from contact_mail.utils import *


class UtilsTest(TestCase):
    def tearDown(self):
        Person.objects.all().delete()

    def test_valid_email(self):
        self.assertTrue(check_email('test@mail.com'))

    def test_invalid_email(self):
        self.assertFalse(check_email('123com.pl'))

    def test_valid_number(self):
        self.assertEqual(check_if_unsigned_int(2), 2)

    def test_invalid_number(self):
        self.assertEqual(check_if_unsigned_int(-2), None)

    def test_contact_exist(self):
        Person.objects.create(name='Name', surname='Surname', description='Description').save()
        c = contact_exist_get(1)
        self.assertEqual(c.name, 'Name')
        self.assertEqual(c.surname, 'Surname')
        self.assertEqual(c.description, 'Description')

    def test_contact_not_exist(self):
        with self.assertRaises(Http404):
            contact_exist_get(1)
