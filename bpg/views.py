from django.http import HttpResponse 
from django.shortcuts import render
from requests.sessions import Request
from .models import UspsServices, UserDetails
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import parse,parseString,Document
import os
from pathlib import Path
import json
import requests
from django.conf import settings



def init(request):    
        
    user_data = get_user_name (request)    

    if not hasattr(user_data, "userName") or user_data.userName=="" :
        #Return to HomePage without populating links
        return render(request,'bpgtemplate.html')
    else:
        #Read XML Services File and generate Links            
        xmldoc = ET.parse(os.path.join(os.path.dirname(__file__),'services.xml'))
        root = xmldoc.getroot()
        
        serviceList = []
        
        for child in root:
            service = UspsServices()        
            service.serviceCode = child.attrib['serviceCode'].upper()
            service.serviceName = child.attrib['serviceName']
            service.serviceDescription = child.attrib['serviceDescription']
            service.url = child.attrib['url'].replace('{ENV}',settings.ENVIRONMENT).lower
            if service.serviceCode in user_data.ileAccessList:
                service.accessFlag = True
            else:
                service.accessFlag = False            
            service.id = child.attrib['id']                   
            serviceList.append(service)
        serviceList.append(user_data)    
    return render(request, 'bpgtemplate.html',{"serviceList":serviceList})
        

        
def get_user_name(request):
    
    #For Testing in Local Only
    '''user_details = UserDetails()
    user_details.userName = "Test"
    user_details.ileAccess = ""
    return(user_details)'''
    
    try:
        user_details = UserDetails()
        auth_response = get_access_token(request)[0]
        access_token=auth_response["access_token"]         
        print(access_token)   
 
        graph_response = call_graph (access_token)
        print ("Graph API Returned")
        if "givenName" in graph_response:
            user_details.userName=graph_response["givenName"]
            if "mail" in graph_response:
                user_details.userName = user_details.userName + " (" + graph_response["mail"] + ")"
            #user_details.uid=graph_response["id"]
        user_details.ileAccessList=get_access_list (auth_response['user_claims'])
        return (user_details)
        
    except Exception as e:
        print ("get_user_name Exception")
        print (e)
        user_details.userName=""
        return (user_details)   

def get_access_token(request):

    auth_url = str(request.build_absolute_uri())+".auth/me"
    #auth_url = "https://usps-bpg-dev.azurewebsites.net/.auth/me" #Enable for localhost
    
    try:
        cookie = request.COOKIES.get("AppServiceAuthSession")
        if cookie is not None:
            curSession = requests.Session() # all cookies received will be stored in the session object  
            response = curSession.get(auth_url,cookies=request.COOKIES)                
            auth_json = response.json()          
        return auth_json
    except Exception as e:
        print ("Inside get_access_token exception")
        print (e)

def call_graph(access_token):
    print(access_token)
    response = requests.get("https://graph.microsoft.com/v1.0/me",headers={'Authorization': 'Bearer '+ access_token})
    graph_json = response.json()
    if response.ok:        
        print(graph_json)
    else:    
    
        if "error" in graph_json:
            print(graph_json["error"]["code"])        
        print (response.status_code)
    return graph_json
    
def get_access_list(user_claims):
    ileAccessList=[]
    for userclaims in user_claims:
        if userclaims['typ'].startswith('ILE'):
            ileAccessList.append(userclaims['val'].split("|")[0].upper())
    return(ileAccessList)