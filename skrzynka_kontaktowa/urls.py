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
    url('^$', ShowAllContacts.as_view()),
    url('^new$', NewContact.as_view()),
    url('^show/(?P<id>\d+)$', ShowContact.as_view()),
    url('^delete/(?P<id>\d+)$', DeleteContact.as_view()),
    url('^modify/(?P<id>\d+)$', ModifyContact.as_view()),
    url('^modify/(?P<id>\d+)/addAddress$', AddAddress.as_view()),
    url('^modify/(?P<id>\d+)/removeAddress$', RemoveAddress.as_view()),
    url('^modify/(?P<id>\d+)/deleteAddress$', DeleteAddress.as_view()),
    url('^modify/(?P<id>\d+)/addPhone$', AddPhone.as_view()),
    url('^modify/(?P<id>\d+)/modifyPhone/(?P<phone_id>\d+)$', ModifyPhone.as_view()),
    url('^modify/(?P<id>\d+)/deletePhone/(?P<phone_id>\d+)$', DeletePhone.as_view()),
    url('^modify/(?P<id>\d+)/modifyEmail/(?P<email_id>\d+)$', ModifyEmail.as_view()),
    url('^modify/(?P<id>\d+)/addEmail$', AddEmail.as_view()),
    url('^modify/(?P<id>\d+)/deleteEmail/(?P<email_id>\d+)$', DeleteEmail.as_view()),

]
