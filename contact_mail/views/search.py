from django.shortcuts import render

from contact_mail.models import Person
from contact_mail.views.base import BaseView


class SearchContacts(BaseView):
    @staticmethod
    def get(request):
        if not request.GET.get('name') and not request.GET.get('surname'):
            contacts = Person.objects.all()

        else:
            contacts = Person.objects.all().filter(name__contains=request.GET.get('name').strip()).filter(
                surname__contains=request.GET.get('surname').strip())

        context = {
            'contacts': contacts.order_by('surname', 'name')
        }
        return render(request, 'contact_mail/show_all_contacts.html', context)
