from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from contact_mail.models import Group, Person
from contact_mail.views.base import BaseView


class ShowGroupsView(View):
    @staticmethod
    def get(request):
        groups = Group.objects.all()
        context = {
            'groups': groups,
        }
        return render(request, 'contact_mail/show_groups.html', context)


class AddGroupView(BaseView):
    FORM_FIELDS = ('group_name',
                   'contacts',
                   )

    def get(self, request):
        context = {
            'contacts': Person.objects.all(),
        }
        return render(request, 'contact_mail/add_group.html', context)

    def post(self, request):
        self._get_form_field_values(request)

        if not self._validate_form(request, *self.FORM_FIELDS):
            return redirect('/groups/add')

        group = Group.objects.create(name=self.group_name)
        for contact_id in self.contacts:
            if Person.objects.filter(pk=contact_id).first():
                contact = Person.objects.get(pk=contact_id)
                contact.group.add(group)

        messages.add_message(request, messages.INFO, "Group has been created")
        return redirect('/groups')


class DeleteGroupView(View):
    @staticmethod
    def post(request, group_id):
        if not Group.objects.filter(pk=group_id).first():
            messages.add_message(request, messages.ERROR, "Group does not exist")
            return redirect('/groups')
        group = Group.objects.get(pk=group_id)
        group.delete()
        messages.add_message(request, messages.INFO, "Group has been deleted")
        return redirect('/groups')


class ModifyGroupView(BaseView):
    FORM_FIELDS = ('group_name',
                   'contacts',
                   )

    @staticmethod
    def get(request, group_id):
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

        self._get_form_field_values(request)

        if not self._validate_form(request, *self.FORM_FIELDS, group_id=group_id):
            return redirect('/groups/modify/{}'.format(group_id))

        if self.group_name == Group.objects.get(pk=group_id).name:
            pass
        elif Group.objects.all().filter(name=self.group_name).first() is not None:
            messages.add_message(request, messages.ERROR, "Group with given name already exists")
            valid = False

        group = Group.objects.get(pk=group_id)
        group.name = self.group_name
        group.person_set.clear()

        for contact_id in self.contacts:
            if Person.objects.filter(pk=contact_id).first():
                contact = Person.objects.get(pk=contact_id)
                contact.group.add(group)

        group.save()
        messages.add_message(request, messages.INFO, "Group has been modified")
        return redirect('/groups/modify/{}'.format(group_id))

    def _form_valid(self, request, group_id):
        valid = True

        if not self.name:
            messages.add_message(request, messages.ERROR, "Name is required")
            valid = False

        if self.name == Group.objects.get(pk=group_id).name:
            pass
        elif Group.objects.all().filter(name=self.name).first():
            messages.add_message(request, messages.ERROR, "Group with given name already exists")
            valid = False

        return valid


class ShowGroupView(View):
    @staticmethod
    def get(request, group_id):
        if not Group.objects.filter(pk=group_id).first():
            messages.add_message(request, messages.ERROR, "Group does not exist")
            return redirect('/groups')
        group = Group.objects.get(pk=group_id)

        if not request.GET.get('name') and not request.GET.get('surname'):
            contacts = group.person_set.all()

        else:
            contacts = group.person_set.all().filter(name__contains=request.GET.get('name')).filter(
                surname__contains=request.GET.get('surname'))

        context = {
            'group': group,
            'contacts': contacts,
        }

        return render(request, 'contact_mail/show_group.html', context)
