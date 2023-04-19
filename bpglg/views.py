from plistlib import UID
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings



from pathlib import Path
import json

from django.shortcuts import render

from .uspsOtp import *
from .uspsMail import *

from .uspsSearch import search_users
from .models import RegistrationForm, UserDetails, UserMgmtSearchForm, UserAccessControlForm
from .graph import does_user_exists, send_invitation_to_user,update_user_details,get_group_id_list,add_groups_to_user,get_user_status, set_user_status, init_user_access_control,groups_assign_to_user, groups_unassign_to_user, fetch_user_groups, get_supplier_group_id
from .clsgraph import fetch_supplier_wrapper

#Import Custom Logger Module
from .uspslogger import printlog,setlogenv

# Logout Function


def logout(request):
    # Redirect to the logout endpoint of Azure Web
    print("Logout Initiated")
    return HttpResponseRedirect("/.auth/logout")

# Main Init Function


def init(request):
    #OPTIONAL: Set the custom Log Environment before first use. Make sure request is passed.
    setlogenv(request)
    #Call Log Function to print Log
    printlog('Logger has been activated')
    #optionally call logger with log level
    printlog('Logger has been activated in WARNING mode','WARNING')
    
    response_message = {"validation_error":"",
                        "invitation_message":""}
    # if this is a GET request present a Blank Form
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'bpglgindex.html', {'form': form})

    # if this is a POST request we need to process the form data
    elif request.method == 'POST':
        print(request.POST)
        print("POST Printed")
        form = RegistrationForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user_details = UserDetails()
            user_details.firstName = form.cleaned_data['firstName'].strip()
            user_details.lastName = form.cleaned_data['lastName'].strip()
            user_details.workEmail = form.cleaned_data['workEmail'].strip()
            user_details.company = form.cleaned_data['company'].strip()
            user_details.scac = form.cleaned_data['scac'].strip()
            user_details.duns = form.cleaned_data['duns'].strip()
            user_details.responseText=""
            user_details.user_id = ""

            request.session['PROCESSING_STATUS'] = 'PENDING'
            

            #If twoFactorCode is NOT present in request, check if user exists
            if (not 'twoFactorCode' in request.POST):                     
                request.session['OTP_COUNTER'] = '0'        
                user_details=does_user_exists (user_details)            

            if (user_details.responseText!=""):
                response_message['validation_error']=user_details.responseText
                return render(request, 'bpglgindex.html', {'form': form, "response_message":response_message})                         
               
           
            
            otp_validated_flag = 'N'
            otp = ""

            

            if request.session.get('OTP_COUNTER', False):
                request.session['OTP_COUNTER'] = str(int(request.session.get('OTP_COUNTER', False)) + 1)
                print ("Session available")             
                print(request.session['OTP_COUNTER'])      
            else:
                request.session['OTP_COUNTER'] = '1'
                print('Init Session')                                     
                print(request.session['OTP_COUNTER'])   
            
            if (request.POST.get('twoFactorCode', False)):
                print("OTP Entered by User: "+user_details.workEmail + ":" + request.POST['twoFactorCode'])
                
                
                if request.session.get('OTP', False):
                    print("OTP in SESSION")
                    print(request.session['OTP'])
                    validate_otp_result = validate_otp_wrapper(int(request.session['OTP']),int(request.POST['twoFactorCode']),int(request.session['OTP_COUNTER']),int(request.session['OTP_EXPIRES_AT']))

                    if (validate_otp_result==""):
                        otp_validated_flag = 'Y'
                        supplier_group_name=""
                        supplier_group_description = ""

                        '''supplier_result = fetch_supplier_wrapper(user_details)
                        if (supplier_result['clsj1Id'] == ""):
                            supplier_group_name = "NAT_AZURE_SUPPLIER_{}_ILE{}".format(supplier_result['clsj1Id'],settings.ENVIRONMENT)                            
                            supplier_group_description = {
                                "supplierName": user_details.company,
                                "supplierDomainName": user_details.workEmail.split('@')[1],
                                "supplierID": supplier_result['clsj1Id'],
                                "APEXID": "",
                                "SCAC": user_details.scac,
                                "DUNS": user_details.duns
                            }
                            del request.session['OTP_COUNTER']
                            del request.session['OTP']
                            del request.session['OTP_EXPIRES_AT']
                            response_message['validation_error']=supplier_result['statusMessage']
                            return render(request, 'bpglgindex.html', {'form': form, "response_message":response_message})                        
                        else:'''
                        #TEST
                        
                        jpid = 0
                        for character in user_details.company:
                            jpid = jpid + ord(character)
                        supplier_group_name = "NAT_AZURE_SUPPLIER_{}_ILE_{}".format(str(jpid),settings.ENVIRONMENT)  
                        print("supplier_group_name="+supplier_group_name)
                        supplier_group_description = {
                                "supplierName": user_details.company,
                                "supplierDomainName": user_details.workEmail.split('@')[1],
                                "supplierID": "12345",
                                "APEXID": "98765",
                                "SCAC": user_details.scac,
                                "DUNS": user_details.duns
                            }
                        #ENDTEST
                        user_details=send_invitation_to_user (user_details)
                        response_message['invitation_message'] = "An invitation has been sent to " + user_details.workEmail + ".\nPlease check your mails and Accept the invitation."                        
                        extension_attributes = {
                            "extension_a037f2abeebd4a1dbf8f8f8e0789d52f_ILERPT_Session_UserID": user_details.user_id,
                            "extension_bd7ea6b1f947459dad5a0ea3fc55cc85_ILE_Alternate_UserID_1": "ILERPT|{}|99999|{}|TRUE|678765|{}|USR|{}".format(user_details.user_id,user_details.company,settings.ENVIRONMENT,user_details.workEmail.split('@')[1])
                        }
                        print(extension_attributes)
                        if user_details.user_id != "":
                            user_details_update_response = update_user_details(user_details.user_id,user_details.firstName,user_details.lastName,user_details.company,"",None,extension_attributes)
                            print(user_details_update_response)
                            groups_list = get_group_id_list()
                            groups_list.append(get_supplier_group_id (supplier_group_name, supplier_group_description))
                               
                            
                            group_assignment_result=add_groups_to_user(user_details.user_id,groups_list)                 
                        del request.session['OTP_COUNTER']
                        del request.session['OTP']
                        del request.session['OTP_EXPIRES_AT']                        
                        request.session['PROCESSING_STATUS'] = 'COMPLETE'
                        return render(request, 'bpglgindex.html', {  'display_main_form': 'hidden', 'otp_flag': 'N',"response_message":response_message})                    
                    else:
                        response_message = {"error_twoFactorCode":validate_otp_result}
            else:
                #Generate OTP  
                request = generate_otp_wrapper(request)
                #Send Email
                email_to_arr=[{"address": user_details.workEmail,"displayName": user_details.firstName + " " + user_details.lastName}]
                email_subject = "One Time Code for Logistics Gateway Registration"
                email_plain_text = "Please use following One Time Code for registering: " + request.session['OTP']
                email_html_text = get_otp_html(user_details.firstName + " " + user_details.lastName,request.session['OTP'])#"<html><head><title>OTP</title></head><body><h2>Please use following One Time Code for registering: " + request.session['OTP'] + "</h2><h3>Note: The Code is valid for " + str(int(OTP_EXPIRATION_SECONDS/60)) + " minutes</h3></body></html>"
                send_email_wrapper(email_from="", email_to_arr=email_to_arr, email_subject=email_subject, email_plain_text=email_plain_text, email_html_text=email_html_text)                
            return render(request, 'bpglgindex.html', {'form': form, 'otp_flag': 'Y',  'display_main_form': 'hidden', 'otp_validated_flag': otp_validated_flag,"response_message":response_message})            

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def generateotp(request):
    print(request.method)
    if request.method == 'POST':
        print(request.session.get('PROCESSING_STATUS','P'))
        if (request.session.get('PROCESSING_STATUS','PENDING') == 'COMPLETE'):              
            return HttpResponse('Invitation has already been sent',content_type="text/plain",status=200)
        #Generate OTP  
        request = generate_otp_wrapper(request)
        #Send Email     
        email_to_arr=[{"address": request.POST['workEmail'],"displayName": request.POST['displayName']}]
        email_subject = "One Time Code for Logistics Gateway Registration"
        email_plain_text = "Please use following One Time Code for registering: " + request.session['OTP']
        email_html_text = get_otp_html(request.POST['displayName'],request.session['OTP'])#"<html><head><title>OTP</title></head><body><h2>Please use following One Time Code for registering: " + request.session['OTP'] + "</h2><h3>Note: The Code is valid for " + str(int(OTP_EXPIRATION_SECONDS/60)) + " minutes</h3></body></html>"
        send_email_wrapper(email_from="", email_to_arr=email_to_arr, email_subject=email_subject, email_plain_text=email_plain_text, email_html_text=email_html_text)            
        return HttpResponse('One Time Code has been resent',content_type="text/plain",status=200)

def testemail(request):
    response_text = ""
    if request.method == 'POST':
        print(request.POST['postbody'])        
        payload = json.loads(request.POST['postbody'])
        print("Body Loaded")
        #Send Email
        response_text=send_email(message=payload, debug_flag=True)
        if (response_text==""):
            response_text="Mail Sent"
    return render(request, 'testemail.html',{'response_text':response_text})

        
def usermgmt(request):
    # if this is a GET request present a Blank Form
    if request.method == 'GET':
        form = UserMgmtSearchForm()        
        return render(request, 'bpglgusermgmt.html',{'form': form})
    # if this is a POST request we need to process the form data
    elif request.method == 'POST':
        print(request.POST)        
        form = UserMgmtSearchForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("Form Valid")
            
            # process the data in form.cleaned_data as required
            user_details = UserDetails()
            user_details.firstName = form.cleaned_data['firstName'].strip()
            user_details.lastName = form.cleaned_data['lastName'].strip()
            user_details.workEmail = form.cleaned_data['workEmail'].strip()
            user_details.company = form.cleaned_data['company'].strip()
            user_details.scac = form.cleaned_data['scac'].strip()
            user_details.duns = form.cleaned_data['duns'].strip()
            user_details.invitationStatus = form.cleaned_data['pendingInvitationFlag']            
            user_details.responseText=""
            user_details.user_id = ""
            if (request.POST.get('registerUserToggle','NO')=="YES"):
                printlog("Registering User")
                user_details=does_user_exists (user_details)            
                if (user_details.responseText!=""):
                    registerUserMessage=user_details.responseText
                else:
                    user_details=send_invitation_to_user (user_details)
                    registerUserMessage = "An invitation has been sent to " + user_details.workEmail + ".\nPlease check your mails and Accept the invitation."                        
                    if user_details.user_id != "":
                        user_details_update_response = update_user_details(user_details.user_id,user_details.firstName,user_details.lastName,user_details.company,"",None)
                        groups_list = get_group_id_list()
                        group_assignment_result=add_groups_to_user(user_details.user_id,groups_list)                                   
                return render(request, "bpglgusermgmt.html", {'form': form, 'registerUserMessage':registerUserMessage})                
            else:
                users_list = search_users(user_details)
                return render(request, "bpglgusermgmt.html", {'form': form,"users_list": users_list})
                

    return render(request, 'bpglgusermgmt.html',{'form': form})

def resendinvite(request):    
    if request.method == 'POST':
        user_details = UserDetails()
        user_details.firstName = request.POST['firstName']
        user_details.lastName = request.POST['lastName']
        user_details.workEmail = request.POST['workEmail']
        user_details=send_invitation_to_user (user_details)
        response_message = "An invitation has been sent to " + user_details.workEmail + ".\nPlease check your mails and Accept the invitation."   
        return HttpResponse(response_message,content_type="text/plain",status=200)    
    
def get_user_access_control_form(request):
    if request.method == 'GET':
        form_initial = {}
        list_form_initial = []

        
        form = UserAccessControlForm()
        active_flag = get_user_status (request.GET['user_id'])
        form_initial['activeUserFlag'] = active_flag
        form['activeUserFlag'].field.widget.attrs.update({'data-group-initial-status': str(active_flag)})

        list_form_initial.append ({
            'fieldName':'activeUserFlag',
            "fieldValue": active_flag,
            'data-group-initial-status': str(active_flag),
            'data-group-name': ""            
        })

        admin_flag=False
        group_name_list=fetch_user_groups(request.GET['user_id'])        

        for fields in form:
            print(fields.name)
            if fields.name!='activeUserFlag':
                if 'data-group-name' in fields.field.widget.attrs:
                        list_form_initial.append ({
                            'fieldName':fields.name,
                            "fieldValue": False,
                            'data-group-initial-status': str(False),
                            'data-group-name': fields.field.widget.attrs['data-group-name']+'_USR_'+settings.ENVIRONMENT            
        })
                        if fields.field.widget.attrs['data-group-name']+'_ADM_'+settings.ENVIRONMENT in group_name_list:
                            admin_flag = True
                        
        list_form_initial.append ({
            'fieldName':'adminFlag',
            "fieldValue": admin_flag,
            'data-group-initial-status': str(admin_flag),
            'data-group-name': ""            
        })
        
        init_user_access_control(list_form_initial, request.GET.get('user_id'))
        for fields in list_form_initial:
            form_initial[fields['fieldName']]=fields['fieldValue']            
            form[fields['fieldName']].field.widget.attrs.update({'data-group-name': fields['data-group-name']})
            form[fields['fieldName']].field.widget.attrs.update({'data-group-initial-status': fields['data-group-initial-status']})
            #print(fields['fieldName'] + fields['data-group-name'])

        form.initial=form_initial
        
        context = {
        'form':form,"user_id":request.GET['user_id']
    }
    elif request.method == 'POST':  
        
        form = UserAccessControlForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            print("Valid Form")            
            print(request.POST.get('user_id'))
            print(form.cleaned_data)
            print (form.cleaned_data['activeUserFlag']) 
            
            set_user_status(request.POST.get('user_id'),form.cleaned_data['activeUserFlag'])
            
            groups_to_remove = []
            groups_to_add = []
           # add_groups_to_user(request.POST.get('user_id'),groups_to_add)

            adminFlag = form.cleaned_data['adminFlag']

            for fields in form:
                print(fields)
                if (fields.value()):
                    if 'data-group-name' in fields.field.widget.attrs:
                        print("init: "+ (fields.field.widget.attrs['data-group-initial-status']))
                        #if fields.field.widget.attrs['data-group-initial-status'] != "" and eval(fields.field.widget.attrs['data-group-initial-status']) == False:
                        groups_to_add.append(fields.field.widget.attrs['data-group-name']+'_USR_'+settings.ENVIRONMENT)
                        if (adminFlag):
                            groups_to_add.append(fields.field.widget.attrs['data-group-name']+'_ADM_'+settings.ENVIRONMENT)

                else:
                    if 'data-group-name' in fields.field.widget.attrs:
                        print("init2: "+ (fields.field.widget.attrs['data-group-initial-status']))
                        #if fields.field.widget.attrs['data-group-initial-status'] != "" and eval(fields.field.widget.attrs['data-group-initial-status']) == True:
                        groups_to_remove.append(fields.field.widget.attrs['data-group-name']+'_USR_'+settings.ENVIRONMENT)
                        groups_to_remove.append(fields.field.widget.attrs['data-group-name']+'_ADM_'+settings.ENVIRONMENT)
                            
            for groups in groups_to_remove:
                if (groups in groups_to_add):
                        groups_to_remove.remove(groups)
            print(groups_to_add)
            print (groups_to_remove)

            if len(groups_to_add)>0:
                groups_assign_to_user (groups_to_add,request.POST.get('user_id'))
            if len(groups_to_remove)>0:
                groups_unassign_to_user (groups_to_remove,request.POST.get('user_id'))

            context = { 'form':form }
        else:
            print(form.errors)
                                    
    return render(request, 'useraccesscontrolform.html', context)

