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



def init(request):    
        
    user_data = get_user_name (request)

    if not hasattr(user_data, "userName") or user_data.userName=="" :
        #Return to HomePage without populating links
        return render(request,'bpgtemplate.html')
    else:            
        xmldoc = ET.parse(os.path.join(os.path.dirname(__file__),'services.xml'))
        root = xmldoc.getroot()
        
        serviceList = []
        
        for child in root:
            service = UspsServices()        
            service.serviceName = child.attrib['serviceName']
            service.serviceDescription = child.attrib['serviceDescription']
            service.accessFlag = eval(child.attrib['accessFlag'].title())
            service.id = child.attrib['id']                   
            serviceList.append(service)
        serviceList.append(user_data)    
    return render(request, 'bpgtemplate.html',{"serviceList":serviceList})
        

        
def get_user_name(request):
    print('Inside get_user_name Function')
    try:
        user_details = UserDetails()
        auth_url = str(request.build_absolute_uri())+".auth/me"
        print(auth_url)
        access_token=get_access_token(request)[0]["access_token"] 
        print(access_token)   
        print ("Calling Graph API")    
        graph_response = call_graph (access_token)
        print ("Graph API Returned")
        if "givenName" in graph_response:
            user_details.userName=graph_response["givenName"]
            if "mail" in graph_response:
                user_details.userName = user_details.userName + " (" + graph_response["mail"] + ")"
            #user_details.uid=graph_response["id"]
        
        return (user_details)
        
    except Exception as e:
        print ("get_user_name Exception")
        print (e)
        user_details.userName=""
        return (user_details)   

def get_access_token(request):

    auth_url = str(request.build_absolute_uri())+".auth/me"
    #auth_url = "https://usps-bpg-dev.azurewebsites.net/.auth/me" #Enable for localhost
    print("URL TO CALL: "+auth_url)
    
    try:
        cookie = request.COOKIES.get("AppServiceAuthSession")
        if cookie is not None:
            print("Calling Cookie API")
            curSession = requests.Session() # all cookies received will be stored in the session object  
            response = curSession.get(auth_url,cookies=request.COOKIES)  
            print ("Status is "+ str(response.status_code))        
        
            auth_json = response.json()
            '''
        if response.ok:        
            print(auth_json)
        else:    
        
            if "error" in auth_json:
                print(auth_json["error"]["code"])        
            print (response.status_code)
            '''
        return auth_json
    except Exception as e:
        print ("Inside get_access_token exception")
        print (e)

def call_graph(access_token):
    print("Inside call_graph API")
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
    
