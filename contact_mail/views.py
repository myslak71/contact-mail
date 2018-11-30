from abc import ABC

from django.contrib import messages
from django.core.validators import validate_email
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from .models import *

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


class ShowAllContactsView(View):
    def get(self, request):
        contacts = Person.objects.all().order_by('surname')
        context = {
            'contacts': contacts,
        }
        return render(request, 'contact_mail/show_all_contacts.html', context)


class ShowContactView(View):
    def get(self, request, id):
        context = {
            'contact': contact_exist_get(id)
        }
        return render(request, 'contact_mail/show_contact.html', context)


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


class NewContactView(BaseView):
    FORM_FIELDS = ('name',
                   'surname',
                   'description',
                   'city',
                   'street',
                   'building_number',
                   'apartment_number',
                   'phone_type',
                   'number',
                   'email_type',
                   'email_address',
                   )

    @staticmethod
    def get(request):
        return render(request, 'contact_mail/new_contact.html')

    def post(self, request):
        self._get_form_field_values(request)

        if not self._form_valid(request):
            return redirect('/new')

        contact = Person.objects.create(name=self.name, surname=self.surname, description=self.description)
        contact.address = Address.objects.create(city=self.city, street=self.street,
                                                 building_number=self.building_number,
                                                 apartment_number=self.apartment_number)

        Phone.objects.create(number=self.number, type=self.phone_type, person=contact)
        Email.objects.create(address=self.email_address, type=self.email_type, person=contact)

        contact.save()
        messages.add_message(request, messages.INFO, 'Contact has been added')
        return redirect('/')

    def _form_valid(self, request):
        valid = True  # adds message for every inappropriate input

        if not self.name or not self.surname:
            messages.add_message(request, messages.ERROR, 'Name and surname are required')
            valid = False

        if self.phone_type not in str(PHONE_CHOICES):
            messages.add_message(request, messages.ERROR, 'Inappropriate phone type value')
            valid = False

        if not self.number or not check_if_unsigned_int(self.number):
            messages.add_message(request, messages.ERROR, 'Inappropriate phone number')
            valid = False

        if self.email_type not in str(EMAIL_CHOICES):
            messages.add_message(request, messages.ERROR, 'Inappropriate email type value')
            valid = False

        if not self.email_address:
            messages.add_message(request, messages.ERROR, 'Inappropriate email address')
            valid = False

        if not check_email(self.email_address):
            messages.add_message(request, messages.ERROR, 'Inappropriate email address')
            valid = False

        return valid


class DeleteContactView(View):
    def post(self, request, id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        contact.delete()
        messages.add_message(request, messages.INFO, 'Contact has been deleted')
        return redirect('/')


class ModifyContactView(BaseView):
    FORM_FIELDS = ('name',
                   'surname',
                   'description')

    @staticmethod
    def get(request, id):
        context = {
            'contact': contact_exist_get(id),
        }
        return render(request, 'contact_mail/modify_contact.html', context)

    def post(self, request, id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        self._get_form_field_values(request)

        if not self._form_valid(request):
            return redirect('/new')

        contact.name, contact.surname, contact.description = self.name, self.surname, self.description
        contact.save()

        messages.add_message(request, messages.INFO, 'Personal data has been modified')
        return redirect('/modify/{}'.format(contact.id))

    def _form_valid(self, request):
        valid = True  # adds message for every inappropriate input

        if not self.name or not self.surname:
            messages.add_message(request, messages.ERROR, 'Name and surname are required')
            valid = False

        return valid


class AddAddressView(BaseView):
    FORM_FIELDS = ('city', 'street', 'building_number', 'apartment_number')

    def post(self, request, id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        self._get_form_field_values(request)

        if not self._form_valid(request):
            return redirect('/modify/{}'.format(id))

        address = Address.objects.create(city=self.city, street=self.street,
                                         building_number=self.building_number,
                                         apartment_number=self.apartment_number)

        contact.address = address
        contact.save()

        messages.add_message(request, messages.INFO, 'Address has been added')
        return redirect('/modify/{}'.format(id))

    def _form_valid(self, request):
        valid = True

        if not self.city or not self.street or not self.building_number or not self.apartment_number:
            messages.add_message(request, messages.ERROR, 'Inappropriate address')
            valid = False

        return valid


class RemoveAddressView(View):

    def post(self, request, id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        if not contact.address:
            messages.add_message(request, messages.ERROR, 'Address does not exist')
            return redirect('/modify/{}'.format(id))

        address = Address.objects.get(pk=contact.address.id)
        address.person_set.clear()

        messages.add_message(request, messages.INFO, 'Address has been disassociated from contact')
        return redirect('/modify/{}'.format(id))


class DeleteAddressView(View):
    def post(self, request, id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        if not contact.address:
            messages.add_message(request, messages.ERROR, 'Address does not exist')
            return redirect('/modify/{}'.format(id))

        address = Address.objects.get(pk=contact.address.id)
        address.person_set.delete()

        messages.add_message(request, messages.INFO, 'Address has been deleted')
        return redirect('/modify/{}'.format(id))


class AddPhoneView(BaseView):
    FORM_FIELDS = ('phone_type', 'number')

    def post(self, request, id):
        self._get_form_field_values(request)
        if not self._form_valid(request):
            return redirect('/modify/{}'.format(id))

        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        contact = Person.objects.filter(pk=id).first()
        Phone.objects.create(number=self.number, type=self.phone_type, person=contact)

        messages.add_message(request, messages.INFO, 'Phone has been added')
        return redirect('/modify/{}'.format(id))

    def _form_valid(self, request):
        valid = True

        if self.phone_type not in str(PHONE_CHOICES):
            messages.add_message(request, messages.ERROR, 'Inappropriate phone type value')
            valid = False

        if not self.number or not check_if_unsigned_int(self.number):
            messages.add_message(request, messages.ERROR, 'Inappropriate phone number')
            valid = False

        return valid


class ModifyPhoneView(BaseView):
    FORM_FIELDS = ('phone_type', 'number')

    def post(self, request, id, phone_id):
        self._get_form_field_values(request)
        if not self._form_valid(request):
            return redirect('/modify/{}'.format(id))

        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        phone = Phone.objects.filter(pk=phone_id).first()

        if not phone:
            messages.add_message(request, messages.ERROR, 'Phone does not exist')
            return redirect('/modify/{}'.format(id))

        phone.number, phone.type = self.number, self.phone_type
        phone.save()

        messages.add_message(request, messages.INFO, 'Phone has been modified')
        return redirect('/modify/{}'.format(id))

    def _form_valid(self, request):
        valid = True

        if not self.number or not check_if_unsigned_int(self.number):
            messages.add_message(request, messages.ERROR, 'Inappropriate phone number')
            valid = False

        if self.phone_type not in str(PHONE_CHOICES):
            messages.add_message(request, messages.ERROR, 'Inappropriate phone type value')
            valid = False

        return valid


class DeletePhoneView(View):
    def post(self, request, id, phone_id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        phone = Phone.objects.filter(pk=phone_id).first()

        if not phone:
            messages.add_message(request, messages.ERROR, 'Phone does not exist')
            return redirect('/modify/{}'.format(id))

        phone.delete()

        messages.add_message(request, messages.INFO, 'Phone has been deleted')
        return redirect('/modify/{}'.format(id))


class AddEmailView(BaseView):
    FORM_FIELDS = ('email_type', 'email_address')

    def post(self, request, id):
        self._get_form_field_values(request)
        if not self._form_valid(request):
            return redirect('/modify/{}'.format(id))

        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        Email.objects.create(address=self.email_address, type=self.email_type, person=contact)
        messages.add_message(request, messages.INFO, 'Email has been added')
        return redirect('/modify/%s' % id)

    def _form_valid(self, request):
        valid = True

        if self.email_type not in str(EMAIL_CHOICES):
            messages.add_message(request, messages.ERROR, 'Inappropriate email type value')
            valid = False

        if not self.email_address or not check_email(self.email_address):
            messages.add_message(request, messages.ERROR, 'Inappropriate email address')
            valid = False

        return valid


class ModifyEmailView(BaseView):
    FORM_FIELDS = ('email_type', 'email_address')

    def post(self, request, id, email_id):
        self._get_form_field_values(request)
        if not self._form_valid(request):
            return redirect('/modify/{}'.format(id))

        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        email = Email.objects.get(pk=email_id)
        email.address, email.type = self.email_address, self.email_type
        email.save()

        messages.add_message(request, messages.INFO, 'Email has been modified')
        return redirect('/modify/%s' % id)

    def _form_valid(self, request):
        valid = True

        if self.email_type not in str(EMAIL_CHOICES):
            messages.add_message(request, messages.ERROR, 'Inappropriate email type value')
            valid = False

        if not self.email_address or not check_email(self.email_address):
            messages.add_message(request, messages.ERROR, 'Inappropriate email address')
            valid = False

        return valid


class DeleteEmailView(View):
    def post(self, request, id, email_id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        email = Email.objects.get(pk=email_id)
        email.delete()

        messages.add_message(request, messages.INFO, 'Email has been deleted')
        return redirect('/modify/{}'.format(id))


class ShowGroupsView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups,
        }
        return render(request, 'contact_mail/show_groups.html', context)


class AddGroupView(BaseView):
    FORM_FIELDS = ('name',
                   'contacts',
                   )

    def get(self, request):
        contacts = Person.objects.all()
        context = {
            'contacts': contacts,
        }
        return render(request, 'contact_mail/add_group.html', context)

    def post(self, request):
        self._get_form_field_values(request)
        if not self._form_valid(request):
            return redirect('/groups/add')

        group = Group.objects.create(name=self.name)
        for contact_id in self.contacts:
            if Person.objects.filter(pk=contact_id).first():
                contact = Person.objects.get(pk=contact_id)
                contact.group.add(group)

        messages.add_message(request, messages.INFO, "Group has been created")
        return redirect('/groups')

    def _form_valid(self, request):
        valid = True

        if not self.name:
            messages.add_message(request, messages.ERROR, "Name is required")
            valid = False

        if Group.objects.all().filter(name=self.name).first() is not None:
            messages.add_message(request, messages.ERROR, "Group with given name already exists")
            valid = False

        return valid


class DeleteGroupView(View):
    def post(self, request, group_id):
        if not Group.objects.filter(pk=group_id).first():
            messages.add_message(request, messages.ERROR, "Group does not exist")
            return redirect('/groups')
        group = Group.objects.get(pk=group_id)
        group.delete()
        messages.add_message(request, messages.INFO, "Group has been deleted")
        return redirect('/groups')


class ModifyGroupView(BaseView):
    FORM_FIELDS = ('name',
                   'contacts',
                   )

    def get(self, request, group_id):
        if Group.objects.filter(pk=group_id).first() is None:
            messages.add_message(request, messages.ERROR, "Group does not exist")
            return redirect('/groups')
        group = Group.objects.get(pk=group_id)
        contacts = Person.objects.all()
        context = {
            'group': group,
            'contacts': contacts,
        }
        return render(request, 'contact_mail/modify_group.html', context)

    def post(self, request, group_id):
        if Group.objects.filter(pk=group_id).first() is None:
            messages.add_message(request, messages.ERROR, "Group does not exist")
            return redirect('/groups')

        self._get_form_field_values(request)
        if not self._form_valid(request, group_id):
            return redirect('/groups/modify/{}'.format(group_id))

        group = Group.objects.get(pk=group_id)
        group.name = self.name
        group.person_set.clear()

        for contact_id in self.contacts:
            if Person.objects.filter(pk=contact_id).first():
                contact = Person.objects.get(pk=contact_id)
                contact.group.add(group)

        group.save()
        messages.add_message(request, messages.INFO, "Group has been modified")
        return redirect('/groups')

    def _form_valid(self, request, group_id):
        valid = True

        if not self.name:
            messages.add_message(request, messages.ERROR, "Name is required")
            valid = False

        if self.name == Group.objects.get(pk=group_id).name:
            pass
        elif Group.objects.all().filter(name=self.name).first() is not None:
            messages.add_message(request, messages.ERROR, "Group with given name already exists")
            valid = False

        return valid


class ShowGroupView(View):
    def get(self, request, group_id):
        if Group.objects.filter(pk=group_id).first() is None:
            messages.add_message(request, messages.ERROR, "Group does not exist")
            return redirect('/groups')
        group = Group.objects.get(pk=group_id)

        if not request.GET.get('name') and not request.GET.get('surname'):
            contacts = group.person_set.all()

        else:
            contacts = group.person_set.all().filter(name__contains=request.GET.get('name')).filter(
                surname__contains='')

        context = {
            'group': group,
            'contacts': contacts,
        }

        return render(request, 'contact_mail/show_group.html', context)
