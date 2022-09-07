from django.db import models
from django import forms

# Create your models here.

# creating a form


class RegistrationForm(forms.Form):
    firstName = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    lastName = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    company = forms.CharField(label='Company', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    supplierId = forms.IntegerField(
        label='Supplier ID', widget=forms.TextInput(attrs={'class': 'form-control'}))
