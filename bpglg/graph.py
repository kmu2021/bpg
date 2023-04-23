
from django.conf import settings
import json
from time import sleep
import os
import requests


G_ACCESS_TOKEN = "" #Global variable for access token
G_INVITATION_ACCESS_TOKEN = "" #Global variable for invitation access token

#Fetch Access Token
def fetch_access_token ():
    global G_ACCESS_TOKEN
    if G_ACCESS_TOKEN == "":
        G_ACCESS_TOKEN = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
    return G_ACCESS_TOKEN

#Fetch Invitation Access Token
def fetch_invitation_access_token():
    global G_INVITATION_ACCESS_TOKEN
    if G_INVITATION_ACCESS_TOKEN == "":
        G_INVITATION_ACCESS_TOKEN = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_INVITATION_CLIENT_ID), str(settings.AZURE_INVITATION_CLIENT_SECRET))
    return G_INVITATION_ACCESS_TOKEN


def get_access_token(tenant_id, client_id, client_secret):
#    global G_ACCESS_TOKEN
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
 #           G_ACCESS_TOKEN = access_token

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
    email_message_body = "Hello "+display_name + ", \r\n\r"\
        "Welcome to USPS Integrated Logistics EcoSystem (ILE) registration.\r\n\r" + \
        "Click \"Accept invitation\" link below to complete the registration process.\r\n\r" + \
        "If you have questions, please contact USPS Integrated Logistics EcoSystem (ILE) TMS Support at ILETMSSupport@usps.gov." 
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


def update_user_details(user_id, given_name, surname, company_name, bpg_grp_id, access_token, extension_attributes):
   # global G_ACCESS_TOKEN
    access_token = fetch_access_token()
    print('update_user_details user_id:'+user_id)
    print("access_token"+access_token)
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
        if bpg_grp_id != "":
            add_to_group(user_id, bpg_grp_id, access_token)
    
    
    if len(extension_attributes)>0:
        req_body = extension_attributes
        response = requests.patch(url, json=req_body, headers=req_header)
        print('Updating Extension Attribute')
        print(response)
        if (response.status_code < 200 or response.status_code > 229):
            print('Extension Attribute Update Fail')
        try:
            print(response.json())
        except Exception as e:
            print('Exception while parsing JSON')

    return 'User Attributes Updated'

def get_bpg_group_id (BPG_GRP_NAME,access_token):
    url = 'https://graph.microsoft.com/v1.0/groups'
    req_params = {'$select': 'id', '$filter': 'displayName eq \''+BPG_GRP_NAME+'\''}
    req_header = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, params=req_params, headers=req_header)
    response_json = response.json()
    bpg_grp_id = ''
    if not response.ok:
        if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)
    else:
        print('Group Check Result')
        print(response_json)
        try:
            bpg_grp_id = response_json['value'][0]['id']

        except Exception as e:
            bpg_grp_id = ''

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
        except Exception as e:
            print('Exception while parsing JSON')

        '''if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)'''
        return 'Error in Adding User to Group'
    else:
        print('Group Add Pass')
    return 'Added to Group'

#Check if User Exists or Not
def does_user_exists(user_details):
    access_token = fetch_access_token()
    #if access_token == "":
     #   access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
        

    user_id = get_user_id(user_details.workEmail, access_token)
    if user_id != '':
        print('User ID is '+ str(user_id))
        user_details.responseText = 'User is already registered'
        user_details.user_id = user_id
    return user_details

#Send Invitation to User - Wrapper Function
def send_invitation_to_user(user_details):
    access_token = fetch_invitation_access_token()
  #  if access_token == "":
   #     access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_INVITATION_CLIENT_ID), str(settings.AZURE_INVITATION_CLIENT_SECRET))
    redirectUrl = settings.WEBSITE_URL
    user_details.user_id = invite_user(user_details.workEmail, user_details.firstName +
                                               ' '+user_details.lastName,  redirectUrl, access_token)
    if (user_details.user_id==''):
        user_details.responseText = 'User Invitation Failed. Please contact administrator.'
    return user_details

#Get List of Groups IDs
def get_group_id_list(group_name_list = None):
   # global G_ACCESS_TOKEN
    access_token = fetch_access_token()

    groups_list = []
    group_search_string = ""
    url = 'https://graph.microsoft.com/v1.0/groups'
    select='id'

   # if access_token == "":
    #    access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
    if group_name_list is None:
        with open(os.path.join(os.path.dirname(__file__),'config/groups.json'),'r') as group_file:
            parsed_json = json.load(group_file)
        group_search_string = ""
        for group_name in parsed_json[settings.ENVIRONMENT]:
            group_search_string = group_search_string + '"displayName:' + group_name + '" OR '
    else:
        for group_name in group_name_list:
            group_search_string = group_search_string + '"displayName:' + group_name + '" OR '

    if group_search_string != "":
        group_search_string = group_search_string.rstrip(' OR ')
    

    req_params = {'$select': select, '$search': group_search_string, '$count': 'true'}
    print(req_params)
        
    req_header = {'Authorization': 'Bearer ' + access_token, 'ConsistencyLevel': 'Eventual'}
    response = requests.get(url, params=req_params, headers=req_header)
    response_json = response.json()
    #print(response_json['value'])
    if not response.ok:
        if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)
    else:
        for groups in response_json['value']:
            try:            
                print(groups['id'])
                groups_list.append(groups['id'])
            except Exception as e:
                print("EXCEPTION PARSING RESPONSE")            
                print (e)    
    return groups_list


#Add Groups to User
def add_groups_to_user(user_id,group_id_list):
   # global G_ACCESS_TOKEN
    access_token = fetch_access_token()
     
    url = 'https://graph.microsoft.com/v1.0/groups/{}/members/$ref'
    

   # if access_token == "":
    #    access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
    
    req_header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + access_token}
    
    message = ""
    
    for idx in range(len(group_id_list)):
        post_url = url.format(group_id_list[idx])
        req_body = {
            "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/{}".format(user_id)
            }
        print(req_body)
        for ctr in range(5):
            response = requests.post(post_url, data=json.dumps(req_body), headers=req_header)   
            print(ctr)
            print(int(response.status_code) )
            if (int(response.status_code) == 204 or int(response.status_code) == 400 ):
                print('Assigning Group Passed')
                break         
            else:
                message='Group Addition Failed'                
                try:
                    print(response.json())
                except Exception as e:
                    message='Exception while parsing JSON'
                    print(message)
                sleep(2)                     
    return 'Groups Assigned'
    
#Check if User is Active
def get_user_status(user_id):   
   # global G_ACCESS_TOKEN
    access_token = fetch_access_token()

 #   if access_token == "":
  #     access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
    account_enabled = False

    url = 'https://graph.microsoft.com/v1.0/users'
    req_params = {'$select': 'accountEnabled', '$filter': 'id eq \''+user_id+'\''}
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
            account_enabled = response_json['value'][0]['accountEnabled']
        except Exception as e:
            print(e)
            account_enabled = False
    return account_enabled

#set user status
def set_user_status(user_id, user_status):   
   # global G_ACCESS_TOKEN
    access_token = fetch_access_token()

  #  if access_token == "":
   #    access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
    #account_enabled = False

    url = 'https://graph.microsoft.com/v1.0/users/'+user_id

    req_body = {
        "accountEnabled": user_status
    }
    print (req_body)

    req_header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + access_token}
    response = requests.patch(url, json=req_body, headers=req_header)

    
    print(response.status_code)   
    
    if (response.status_code < 200 or response.status_code > 229):
        print('User Update Fail')
        try:
            print(response.json())
        except Exception as e:
            print('Exception while parsing JSON')
        return False
    else:
        print('User Update Pass')
        return True

def init_user_access_control(list_form_initial, user_id):
    user_group_name_list = fetch_user_groups(user_id)
    print(user_group_name_list)
    for records in list_form_initial:
        print(records)
        if records['data-group-name'] in user_group_name_list:
            records['fieldValue']=True
            records['data-group-initial-status']="True"
    return list_form_initial

def groups_assign_to_user (groups_to_add,user_id):
    if len(groups_to_add):
        add_groups_to_user(user_id,get_group_id_list(groups_to_add))

def groups_unassign_to_user (groups_to_remove,user_id):
    print(get_group_id_list(groups_to_remove))    
    if len(groups_to_remove):
        remove_groups_from_user(user_id,get_group_id_list(groups_to_remove))

#Fetch Groups for an user
def fetch_user_groups(user_id):
    #global G_ACCESS_TOKEN
    access_token = fetch_access_token()
     
    url = 'https://graph.microsoft.com/v1.0/users/{}/memberOf?$select=id,displayName'.format(user_id)
    
    
   
   # if access_token == "":
    #    access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
    
    req_header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + access_token}
    
    response = requests.get(url, headers=req_header)
    response_json = response.json()
    group_name_list = []

    if not response.ok:
        if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)
    else:
        for groups in response_json['value']:
            try:                            
                group_name_list.append(groups['displayName'])
            except Exception as e:
                print("EXCEPTION PARSING RESPONSE")            
                print (e)  

    return group_name_list
    

#Remove Groups From User
def remove_groups_from_user(user_id,group_id_list):
    #global G_ACCESS_TOKEN
    access_token = fetch_access_token()
     
    url = 'https://graph.microsoft.com/v1.0/groups/{}/members/{}/$ref'
    

   # if access_token == "":
    #    access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
    
    req_header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + access_token}
    
    message = ""
    print("inside Remove groups")
    print(group_id_list)
    for idx in range(len(group_id_list)):
        del_url = url.format(group_id_list[idx],user_id)
       
        print("delurl: "+del_url)
        response = requests.delete(del_url, headers=req_header)   
        
        print(int(response.status_code) )
        if (int(response.status_code) == 204 or int(response.status_code) == 400 ):
            print('Group Removed')
            #break         
        else:
            message='Group Removal Failed'                
            try:
                print(response.json())
            except Exception as e:
                message='Exception while parsing JSON'
                print(message)
                                    
    return 'Groups Removed' 

#Create a Supplier Group and return ID   
def create_supplier_group (group_name, group_description):
    #global G_ACCESS_TOKEN
    access_token = fetch_access_token()
     
    url = 'https://graph.microsoft.com/v1.0/groups'
    group_id = ""
    

   # if access_token == "":
    #    access_token = get_access_token(str(settings.AZURE_TENANT_ID), str( settings.AZURE_CLIENT_ID), str(settings.AZURE_CLIENT_SECRET))
    
    req_header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + access_token}
    
    req_body = {
        "description": json.dumps(group_description),
        "displayName": group_name,
        "mailEnabled": False,
        "groupTypes": [
    ],
    "mailNickname": group_name,
    "securityEnabled": True
    }
    print('req_body: ')
    print(req_body)
    response = requests.post(url, json=req_body, headers=req_header)

    response_json = response.json()

    print(response_json)
    if not response.ok:
        print('Group Creation Failed')
        if "error" in response_json:
            print(response_json["error"]["code"])
            print(response.status_code)
    else:
        print('Group Creation Success')
        print(response_json)
        try:
            group_id = response_json['id']
        except Exception as e:
            group_id = ''
    return group_id
    

#Create a Supplier Group    
def get_supplier_group_id (group_name, group_description):
    print('calling get_group_id_list: '+group_name)
        
    supplier_group_id_list = get_group_id_list([group_name]) 
    if len(supplier_group_id_list) == 0:
        supplier_group_id = create_supplier_group (group_name,group_description)
    else:
        supplier_group_id = supplier_group_id_list[0]
    print("supplier_group_id="+str(supplier_group_id))
    return supplier_group_id
