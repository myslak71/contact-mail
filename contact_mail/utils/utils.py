from django.core.validators import validate_email
from django.http import Http404

from contact_mail.models import PHONE_CHOICES, EMAIL_CHOICES, Person

PHONE_CHOICES = dict(PHONE_CHOICES)
EMAIL_CHOICES = dict(EMAIL_CHOICES)


def check_email(email):
    try:
        validate_email(email)
        return True
    except:
        return False


def check_if_unsigned_int(number):
    try:
        if int(number) >= 0:
            return number
        raise Exception
    except Exception:
        return None


def contact_exist_get(contact_id):
    contact = Person.objects.filter(pk=contact_id).first()
    if not contact:
        raise Http404
    return contact
