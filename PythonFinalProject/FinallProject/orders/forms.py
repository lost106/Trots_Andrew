from django import forms
from .models import *


class CheckOutContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.CharField(required=False)
    comment = forms.CharField(required=False)
    address = forms.CharField(required=True)





