from django.shortcuts import render
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
    print("ABSOULTE URL: " + request.build_absolute_uri())

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
        access_token=get_access_token(request)
        graph_response = call_graph (access_token)
        #graph_response = call_graph ("eyJ0eXAiOiJKV1QiLCJub25jZSI6ImFXLVRaTkdfZUJoUFFQa3FGLWlZMER1NXZFNWNrMFZGUHlvb2c3eWFBVFkiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9mOWFhNTc4OC1lYjMzLTRhNDktOGFkMC03NjEwMTkxMGNhYzMvIiwiaWF0IjoxNjI1NTUzNTc2LCJuYmYiOjE2MjU1NTM1NzYsImV4cCI6MTYyNTU1NzQ3NiwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsidXJuOnVzZXI6cmVnaXN0ZXJzZWN1cml0eWluZm8iLCJ1cm46bWljcm9zb2Z0OnJlcTEiLCJ1cm46bWljcm9zb2Z0OnJlcTIiLCJ1cm46bWljcm9zb2Z0OnJlcTMiLCJjMSIsImMyIiwiYzMiLCJjNCIsImM1IiwiYzYiLCJjNyIsImM4IiwiYzkiLCJjMTAiLCJjMTEiLCJjMTIiLCJjMTMiLCJjMTQiLCJjMTUiLCJjMTYiLCJjMTciLCJjMTgiLCJjMTkiLCJjMjAiLCJjMjEiLCJjMjIiLCJjMjMiLCJjMjQiLCJjMjUiXSwiYWlvIjoiRTJaZ1lQanhiNE1zYTJLejBsV0paSTMyYmF5bm13VVVEbVQ4cU5lN3hTUGY5KzdlcitjQSIsImFtciI6WyJwd2QiXSwiYXBwX2Rpc3BsYXluYW1lIjoidXNwcy1icGctZGV2IiwiYXBwaWQiOiJiZDdlYTZiMS1mOTQ3LTQ1OWQtYWQ1YS0wZWEzZmM1NWNjODUiLCJhcHBpZGFjciI6IjEiLCJmYW1pbHlfbmFtZSI6Ik11cmFyaSIsImdpdmVuX25hbWUiOiJLaXNob3JlIiwiaWR0eXAiOiJ1c2VyIiwiaW5fY29ycCI6InRydWUiLCJpcGFkZHIiOiI1Ni4xNTguMTI4LjIiLCJuYW1lIjoiTXVyYXJpLCBLaXNob3JlIC0gVG9wZWthLCBLUyAtIENvbnRyYWN0b3IiLCJvaWQiOiIzZDBmMWRjZS1iZjRiLTQwMzItOTgxNS05N2UwNDEzMmYzZGIiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtODE1Njg0Mzk0LTEwODI3OTk4NDItMTEwMzU2NzI5OC01MDk0Nzc1IiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAwOEEyQjY1MUYiLCJwd2RfZXhwIjoiMTAzMTQ1OCIsInJoIjoiMC5BUmdBaUZlcS1UUHJTVXFLMEhZUUdSREt3N0dtZnIxSC1aMUZyVm9Pb194VnpJVVlBR1EuIiwic2NwIjoiVXNlci5SZWFkIHByb2ZpbGUgb3BlbmlkIGVtYWlsIiwic3ViIjoiSmVLX3pwZS1vcHI2SUdHVEpaWFl2R2FYWk81b2YwTThjWUdwNmpKSU9HMCIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJOQSIsInRpZCI6ImY5YWE1Nzg4LWViMzMtNGE0OS04YWQwLTc2MTAxOTEwY2FjMyIsInVuaXF1ZV9uYW1lIjoiS2lzaG9yZS5NdXJhcmlAdXNwcy5nb3YiLCJ1cG4iOiJLaXNob3JlLk11cmFyaUB1c3BzLmdvdiIsInV0aSI6ImNTeDVPVTlRWlVxRFJnODc3ZDVuQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfc3QiOnsic3ViIjoidGxkQVlCbHJFVEZqXzBFVlB5RGpiT0lYRFJHcVZBY2tJNXJSR2E0RTZwbyJ9LCJ4bXNfdGNkdCI6MTQ1MjYxOTE2MX0.fOXgC1xtpat-57xsVYkCchtMbHxOYoobHX4jEaVAWClzydI-cDsCyBMy7H1avFQnItQngYKmx2HIMLQWUQS45LA7kk_H3GLPh55EEY9XFIz9esqw8QntVZnMMDGCKy5KGVZ8MSgsX556Gh32VVdAnAoCvJi66S3Zyyq6QRWe2EOeLW0xc--Mw2cpflyOLWoCIGciHj8AjNfYF_xtJzzIEXo9aVz_6l2mOlVNi9UX5yNNLbQmMLCpg9LHTPm-c_2KTzdCX-BP10lZsUMc6Q2fNOu677k_chZSRj-CykRy9N_tYGWro3q-VPzD7-ffQZ0nhLcrue903SSA00j6c2W3Jw")
        #user_details.uid = 1900
        if "givenName" in graph_response:
            user_details.userName=graph_response["givenName"]
            user_details.uid=graph_response["id"]
        return (user_details)
    except Exception as e:
        print (e)
        user_details.userName=""
        return (user_details)   

def get_access_token(request):
    '''
    print("Fetching token")
    json_object_string = Path(os.path.join(os.path.dirname(__file__),'access_token.json')).read_text()
    json_object = json.loads(json_object_string)    
    access_token = json_object[0]["access_token"]
    print("access token: "+access_token)
    return access_token
    '''
    auth_url = str(request.build_absolute_uri())+".auth/me"
    print("URL TO CALL"+auth_url)
    cookie = request.COOKIES.get("AppServiceAuthSession")
    try:
        response = requests.get(auth_url,cookies=cookie)
        auth_json = response.json()
        if response.ok:        
            print(auth_json)
        else:    
        
            if "error" in auth_json:
                print(auth_json["error"]["code"])        
            print (response.status_code)
        return auth_json
    except Exception as e:
        print ("Inside exception token")
        print (e)

def call_graph(access_token):
    response = requests.get("https://graph.microsoft.com/v1.0/me",headers={'Authorization': 'Bearer '+ access_token})
    graph_json = response.json()
    if response.ok:        
        print(graph_json)
    else:    
    
        if "error" in graph_json:
            print(graph_json["error"]["code"])        
        print (response.status_code)
    return graph_json
    
