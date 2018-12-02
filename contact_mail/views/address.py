from django.contrib import messages
from django.shortcuts import redirect
from django.views import View

from contact_mail.models import Person, Address
from contact_mail.views.base import BaseView


class AddAddressView(BaseView):
    FORM_FIELDS = ('city', 'street', 'building_number', 'apartment_number')

    def post(self, request, id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        self._get_form_field_values(request)

        if not self._validate_form(request, *self.FORM_FIELDS):
            return redirect('/modify/{}'.format(id))

        contact.address = Address.objects.create(city=self.city, street=self.street,
                                                 building_number=self.building_number,
                                                 apartment_number=self.apartment_number)
        contact.save()

        messages.add_message(request, messages.INFO, 'Address has been added')
        return redirect('/modify/{}'.format(id))


class RemoveAddressView(View):
    @staticmethod
    def post(request, id):
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
    @staticmethod
    def post(request, id):
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
