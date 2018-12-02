from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.core.files.storage import FileSystemStorage
from contact_mail.models import Group, Person
from contact_mail.views.base import BaseView

class AddPictureView(View):
    def post(self, request, id):
        if request.FILES['picture_file']:
            contact = Person.objects.get(pk=id)
            contact.image = request.FILES['picture_file']
            contact.save()
        return redirect('/modify/{}'.format(id))