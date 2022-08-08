from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import UserDetails
from django.conf import settings
import json
from time import sleep
import os

import requests

# Main Init Function


def init(request):
    return HttpResponse("return this string")

    # Main Init Function


@csrf_exempt
def process(request):
    print(request.scheme)
    print("Welcome")
    if request.method == "GET":
        return HttpResponse('UNSUPPORTED ACTION')
    elif request.method == "POST":
        users = json.loads(request.body)
        response_body = []
        access_token = ""
        invitation_count = 0
        for user in users:
            user_details = UserDetails()
            user_details.uid = user['uid']
            user_details.firstName = user['firstName']
            user_details.lastName = user['lastName']
            user_details.email = user['email']
            user_details.company = user['company']
            user_details.supplierId = user['supplierId']
            user_details.responseText = ''
            print(response_body)

            if access_token == "":
                access_token = get_access_token(str(settings.AZURE_TENANT_ID), str(
                    settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
                print(access_token)
            user_id = get_user_id(user_details.email, access_token)
            if user_id != '':
                user_details.responseText = 'User already Exists'
                user_details.user_id = user_id
            else:
                user_details.user_id = invite_user(user_details.email, user_details.firstName +
                                                ' '+user_details.lastName, request.scheme + "://" + os.environ.get('WEBSITE_HOSTNAME'), access_token)
                if user_details.user_id != '':
                    invitation_count = invitation_count + 1

            response_body.append(vars(user_details))

        if invitation_count > 0:
            print('Updating User since sucessfully sent ' +
                str(invitation_count)+' invitations')
            sleep(60)
            print(response_body)
            i = 0
            while i < len(response_body):
                print('inside loop')
                if (response_body[i]['user_id'] != '' and response_body[i]['responseText'] == ''):
                    response_body[i]['responseText'] = update_user_details(
                        response_body[i]['user_id'], response_body[i]['firstName'], response_body[i]['lastName'], response_body[i]['company'], access_token)
                i = i + 1
        return HttpResponse(json.dumps(response_body))


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
            print(response_json["error"]["code"])
            print(response.status_code)
    else:
        print('User Check Result')
        print(response_json)
        try:
            user_id = response_json['value'][0]['id']

        except Exception as e:
            user_id = ''

    return user_id


def invite_user(email, display_name, redirect_url, access_token):
    url = 'https://graph.microsoft.com/v1.0/invitations'
    email_message_body = "Hello "+display_name + \
        ",\nWelcome to USPS Integrated Logistics EcoSystem (ILE) registration."
    req_body = {
        "invitedUserEmailAddress": email,
        "invitedUserDisplayName": display_name,
        "inviteRedirectUrl": redirect_url,
        "sendInvitationMessage": True,
        "invitedUserMessageInfo": {
            "customizedMessageBody": email_message_body
        }
    }
    print(req_body)
    req_header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + access_token}
    response = requests.post(url, json=req_body, headers=req_header)
    print(requests)
    response_json = response.json()
    user_id = ''
    print('Invitation Result')
    print(response_json)
    if not response.ok:
        print('Invitation Fail')
        if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)
    else:
        print('Invitation Pass')
        print(response_json)
        try:
            user_id = response_json['invitedUser']['id']
        except Exception as e:
            user_id = ''

    return user_id


def update_user_details(user_id, given_name, surname, company_name, access_token):
    print('update_user_details user_id:'+user_id)
    url = 'https://graph.microsoft.com/v1.0/users/'+user_id

    req_body = {
        "givenName": given_name,
        "surname": surname,
        "companyName": company_name
    }

    req_header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + access_token}
    response = requests.patch(url, json=req_body, headers=req_header)
    print('Sent Data')
    print(response)

    print('User Update Result')
    if (response.status_code < 200 or response.status_code > 229):
        print('User Update Fail')
        try:
            print(response.json())
        except Exception as e:
            print('Exception while parsing JSON')

        '''if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)'''
        return 'Error in Updating User'
    else:
        print('User Update Pass')
    return ''
