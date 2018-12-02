from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from contact_mail.models import Group, Person


class AddPictureView(View):
    def post(self, request, id):
        try:
            if request.FILES['picture_file']:
                contact = Person.objects.get(pk=id)
                contact.image = request.FILES['picture_file']
                contact.save()
        except:
            messages.add_message(request, messages.ERROR, 'You need to specify a file path.')
        return redirect('/modify/{}'.format(id))
