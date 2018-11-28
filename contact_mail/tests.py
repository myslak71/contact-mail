from django.test import TestCase
from random import randint
# Create your tests here.

PHONE_CHOICES = (
    (0, 'mobile'),
    (1, 'company'),
    (2, 'home'),
)

PHONE_CHOICES = dict(PHONE_CHOICES)

print(PHONE_CHOICES)
print('2' in str(PHONE_CHOICES))

from django.core.validators import validate_email

print(validate_email('kornel@gmail.com'))

input('Wciśnij')
print(randint(1, 4))