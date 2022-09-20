from django.db import models
from django import forms

# Create your models here.

# creating a form


class RegistrationForm(forms.Form):
  
    firstName = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'First Name'}))
    lastName = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',  'required': True, 'aria-label': 'Last Name'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Email'}))
    company = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Company'}))
    supplierId = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'required': True, 'aria-label': 'Supplier ID','pattern':'[0-9]+', 'title':'Enter numbers Only '}))
    ileAppFlag = forms.BooleanField(required=False, initial=True,label='ILE')
    faAppFlag = forms.BooleanField(required=False, initial=True,label='FA')
     
class UserDetails:
    uid: int
    firstName: str
    lastName: str
    email: str
    company: str
    supplierId: str
    responseText: str
    user_id: str