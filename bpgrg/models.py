from django.db import models
from django import forms

# Create your models here.

# creating a form


class RegistrationForm(forms.Form):
    APP_CHOICES = (
        ("iles", "ILE"),
        ("fas", "FA"),
    )

    firstName = forms.CharField(max_length=2000, widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'First Name'}))
    lastName = forms.CharField(max_length=2000, widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'Last Name'}))
    email = forms.EmailField(max_length=2000, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Email'}))
    company = forms.CharField(max_length=2000, widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Company'}))
  #  supplierId = forms.IntegerField(widget=forms.TextInput(
   #     attrs={'class': 'form-control', 'required': True, 'aria-label': 'Supplier ID', 'pattern': '[0-9]+', 'title': 'Enter numbers Only '}))
    supplierId = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Please Click', 'required': True, 'readonly': 'readonly', 'aria-label': 'Supplier ID'}))   
    ileAppFlag = forms.BooleanField(required=False, initial=True, label='ILE')
    faAppFlag = forms.BooleanField(required=False, initial=True, label='FA')
   # appList = forms.MultipleChoiceField(
    #    choices=APP_CHOICES, widget=forms.CheckboxSelectMultiple)


class UserDetails:
    uid: int
    firstName: str
    lastName: str
    email: str
    company: str
    invitationStatus: str
    supplierId: str
    responseText: str
    user_id: str
    appListDict = {}
