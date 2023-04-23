
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from time import sleep
import os
import random
import requests
from .uspslogger import printlog,setlogenv
import os
import traceback


def get_access_token(tenant_id, client_id, client_secret):
    
    scope = 'https://graph.microsoft.com/.default'
    grant_type = 'client_credentials'
    token_url = 'https://login.microsoftonline.com/'+tenant_id+'/oauth2/v2.0/token'
    request_header = {'Content-Type': 'application/x-www-form-urlencoded'}
    request_body = {
        "client_id": client_id,
        "grant_type": grant_type,
        "client_secret": client_secret,
        "scope": scope
    }

    response = requests.post(
        token_url, data=request_body, headers=request_header)
    access_token_json = response.json()
    access_token = ''
    if not response.ok:
        if "error" in access_token_json:
            print(access_token_json["error"]["code"])
            print(response.status_code)
    else:
        if "access_token" in access_token_json:
            access_token = access_token_json["access_token"]

    return access_token

def get_user_id(email, access_token):    
    url = 'https://graph.microsoft.com/v1.0/users'
    req_params = {'$select': 'id', '$filter': 'mail eq \''+email+'\''}
    req_header = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, params=req_params, headers=req_header)
    response_json = response.json()
    user_id = ''
    if not response.ok:
        if "error" in response_json:
            #print(response_json["error"]["code"])
            #print(response.status_code)
            printlog('errorMessage:'+response_json["error"]["code"],'ERROR')
    else:
        print('User Check Result')
        print(response_json)
        try:
            user_id = response_json['value'][0]['id']

        except Exception as e:
            errorMessage = traceback.format_exc()
            printlog('errorMessage:'+errorMessage,'ERROR')
            user_id = ''

    return user_id

def get_group_id (BPG_GRP_NAME,access_token):
    url = 'https://graph.microsoft.com/v1.0/groups'
    req_params = {'$select': 'id', '$filter': 'displayName eq \''+BPG_GRP_NAME+'\''}
    req_header = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, params=req_params, headers=req_header)
    response_json = response.json()
    bpg_grp_id = ''
    if not response.ok:
        if "error" in response_json:
            #print(response_json["error"]["code"])
            #print(response.status_code)
            printlog('errorMessage:'+response_json["error"]["code"],'ERROR')
    else:
        print('Group Check Result')
        print(response_json)
        try:
            bpg_grp_id = response_json['value'][0]['id']

        except Exception as e:
            bpg_grp_id = ''
            errorMessage = traceback.format_exc()
            printlog('errorMessage:'+errorMessage,'ERROR')

    return bpg_grp_id

def add_to_group(user_id, bpg_grp_id, access_token):
    print('Adding User to Group')
    url = 'https://graph.microsoft.com/v1.0/groups/'+bpg_grp_id+'/members/$ref'

    req_body = {
        "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/"+user_id,
    }

    req_header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + access_token}
    response = requests.post(url, json=req_body, headers=req_header)
    print('Sent Data')
    print(response)

    print('Group Update Result')
    if (response.status_code < 200 or response.status_code > 229):
        print('Add Group Failed')
        try:
            print(response.json())
            printlog('errorMessage:'+response.json(),'ERROR')
        except Exception as e:
            print('Exception while parsing JSON')
            errorMessage = traceback.format_exc()
            printlog('errorMessage:'+errorMessage,'ERROR')


        '''if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)'''
        return 'Error in Adding User to Group'
    else:
        print('Group Add Pass')
    return 'Added to Group'

def check_user_group (user_id,group_id,access_token):
    url = 'https://graph.microsoft.com/v1.0/users/'+user_id+'/checkMemberGroups'
    req_header = {'Authorization': 'Bearer ' + access_token}
    req_body = {
        "groupIds": [group_id]
    }
    response = requests.post(url, json=req_body, headers=req_header)
    response_json = response.json()
    grp_id = ''
    if not response.ok:
        if "error" in response_json:
            #print(response_json["error"]["code"])
            #print(response.status_code)
            printlog('errorMessage:'+response_json["error"]["code"],'ERROR')
    else:
        print('Group Check Result')
        print(response_json)
        try:
            grp_id = response_json['value'][0]

        except Exception as e:
            grp_id = ''
            errorMessage = traceback.format_exc()
            printlog('errorMessage:'+errorMessage,'ERROR')

    return grp_id