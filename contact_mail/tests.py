from django.test import TestCase
from random import randint


# Create your tests here.

class CiTest(TestCase):
    def test_test(self):
        self.assertEqual(1, 1)

    def test_test2(self):
        self.assertEqual(1, 2)
