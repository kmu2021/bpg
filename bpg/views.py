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
    print("Logout Initiated")
    return HttpResponseRedirect("/.auth/logout")
    #https://login.microsoftonline.com/<tenantid>/oauth2/v2.0/authorize?response_type=code+id_token&client_id=<clientid>&scope=openid+profile+email&response_mode=form_post&nonce=<random>&state=redir%3D%252F

# Main Init Function
def init(request):    
    # Populate User Details    
    user_data = get_user_name (request)    

    if not hasattr(user_data, "userName") or user_data.userName=="" :
        # If User Details not available, Return to Login Page
        print("Not Authenticated. Redirecting to Login Page")
        #return render(request,'bpgtemplate.html')
        #return HttpResponseRedirect("/.auth/login/aad?post_login_redirect_uri=/")
        return HttpResponseRedirect(user_data.loginUrl)
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
            service.url = child.attrib[str((settings.ENVIRONMENT)+'url').upper()]
            service.logoutUrl = service.url + child.attrib['LOGOUTURL']
            
            # If ServiceCode (from xml) is available in User's ILE Access List, show the service
            try:
                
                for item in user_data.ileAccessList:      
                    print(item)              
                    if service.serviceCode == item.split("|")[0].upper():
                        service.accessFlag = True  
                        break          
                    else :
                        service.accessFlag = False
            except Exception as e:
                print(e)
                service.accessFlag = False
            service.pendingActivationFlag = int(os.environ.get('BPG_LINKS_DISABLED',0)) if 'BPG_LINKS_DISABLED' in os.environ else 0
            if service.pendingActivationFlag == 0:
                try:
                    for item in user_data.ileAccessList:
                        if service.serviceCode + "|" + "TRUE"==item:
                            service.pendingActivationFlag = 0
                            break
                        else:
                            service.pendingActivationFlag = 1
                except Exception as e:
                    #Do nothing since pending flag is already initialized from Environment
                    pass            
            service.id = child.attrib['id']                   
            serviceList.append(service)
        serviceList.append(user_data)    
    return render(request, 'bpgtemplate.html',{"serviceList":serviceList})
        

# Get User Details        
def get_user_name(request):
    # For Testing in Local Only. Will be removed before deployment to Prod
    '''user_details = UserDetails()
    user_details.userName = "Test"
    user_details.ileAccessList = ['FA|FALSE','ILERPT|TRUE']
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

        #Generate Login URL
        user_details.loginUrl = get_login_url (auth_response['user_claims'])
        return (user_details)
        
    except Exception as e:
        print ("get_user_name Exception")
        print (e)
        user_details.userName=""
        return (user_details)   

# Fetch Access Token for the validated user
def get_access_token(request):

    auth_url = request.scheme + "://" + os.environ.get('WEBSITE_HOSTNAME') +"/.auth/me"
    #print("AUTH URL"+auth_url)
    try:        
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
    # Call Graph API using access token
    response = requests.get("https://graph.microsoft.com/v1.0/me",headers={'Authorization': 'Bearer '+ access_token})
    graph_json = response.json()
    if not response.ok:        
        if "error" in graph_json:
            print(graph_json["error"]["code"])        
            print (response.status_code)
    return graph_json

# Generate a list of ILE claims user has access to    
def get_access_list(user_claims):
    ileAccessList=[]
    try:
        for userclaims in user_claims:
            if userclaims['typ'].startswith('ILE'):
                try:
                    appname = userclaims['val'].split("|")[0].upper()
                    appstatus = userclaims['val'].split("|")[4].upper()
                    
                except Exception as e:
                    appstatus = ""
                ileAccessList.append(appname + "|" + appstatus)
    except Exception as e:
        print ("get_access_list Exception")
        print (e)       
    return(ileAccessList)

    
# Generate a list of ILE claims user has access to    
def get_login_url(user_claims):
    base_url = "https://login.microsoftonline.com/"
    try:
        for userclaims in user_claims:
            if userclaims['typ'] == 'aud':
                client_id = userclaims['val']
            if userclaims['typ'] == 'aud':
                tenant_id = userclaims['val']
        login_url = base_url + tenant_id + "/oauth2/v2.0/authorize?response_type=code+id_token&client_id=" + client_id + "&scope=openid+profile+email&response_mode=form_post&nonce=12345678902389447837_12121123213&state=redir%3D%252F"
        print("Login URL: "+login_url)
    except Exception as e:
        print ("get_login_url Exception")
        print (e)       
    return(login_url)