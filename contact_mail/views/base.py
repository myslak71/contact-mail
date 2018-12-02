from abc import ABC

from django.contrib import messages
from django.views import View

from contact_mail.models import Group
from contact_mail.utils import PHONE_CHOICES, check_if_unsigned_int, EMAIL_CHOICES, check_email


class BaseView(View, ABC):
    FORM_FIELDS = ()

    def _get_form_field_values(self, request):
        '''
        Get field value from request and set it as instance attribute for every field in FORM_FIELDS

        :param request: rest request data
        :return:
        '''
        for field in self.FORM_FIELDS:
            if field == 'contacts':
                setattr(self, 'contacts', request.POST.getlist('contacts'))
                continue
            setattr(self, field, request.POST.get(field).strip())

    def _validate_form(self, request, *args, group_id=None):
        valid = True

        if 'name' in args and 'surname' in args:
            if not self.name or not self.surname:
                messages.add_message(request, messages.ERROR, 'Name and surname are required')
                valid = False

        if 'city' in args and 'street' in args and 'building_number' in args and 'apartment_number' in args:
            if not self.city or not self.street or not self.building_number or not self.apartment_number:
                messages.add_message(request, messages.ERROR, 'Inappropriate address')
                valid = False

        if 'number' in args and 'phone_type' in args:
            if self.phone_type not in str(PHONE_CHOICES):
                messages.add_message(request, messages.ERROR, 'Inappropriate phone type value')
                valid = False

            if not self.number or not check_if_unsigned_int(self.number):
                messages.add_message(request, messages.ERROR, 'Inappropriate phone number')
                valid = False

        if 'email_type' in args and 'email_address' in args:
            if self.email_type not in str(EMAIL_CHOICES):
                messages.add_message(request, messages.ERROR, 'Inappropriate email type value')
                valid = False

            if not self.email_address:
                messages.add_message(request, messages.ERROR, 'Inappropriate email address')
                valid = False

            if not check_email(self.email_address):
                messages.add_message(request, messages.ERROR, 'Inappropriate email format')
                valid = False

        if 'group_name' in args and 'contacts' in args and not group_id:
            if not self.group_name:
                messages.add_message(request, messages.ERROR, "Name is required")
                valid = False

            if Group.objects.all().filter(name=self.group_name).first():
                messages.add_message(request, messages.ERROR, "Group with given name already exists")
                valid = False

        if 'group_name' in args and 'contacts' in args and group_id:
            if not self.group_name:
                messages.add_message(request, messages.ERROR, "Name is required")
                valid = False

            if self.group_name == Group.objects.get(pk=group_id).name:
                pass
            elif Group.objects.all().filter(name=self.group_name).first():
                messages.add_message(request, messages.ERROR, "Group with given name already exists")
                valid = False

        return valid
