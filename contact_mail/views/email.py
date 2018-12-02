from django.contrib import messages
from django.shortcuts import redirect
from django.views import View

from contact_mail.models import Person, Email
from contact_mail.views.base import BaseView


class AddEmailView(BaseView):
    FORM_FIELDS = ('email_type', 'email_address')

    def post(self, request, id):
        self._get_form_field_values(request)
        if not self._validate_form(request, *self.FORM_FIELDS):
            return redirect('/modify/{}'.format(id))

        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        Email.objects.create(address=self.email_address, type=self.email_type, person=contact)
        messages.add_message(request, messages.INFO, 'Email has been added')
        return redirect('/modify/%s' % id)


class ModifyEmailView(BaseView):
    FORM_FIELDS = ('email_type', 'email_address')

    def post(self, request, id, email_id):
        self._get_form_field_values(request)
        if not self._validate_form(request, *self.FORM_FIELDS):
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


class DeleteEmailView(View):
    @staticmethod
    def post(request, id, email_id):
        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')

        email = Email.objects.get(pk=email_id)
        email.delete()

        messages.add_message(request, messages.INFO, 'Email has been deleted')
        return redirect('/modify/{}'.format(id))
