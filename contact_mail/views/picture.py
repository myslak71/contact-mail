from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.core.files.storage import FileSystemStorage
from contact_mail.models import Group, Person
from contact_mail.views.base import BaseView


class AddPictureView(View):
    def post(self, request, id):
        try:
            if request.FILES['picture_file']:
                print(request.FILES['picture_file'])
                contact = Person.objects.get(pk=id)
                contact.image = request.FILES['picture_file']
                contact.save()
        except:
            messages.add_message(request, messages.ERROR, 'You need to specify file path.')
        return redirect('/modify/{}'.format(id))
