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

# Logout Function
def logout(request):
    # Redirect to the logout endpoint of Azure Web
    print("Logout Initiated")
    return HttpResponseRedirect("/.auth/logout")    

# Main Init Function
def init(request):  
    return render(request, 'bpgrgtemplate.html')