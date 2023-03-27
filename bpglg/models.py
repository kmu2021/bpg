from django.db import models
from django import forms

# Create your models here.

# creating a form


class RegistrationForm(forms.Form):

    firstName = forms.CharField(max_length=200, label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'First Name', 'placeholder': "Enter First Name"}))
    lastName = forms.CharField(max_length=200, label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'Last Name', 'placeholder': "Enter Last Name"}))
    workEmail = forms.EmailField(max_length=400, label='Work Email', widget=forms.EmailInput(
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


class UserMgmtSearchForm(forms.Form):
    lastName = forms.CharField(max_length=200, required=False, label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control search-form', 'aria-label': 'Last Name', 'placeholder': "Search by Last Name"}))
    firstName = forms.CharField(max_length=200, required=False, label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control search-form',  'aria-label': 'First Name', 'placeholder': "Search by First Name"}))
    workEmail = forms.CharField(max_length=400, required=False, label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control search-form', 'aria-label': 'Email', 'placeholder': "Search by Email"}))
    company = forms.CharField(max_length=200, required=False, label='Company', widget=forms.TextInput(
        attrs={'class': 'form-control search-form', 'aria-label': 'Company', 'placeholder': "Search by Company"}))
    scac = forms.CharField(max_length=200, required=False, label='SCAC', widget=forms.TextInput(
        attrs={'class': 'form-control search-form', 'aria-label': 'SCAC', 'placeholder': "Search by SCAC"}))
    duns = forms.CharField(max_length=200, required=False, label='DUNS', widget=forms.TextInput(
        attrs={'class': 'form-control search-form',  'aria-label': 'DUNS', 'placeholder': "Search by DUNS"}))
    
    pendingInvitationFlag = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input','aria-label': 'Pending Invitation'}),
        required=False,label='Pending Invitation'
    )


class UserDetails:
    uid: int
    user_id: str
    firstName: str
    lastName: str
    workEmail: str
    company: str
    scac: str
    duns: str
    invitationStatus: str
    supplierId: str
    responseText: str


class EmailDetail:
    email: str
    isVerified: bool
    counter: int
