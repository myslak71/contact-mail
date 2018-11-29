"""skrzynka_kontaktowa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from contact_mail.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', ShowAllContactsView.as_view()),
    url('^new$', NewContactView.as_view()),
    url('^show/(?P<id>\d+)$', ShowContactView.as_view()),
    url('^delete/(?P<id>\d+)$', DeleteContactView.as_view()),
    url('^modify/(?P<id>\d+)$', ModifyContactView.as_view()),
    url('^modify/(?P<id>\d+)/addAddress$', AddAddressView.as_view()),
    url('^modify/(?P<id>\d+)/removeAddress$', RemoveAddressView.as_view()),
    url('^modify/(?P<id>\d+)/deleteAddress$', DeleteAddressView.as_view()),
    url('^modify/(?P<id>\d+)/addPhone$', AddPhoneView.as_view()),
    url('^modify/(?P<id>\d+)/modifyPhone/(?P<phone_id>\d+)$', ModifyPhoneView.as_view()),
    url('^modify/(?P<id>\d+)/deletePhone/(?P<phone_id>\d+)$', DeletePhoneView.as_view()),
    url('^modify/(?P<id>\d+)/modifyEmail/(?P<email_id>\d+)$', ModifyEmailView.as_view()),
    url('^modify/(?P<id>\d+)/addEmail$', AddEmailView.as_view()),
    url('^modify/(?P<id>\d+)/deleteEmail/(?P<email_id>\d+)$', DeleteEmailView.as_view()),
    url('^groups$', ShowGroupsView.as_view()),
    url('^groups/add$', AddGroupView.as_view()),
    url('^groups/delete/(?P<group_id>\d+)$', DeleteGroupView.as_view()),
    url('^groups/modify/(?P<group_id>\d+)$', ModifyGroupView.as_view()),
    url('^add_picture$', AddPicture.as_view()),
]
