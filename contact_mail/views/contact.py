from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from contact_mail.models import Person, Address, Phone, Email
from contact_mail.utils import contact_exist_get
from contact_mail.views.base import BaseView


class ShowAllContactsView(View):
    @staticmethod
    def get(request):
        contacts = Person.objects.all().order_by('surname')
        context = {
            'contacts': contacts,
        }
        return render(request, 'contact_mail/show_all_contacts.html', context)


class ShowContactView(View):
    @staticmethod
    def get(request, id):
        context = {
            'contact': contact_exist_get(id)
        }
        return render(request, 'contact_mail/show_contact.html', context)


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
                   'picture_file',
                   )

    @staticmethod
    def get(request):
        return render(request, 'contact_mail/new_contact.html')

    def post(self, request):
        self._get_form_field_values(request)

        if not self._validate_form(request, *self.FORM_FIELDS):
            return redirect('/new')

        contact = Person.objects.create(name=self.name, surname=self.surname, description=self.description)
        contact.address = Address.objects.create(city=self.city, street=self.street,
                                                 building_number=self.building_number,
                                                 apartment_number=self.apartment_number)

        Phone.objects.create(number=self.number, type=self.phone_type, person=contact)
        Email.objects.create(address=self.email_address, type=self.email_type, person=contact)

        contact.image = self.picture_file
        contact.save()
        messages.add_message(request, messages.INFO, 'Contact has been added')
        return redirect('/')


class DeleteContactView(View):
    @staticmethod
    def post(request, id):
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

        if not self._validate_form(request, *self.FORM_FIELDS):
            return redirect('/modify/{}'.format(id))

        contact.name, contact.surname, contact.description = self.name, self.surname, self.description
        contact.save()

        messages.add_message(request, messages.INFO, 'Personal data has been modified')
        return redirect('/modify/{}'.format(contact.id))
