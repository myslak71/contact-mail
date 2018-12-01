from django.test import TestCase
from random import randint
# Create your tests here.


def check():
    result = False
    for i in range(10000000):
        if result is not False:
            result = False

def assign():
    result = False
    for i in range(10000000):
        result = False

check()
assign()
print('siema')

"""
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views import View
from .models import *
from django.core.validators import validate_email

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
        number = int(number)
        if number >= 0:
            return number
        raise Exception
    except Exception:
        return None


def contact_exist_get(contact_id):
    contact = Person.objects.filter(pk=contact_id).first()
    if contact is None:
        raise Http404
    return contact


class ShowAllContacts(View):
    def get(self, request):
        contacts = Person.objects.all().order_by('surname')
        context = {
            'contacts': contacts,
        }
        return render(request, 'contact_mail/show_all_contacts.html', context)


class ShowContact(View):
    def get(self, request, id):
        context = {
            'contact': contact_exist_get(id)
        }
        return render(request, 'contact_mail/show_contact.html', context)


class NewContact(View):
    def get(self, request):
        return render(request, 'contact_mail/new_contact.html')

    def post(self, request):
        # Personal data
        if request.POST.get('name').strip() == '' or request.POST.get('surname').strip() == '':
            messages.add_message(request, messages.ERROR, "Name and surname are required")
            return redirect('/new')
        name = request.POST.get('name').strip()
        surname = request.POST.get('surname').strip()
        description = request.POST.get('description').strip()
        contact = Person.objects.create(name=name, surname=surname, description=description)
        # Address
        city = request.POST.get('city').strip()
        street = request.POST.get('street').strip()
        building_number = request.POST.get('building_number').strip()
        apartment_number = request.POST.get('apartment_number').strip()
        address = Address.objects.create(city=city, street=street,
                                         building_number=building_number,
                                         apartment_number=apartment_number)
        contact.address = address
        # Phone
        if request.POST.get('phone_type').strip() not in str(PHONE_CHOICES):
            messages.add_message(request, messages.ERROR, "Inappropriate phone type value")
            return redirect('/new')
        if request.POST.get('number').strip() == '' or check_if_unsigned_int(
                request.POST.get('number').strip()) is None:
            messages.add_message(request, messages.ERROR, "Inappropriate phone number")
            return redirect('/new')
        number = request.POST.get('number').strip()
        phone_type = request.POST.get('phone_type').strip()
        Phone.objects.create(number=number, type=phone_type, person=contact)
        # Email
        if request.POST.get('email_type').strip() not in str(EMAIL_CHOICES):
            messages.add_message(request, messages.ERROR, "Inappropriate email type value")
            return redirect('/new')
        if request.POST.get('email_address').strip() == '':
            messages.add_message(request, messages.ERROR, "Inappropriate email address")
            return redirect('/new')
        if check_email(request.POST.get('email_address').strip()) is False:
            messages.add_message(request, messages.ERROR, "Inappropriate email address")
            return redirect('/new')
        email_address = request.POST.get('email_address').strip()
        email_type = request.POST.get('email_type').strip()
        Email.objects.create(address=email_address, type=email_type, person=contact)
        contact.save()
        messages.add_message(request, messages.INFO, "Contact has been added")
        return redirect('/')


class DeleteContact(View):
    def post(self, request, id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        Person.objects.filter(pk=id).first().delete()
        messages.add_message(request, messages.INFO, "Contact has been deleted")
        return redirect('/')


class ModifyContact(View):
    def get(self, request, id):
        context = {
            'contact': contact_exist_get(id),
        }
        return render(request, 'contact_mail/modify_contact.html', context)

    def post(self, request, id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        contact = Person.objects.filter(pk=id).first()
        name = request.POST.get('name').strip()
        surname = request.POST.get('surname').strip()
        description = request.POST.get('description').strip()
        contact.name = name
        contact.surname = surname
        contact.description = description
        contact.save()
        messages.add_message(request, messages.INFO, "Personal data has been modified")
        return redirect('/modify/%s' % contact.id)


class AddAddress(View):
    def post(self, request, id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        contact = Person.objects.filter(pk=id).first()
        city = request.POST.get('city').strip()
        street = request.POST.get('street').strip()
        building_number = request.POST.get('building_number').strip()
        apartment_number = request.POST.get('apartment_number').strip()
        address = Address.objects.create(city=city, street=street,
                                         building_number=building_number,
                                         apartment_number=apartment_number)
        contact.address = address
        contact.save()
        messages.add_message(request, messages.INFO, "Address has been added")
        return redirect('/modify/%s' % id)


# Disassociates address from contact
class RemoveAddress(View):
    def post(self, request, id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        contact = Person.objects.filter(pk=id).first()
        if contact.address is None:
            messages.add_message(request, messages.ERROR, "Address does not exist")
            return redirect('/modify/%s' % id)
        address = Address.objects.get(pk=contact.address.id)
        address.person_set.clear()
        messages.add_message(request, messages.INFO, "Address has been disassociated from contact")
        return redirect('/modify/%s' % id)


# Deletes address permanently
class DeleteAddress(View):
    def post(self, request, id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        if contact.address is None:
            messages.add_message(request, messages.ERROR, "Address does not exist")
            return redirect('/modify/%s' % id)
        contact = Person.objects.filter(pk=id).first()
        address = Address.objects.get(pk=contact.address.id)
        address.person_set.delete()
        messages.add_message(request, messages.INFO, "Address has been deleted")
        return redirect('/modify/%s' % id)


class AddPhone(View):
    def post(self, request, id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        if request.POST.get('type').strip() not in str(PHONE_CHOICES):
            messages.add_message(request, messages.ERROR, "Inappropriate phone type value")
            return redirect('/modify/%s' % id)
        if request.POST.get('number').strip() == '' or check_if_unsigned_int(
                request.POST.get('number').strip()) is None:
            messages.add_message(request, messages.ERROR, "Inappropriate phone number")
            return redirect('/modify/%s' % id)
        contact = Person.objects.filter(pk=id).first()
        number = request.POST.get('number').strip()
        phone_type = request.POST.get('type').strip()
        Phone.objects.create(number=number, type=phone_type, person=contact)
        messages.add_message(request, messages.INFO, "Phone has been added")
        return redirect('/modify/%s' % id)


class ModifyPhone(View):
    def post(self, request, id, phone_id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        if Phone.objects.filter(pk=phone_id).first() is None:
            messages.add_message(request, messages.ERROR, "Phone does not exist")
            return redirect('/modify/%s')
        if request.POST.get('type').strip() not in str(PHONE_CHOICES):
            messages.add_message(request, messages.ERROR, "Inappropriate phone type value")
            return redirect('/modify/%s' % id)
        if request.POST.get('number').strip() == '' or check_if_unsigned_int(
                request.POST.get('number').strip()) is None:
            messages.add_message(request, messages.ERROR, "Inappropriate phone number")
            return redirect('/modify/%s' % id)
        phone = Phone.objects.filter(pk=phone_id).first()
        number = request.POST.get('number').strip()
        phone_type = request.POST.get('type').strip()
        phone.number = number
        phone.type = phone_type
        phone.save()
        messages.add_message(request, messages.INFO, "Phone has been modified")
        return redirect('/modify/%s' % id)


class DeletePhone(View):
    def post(self, request, id, phone_id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        if Phone.objects.filter(pk=phone_id).first() is None:
            messages.add_message(request, messages.ERROR, "Phone does not exist")
            return redirect('/modify/%s')
        phone = Phone.objects.filter(pk=phone_id).first()
        phone.delete()
        messages.add_message(request, messages.INFO, "Phone has been deleted")
        return redirect('/modify/%s' % id)


class AddEmail(View):
    def post(self, request, id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        if request.POST.get('type').strip() not in str(EMAIL_CHOICES):
            messages.add_message(request, messages.ERROR, "Inappropriate email type value")
            return redirect('/modify/%s' % id)
        if request.POST.get('address').strip() == '':
            messages.add_message(request, messages.ERROR, "Inappropriate email address")
            return redirect('/modify/%s' % id)
        if check_email(request.POST.get('address').strip()) is False:
            messages.add_message(request, messages.ERROR, "Inappropriate email address")
            return redirect('/modify/%s' % id)
        contact = Person.objects.filter(pk=id).first()
        email_address = request.POST.get('address').strip()
        email_type = request.POST.get('type').strip()
        Email.objects.create(address=email_address, type=email_type, person=contact)
        messages.add_message(request, messages.INFO, "Email has been added")
        return redirect('/modify/%s' % id)


class ModifyEmail(View):
    def post(self, request, id, email_id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        if request.POST.get('type').strip() not in str(EMAIL_CHOICES):
            messages.add_message(request, messages.ERROR, "Inappropriate email type value")
            return redirect('/modify/%s' % id)
        if request.POST.get('address').strip() == '':
            messages.add_message(request, messages.ERROR, "Inappropriate email address")
            return redirect('/modify/%s' % id)
        if check_email(request.POST.get('address').strip()) is False:
            messages.add_message(request, messages.ERROR, "Inappropriate email address")
            return redirect('/modify/%s' % id)
        email = Email.objects.get(pk=email_id)
        address = request.POST.get('address').strip()
        email_type = request.POST.get('type').strip()
        email.address = address
        email.type = email_type
        email.save()
        messages.add_message(request, messages.INFO, "Email has been modified")
        return redirect('/modify/%s' % id)


class DeleteEmail(View):
    def post(self, request, id, email_id):
        if Person.objects.filter(pk=id).first() is None:
            messages.add_message(request, messages.ERROR, "Contact does not exist")
            return redirect('/')
        email = Email.objects.get(pk=email_id)
        email.delete()
        messages.add_message(request, messages.INFO, "Email has been deleted")
        return redirect('/modify/%s' % id)


class ShowGroups(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups,
        }
        return render(request, 'contact_mail/show_groups.html', context)


class AddGroup(View):
    def get(self, request):
        contacts = Person.objects.all()
        context = {
            'contacts': contacts,
        }
        return render(request, 'contact_mail/add_group.html', context)

    def post(self, request):
        name = request.POST.get('name').strip()
        if Group.objects.all().filter(name=name).first() is not None:
            messages.add_message(request, messages.ERROR, "Group with given name already exists")
            return redirect('/groups/add')
        group = Group.objects.create(name=name)
        contacts_id = request.POST.getlist('contacts')
        for contact_id in contacts_id:
            if Person.objects.filter(pk=contact_id).first() is None:
                continue
            contact = Person.objects.get(pk=contact_id)
            contact.group.add(group)
        messages.add_message(request, messages.INFO, "Group has been created")
        return redirect('/groups')


class DeleteGroup(View):
    def post(self, request, group_id):
        if Group.objects.filter(pk=group_id).first() is None:
            messages.add_message(request, messages.ERROR, "Group does not exist")
            return redirect('/groups')
        group = Group.objects.get(pk=group_id)
        group.delete()
        messages.add_message(request, messages.INFO, "Group has been deleted")
        return redirect('/groups')


class ModifyGroup(View):
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
        name = request.POST.get('name').strip()
        if name == Group.objects.get(pk=group_id).name:
            pass
        elif Group.objects.all().filter(name=name).first() is not None:
            messages.add_message(request, messages.ERROR, "Group with given name already exists")
            return redirect('/groups/add')
        group = Group.objects.get(pk=group_id)
        group.person_set.clear()
        contacts_id = request.POST.getlist('contacts')
        for contact_id in contacts_id:
            if Person.objects.filter(pk=contact_id).first() is None:
                continue
            contact = Person.objects.get(pk=contact_id)
            contact.group.add(group)
        messages.add_message(request, messages.INFO, "Group has been modified")
        return redirect('/groups')
"""

if not self._validate_form(request, self.FORM_FIELDS):
    return redirect('/new')