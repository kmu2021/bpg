from django.db import models
from django import forms

# Create your models here.

# creating a form


class RegistrationForm(forms.Form):
    APP_CHOICES =(
    ("fa1", "FA1"),
    ("ile1", "ILE1"),
    ("fa2", "FA2"),
    ("ile2", "ILE2"),
    ("fa3", "FA3"),
    ("ile3", "ILE3"),
    ("fa4", "FA4"),
    ("ile4", "ILE4"),
    ("fa5", "FA5"),
    ("ile5", "ILE5"),
    ("fa6", "FA6"),
    ("ile6", "ILE6"),
)
  
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
    appList = forms.MultipleChoiceField(choices = APP_CHOICES)
     
class UserDetails:
    uid: int
    firstName: str
    lastName: str
    email: str
    company: str
    supplierId: str
    responseText: str
    user_id: str