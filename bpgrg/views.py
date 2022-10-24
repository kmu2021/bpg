from plistlib import UID
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
from .models import RegistrationForm, UserDetails
from .graph import processForm
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
        #print(context['formset'])
        return render(request, "bpgrgtemplate.html", context)
    elif request.method == 'POST':
        #print(request)
        RegistrationFormSet = formset_factory(RegistrationForm)
        formset = RegistrationFormSet(data=request.POST)
        newFormset = RegistrationFormSet()
        
        context['formset'] = formset
        print("Context")
        print (context)
        print('ADD ITEM------');
        print(request.POST['additems']);
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
            print("INSIDE ELSE")
            # Form JSON
            counter = 0
            user_list = []
            for form in formset:
                print (form)
                form.responseText = "Invalid Data" 
                form.uid=counter               
                if form.is_valid():
                    # person = form.save(commit=False)
                    print("Form is VALID")
                    appListDict = {}
                    appListDict['ileAppFlag']= form.cleaned_data['ileAppFlag']
                    appListDict['faAppFlag']= form.cleaned_data['faAppFlag']                    
                    print("Adding to Dict")
                    user_dict = {
                        "uid": counter,
                        "firstName": form.cleaned_data['firstName'],
                        "lastName": form.cleaned_data['lastName'],
                        "email": form.cleaned_data['email'],
                        "company": form.cleaned_data['company'],
                        "supplierId": form.cleaned_data['supplierId'],
                        "appListDict": appListDict,
                        "responseText": ""
                    }
                    
                    counter += 1
                    print(user_list)                                        
                    user_list.append(user_dict)
                    print("RESPONSE BODY")
                    #print(user_dict.responseText)
                    print(json.dumps(user_list))
                else:
                    print("Form is Invalid")
            if (counter>0):
                
                print("Calling ProcessForm")
                user_details = UserDetails()
                #user_details =processForm(user_list,request.scheme + "://" + os.environ.get('WEBSITE_HOSTNAME'))
                user_details =processForm(user_list,"https://logistics.usps.com/")
                for users in user_details:
                    print("printing users")
                    print(users.responseText) 
                    for form in formset:
                        if (form.uid==users.uid):
                            form.responseText = users.responseText

            #context['userdetails']=user_details
        return render(request, "bpgrgtemplate.html", context)
    else:
        return render(request, "bpgrgtemplate.html")

    # Add the formset to context dictionary
