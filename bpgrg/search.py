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


def search_users(email,display_name,company_name,invitation_status):

    BPG_GRP_NAME="NAT_AZURE_BPG_ILE_USR_DEV"#will be read from Env later
    bpg_grp_id = ""
    response_body = []
    access_token = ""
    invitation_count = 0
    
    if access_token == "":
        access_token = get_access_token(str(settings.AZURE_TENANT_ID), str(
            settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
        print(access_token)

    if bpg_grp_id == "":
        bpg_grp_id = get_bpg_group_id (BPG_GRP_NAME,access_token)
        print('bpg_grp_id: '+bpg_grp_id)
        #return response_body
    users_list = list_users (email,display_name,company_name,invitation_status,access_token)    
    return users_list


def list_users(email,display_name,company_name,invitation_status,access_token):
    users_list = []
    url = 'https://graph.microsoft.com/v1.0/users'
    select='id,surname,givenName,companyName,mail,externalUserState,extension_9026d427583e4950bf6071088d21aefd_ILERPT_Session_UserID,extension_fe10b6b46b9f4cb68747ccf08f83782a_ILE_Alternate_UserID_1'
    filter = "userType eq 'Guest'"
    print("display_name"+display_name)
    print("email"+email)

    if display_name != "":
        filter+=" and startswith(displayName,'"+display_name+"')"
    if email !="":
        filter+=" and startswith(mail,'"+email+"')"
    if company_name != "":
        filter+=" and startswith(companyName,'"+company_name+"')"
    if invitation_status != "":
        filter+=" and externalUserState eq '"+invitation_status+"'"  

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
                    user_details.uid = user['id']
                    user_details.firstName = user['givenName']
                    user_details.lastName = user['surname']
                    user_details.email = user['mail']
                    user_details.company = user['companyName']
                    user_details.invitationStatus = user['externalUserState']
                   # user_details.supplierId = user['supplierId']
                    users_list.append(user_details)
            except Exception as e:
                print("EXCEPTION PARSING RESPONSE")            
                print (e)        
    return users_list
