from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
import os
from .models import UspsServices, UserDetails
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import parse,parseString,Document
from pathlib import Path
import json
import requests


# Logout Function
def logout(request):
    # Redirect to the logout endpoint of Azure Web
    print("Redirecting to Logout")
    return HttpResponseRedirect("/.auth/logout")

# Main Init Function
def init(request):    
    print("InitRequest")
    # Populate User Details    
    user_data = get_user_name (request)    

    if not hasattr(user_data, "userName") or user_data.userName=="" :
        # If User Details not available, Return to HomePage without populating links
        print("Not Authenticated. Redirecting to Homepage")
        return render(request,'bpgtemplate.html')
    else:
        # If User Details are available, read XML Services File and generate Links            
        xmldoc = ET.parse(os.path.join(os.path.dirname(__file__),'services.xml'))
        root = xmldoc.getroot()
        
        serviceList = []
        
        for child in root:
            service = UspsServices()        
            service.serviceCode = child.attrib['serviceCode'].upper()
            service.serviceName = child.attrib['serviceName']
            service.serviceDescription = child.attrib['serviceDescription']
            # Service URL is generated based upon ENVIRONMENT variable
            service.url = child.attrib['url'].replace('{ENV}',settings.ENVIRONMENT).lower
            # If ServiceCode (from xml) is available in User's ILE Access List, show the service
            if service.serviceCode in user_data.ileAccessList:
                service.accessFlag = True
            else:
                service.accessFlag = False            
            service.id = child.attrib['id']                   
            serviceList.append(service)
        serviceList.append(user_data)
    return render(request, 'bpgtemplate.html',{"serviceList":serviceList})
        

# Get User Details        
def get_user_name(request):
    print("inside get_user_name")
    # For Testing in Local Only. Will be removed before deployment to Prod
    '''user_details = UserDetails()
    user_details.userName = "Test"
    user_details.ileAccess = ""
    return(user_details)'''
    
    try:
        user_details = UserDetails()
        # Get JSON containing Access Token
        auth_response = get_access_token(request)[0]
        access_token=auth_response["access_token"]         
        
        # Call Graph API with the access token
        graph_response = call_graph (access_token)
        
        # Generate UserName to be shown in page
        if "givenName" in graph_response:
            user_details.userName=graph_response["givenName"]
            if "mail" in graph_response:
                user_details.userName = user_details.userName + " (" + graph_response["mail"] + ")"
        # Generate a list of user-claims user has access to
        user_details.ileAccessList=get_access_list (auth_response['user_claims'])
        return (user_details)
        
    except Exception as e:
        print ("get_user_name Exception")
        print (e)
        user_details.userName=""
        return (user_details)   

# Fetch Access Token for the validated user
def get_access_token(request):

    #auth_url = request.scheme + "://" + os.environ.get('WEBSITE_HOSTNAME') +"/.auth/me"
    auth_url = "/.auth/me"
    print("AUTH URL"+auth_url)
    try:
        print("Getting Access Token")
        cookie = request.COOKIES.get("AppServiceAuthSession")
        if cookie is not None:
            curSession = requests.Session() # all cookies received will be stored in the session object  

            # Pass Authentication Cookie to fetch access token
            response = curSession.get(auth_url,cookies=request.COOKIES)                
            auth_json = response.json()          
        return auth_json
    except Exception as e:
        print ("Inside get_access_token exception")
        print (e)

def call_graph(access_token):
    print("inside call_graph")
    # Call Graph API using access token
    response = requests.get("https://graph.microsoft.com/v1.0/me",headers={'Authorization': 'Bearer '+ access_token})
    graph_json = response.json()
    if response.ok:        
        print(graph_json)
    else:    
    
        if "error" in graph_json:
            print(graph_json["error"]["code"])        
        print (response.status_code)
    return graph_json

# Generate a list of ILE claims user has access to    
def get_access_list(user_claims):
    ileAccessList=[]
    for userclaims in user_claims:
        if userclaims['typ'].startswith('ILE'):
            ileAccessList.append(userclaims['val'].split("|")[0].upper())
    return(ileAccessList)