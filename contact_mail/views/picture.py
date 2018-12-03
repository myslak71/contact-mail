from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from contact_mail.models import Group, Person


class AddPictureView(BaseView):
    FORM_FIELDS = ('picture_file',)
    def post(self, request, id):
        self._get_form_field_values(request)

        if not self._validate_form(request, *self.FORM_FIELDS):
            return redirect('/modify/{}'.format(id))

        contact = Person.objects.filter(pk=id).first()

        if not contact:
            messages.add_message(request, messages.ERROR, 'Contact does not exist')
            return redirect('/')
        contact.image = self.picture_file
        contact.save()
        
        return redirect('/modify/{}'.format(id))
