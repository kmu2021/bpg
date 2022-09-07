from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
import os
#from .models import UspsServices, UserDetails
#import xml.etree.ElementTree as ET
#from xml.dom import minidom
#from xml.dom.minidom import parse,parseString,Document
from pathlib import Path
import json
import requests
from django.shortcuts import render
from .models import RegistrationForm
from django.forms import formset_factory

# Logout Function


def logout(request):
    # Redirect to the logout endpoint of Azure Web
    print("Logout Initiated")
    return HttpResponseRedirect("/.auth/logout")

# Main Init Function


def init(request):
    #    return render(request, 'bpgrgtemplate.html')
    context = {}
   # context['form']= RegistrationForm()
    # creating a formset
    if request.method == 'GET':
        RegistrationFormSet = formset_factory(RegistrationForm, extra=1)
        formset = RegistrationFormSet()
        context['formset'] = formset
        return render(request, "bpgrgtemplate.html", context)
    elif request.method == 'POST':
        print(request)
        RegistrationFormSet = formset_factory(RegistrationForm)
        formset = RegistrationFormSet(data=request.POST)
        context['formset'] = formset
        
        if 'additems' in request.POST and request.POST['additems'] == 'true':
            print("ADDDING")
            formset_dictionary_copy = request.POST.copy()
            formset_dictionary_copy['form-TOTAL_FORMS'] = int(
                formset_dictionary_copy['form-TOTAL_FORMS']) + 1
            formset = RegistrationFormSet(formset_dictionary_copy)
            context['formset'] = formset
        elif 'removeitems' in request.POST and request.POST['removeitems'] == 'true':
            print("Removing")
            formset_dictionary_copy = request.POST.copy()
            formset_dictionary_copy['form-TOTAL_FORMS'] = int(
                formset_dictionary_copy['form-TOTAL_FORMS']) - 1
            formset = RegistrationFormSet(formset_dictionary_copy)
            context['formset'] = formset
        else:
            print ("INSIDE ELSE")
            #Form JSON
            counter = 1
            user_list = []
            for form in formset:
                if form.is_valid():
                    # person = form.save(commit=False)
                    print(form.cleaned_data['lastName'])
                    user_dict = {
                        "uid": counter,
                        "firstName": form.cleaned_data['firstName'],
                        "lastName": form.cleaned_data['lastName'],
                        "email": form.cleaned_data['email'],
                        "company": form.cleaned_data['company'],
                        "supplierId": form.cleaned_data['supplierId'],
                    }
                    user_list.append(user_dict)
                    counter += 1
            print (user_list)
            print (json.dumps(user_list))
            
        return render(request, "bpgrgtemplate.html", context)
    else:
        return render(request, "bpgrgtemplate.html")

    # Add the formset to context dictionary
