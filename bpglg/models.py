from django.db import models
from django import forms

# Create your models here.

# creating a form


class RegistrationForm(forms.Form):

    firstName = forms.CharField(max_length=200, label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'First Name', 'placeholder': "Enter First Name"}))
    lastName = forms.CharField(max_length=200, label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'Last Name', 'placeholder': "Enter Last Name"}))
    workEmail = forms.EmailField(max_length=200, label='Work Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Work Email', 'placeholder': "Enter Work Email"}))
    company = forms.CharField(max_length=200, label='Company', widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Company', 'placeholder': "Enter Company"}))
    scac = forms.CharField(max_length=200, label='SCAC', widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'SCAC', 'placeholder': "Enter SCAC"}))
    duns = forms.CharField(max_length=200, label='DUNS', widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'DUNS', 'placeholder': "Enter DUNS"}))
   # tncFlag = forms.BooleanField(required=False, label='tnc')

    tncFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input checkbox-xl'}),
        required=True
    )

    # widget=forms.CheckboxInput(
    #   attrs={'class': 'form-control form-check-input checkbox-xl', 'required': True, 'aria-label': 'Terms', 'placeholder': "Enter Terms"}))


class UserDetails:
    uid: int
    firstName: str
    lastName: str
    workEmail: str
    company: str
    invitationStatus: str
    supplierId: str
    responseText: str
