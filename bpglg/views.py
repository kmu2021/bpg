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

from .search import search_users
from .models import RegistrationForm, UserDetails
from .graph import processForm
from django.forms import formset_factory

# Logout Function


def logout(request):
    # Redirect to the logout endpoint of Azure Web
    print("Logout Initiated")
    return HttpResponseRedirect("/.auth/logout")

# Search Function
def search(request):
    # Redirect to the Search Page
    print("Redirecting to Search Page")
    context = {}
    users_list = []
    if request.method == 'POST':
        #displayName = request.
        display_name=request.POST['srchDisplayName']
        email=request.POST['srchEmail']
        company_name = request.POST['srchCompanyName']
        invitation_status = request.POST.get('srchInvitationStatus','')
        #user_details = UserDetails()      
        users_list =search_users(email,display_name,company_name, invitation_status)
        print("CONTEXT****")
        #print(context['users_list'][0].uid)

        return render(request, "bpgrgsearch.html", {"users_list":users_list})
    else:
        return render(request, "bpgrgsearch.html", context)

# Main Init Function


def init(request):
    # if this is a GET request present a Blank Form
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'bpglgindex.html',{'form': form})
    
    # if this is a POST request we need to process the form data
    elif request.method == 'POST':
        #print(request)
        form = RegistrationForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user_details = {
                        "uid": "",
                        "firstName": form.cleaned_data['firstName'].strip(),
                        "lastName": form.cleaned_data['lastName'].strip(),
                        "email": form.cleaned_data['workEmail'].strip(),
                        "company": form.cleaned_data['company'].strip(),
                        "responseText": ""
                    }
            print(user_details);
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')