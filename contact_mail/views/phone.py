from django.contrib import messages
from django.shortcuts import redirect
from django.views import View

from contact_mail.models import Person, Phone
from contact_mail.views.base import BaseView


class AddPhoneView(BaseView):
    FORM_FIELDS = ('phone_type', 'number')

    def post(self, request, id):
        self._get_form_field_values(request)
        if not self._validate_form(request, *self.FORM_FIELDS):
            return redirect('/modify/{}'.format(id))

        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        contact = Person.objects.filter(pk=id).first()
        Phone.objects.create(number=self.number, type=self.phone_type, person=contact)

        messages.add_message(request, messages.INFO, 'Phone has been added')
        return redirect('/modify/{}'.format(id))


class ModifyPhoneView(BaseView):
    FORM_FIELDS = ('phone_type', 'number')

    def post(self, request, id, phone_id):
        self._get_form_field_values(request)
        if not self._validate_form(request, *self.FORM_FIELDS):
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


class DeletePhoneView(View):
    @staticmethod
    def post(request, id, phone_id):
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
