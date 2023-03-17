from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .graph import get_access_token, get_bpg_group_id
from .models import UserDetails
from django.conf import settings
import json
from time import sleep
import os
import random

import requests

# Process Form data


def search_users(UserDetails):

    response_body = []
    access_token = ""
    invitation_count = 0
    
    if access_token == "":
        access_token = get_access_token(str(settings.AZURE_TENANT_ID), str(
            settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
        print(access_token)

        #return response_body
    users_list = list_users (email = UserDetails.workEmail,firstName=UserDetails.firstName,lastName=UserDetails.lastName,company=UserDetails.company, scac=UserDetails.scac, duns=UserDetails.duns,invitationStatus=UserDetails.invitationStatus,access_token=access_token)    
    return users_list


def list_users(email,firstName,lastName,company, scac,duns,invitationStatus,access_token):
    users_list = []
    url = 'https://graph.microsoft.com/v1.0/users'
    select='id,surname,givenName,displayName,companyName,mail,externalUserState'
    filter = "userType eq 'Guest'"


    if firstName != "":
        filter+=" and startswith(displayName,'"+firstName+"')"
    if lastName != "":
        filter+=" and startswith(surname,'"+lastName+"')"
    if email !="":
        filter+=" and startswith(mail,'"+email+"')"
    if company != "":
        filter+=" and startswith(companyName,'"+company+"')"
    if invitationStatus != "":
        filter+=" and externalUserState eq '"+invitationStatus+"'"  

    req_params = {'$select': select, '$filter': filter, '$count': 'true'}
    print(req_params)
    #req_header = {'ConsistencyLevel': 'Eventual'}
    req_header = {'Authorization': 'Bearer ' + access_token, 'ConsistencyLevel': 'Eventual'}
    response = requests.get(url, params=req_params, headers=req_header)
    response_json = response.json()
    
    if not response.ok:
        if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)
    else:
        print('User Check Result')
        print(response_json)  
        for user in response_json['value']:
            try:
                #users = json.loads(response_json)
            
                    print(user['id'])
                    user_details = UserDetails()    
                    user_details.user_id = user['id']
                    user_details.firstName = user['givenName']
                    if user_details.firstName == None:
                        user_details.firstName = user['displayName'].split()[0:][0]
                    user_details.lastName = user['surname']
                    if user_details.lastName == None:
                        user_details.lastName = user['displayName'].split()[-1:][0]
                    user_details.workEmail = user['mail']
                    user_details.company = user['companyName']
                    user_details.invitationStatus = user['externalUserState']
                    user_details.scac = "ABCD"
                    user_details.duns = "12345678"
                   # user_details.supplierId = user['supplierId']
                    users_list.append(user_details)
            except Exception as e:
                print("EXCEPTION PARSING RESPONSE")            
                print (e)        
    return users_list
