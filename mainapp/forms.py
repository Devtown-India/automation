from django import forms
from mainapp.models import *
from django.contrib import admin
class LinkedInForm(forms.ModelForm):
    class Meta():
        model=sentInvitation
        fields='__all__'