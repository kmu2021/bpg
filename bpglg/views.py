from plistlib import UID
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
import os
from pathlib import Path
import json
import requests
from django.shortcuts import render
from datetime import datetime
import base64

import time
from rest_framework.response import Response
from .uspsOtp import *
from .uspsMail import *

from .search import search_users
from .models import RegistrationForm, UserDetails, EmailDetail
from .graph import does_user_exists, send_invitation_to_user


# Global Variables
OTP_COUNTER = 0


# Logout Function


def logout(request):
    # Redirect to the logout endpoint of Azure Web
    print("Logout Initiated")
    return HttpResponseRedirect("/.auth/logout")

# Search Function


def search(request):
    # Redirect to the Search Page
    print("Redirecting to Search Page")
    context = {}
    users_list = []
    if request.method == 'POST':
        # displayName = request.
        display_name = request.POST['srchDisplayName']
        email = request.POST['srchEmail']
        company_name = request.POST['srchCompanyName']
        invitation_status = request.POST.get('srchInvitationStatus', '')
        #user_details = UserDetails()
        users_list = search_users(
            email, display_name, company_name, invitation_status)
        print("CONTEXT****")
        # print(context['users_list'][0].uid)

        return render(request, "bpgrgsearch.html", {"users_list": users_list})
    else:
        return render(request, "bpgrgsearch.html", context)

# Main Init Function


def init(request):
    
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
            

            #If twoFactorCode is NOT present in request, check if user exists
            if (not 'twoFactorCode' in request.POST):     
                print("Checking uid")   
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
                        user_details=send_invitation_to_user (user_details)
                        response_message['invitation_message'] = "An invitation has been sent to " + user_details.workEmail + ".\nPlease check your mails and Accept the invitation."                        
                        del request.session['OTP_COUNTER']
                        del request.session['OTP']
                        del request.session['OTP_EXPIRES_AT']
                        return render(request, 'bpglgindex.html', {'form': form,  'display_main_form': 'hidden', 'otp_flag': 'N',"response_message":response_message})
                    else:
                        response_message = {"error_twoFactorCode":validate_otp_result}
            else:
                #Generate OTP  
                request = generate_otp_wrapper(request)
                #Send Email
                email_to_arr=[{"address": user_details.workEmail,"displayName": user_details.firstName + " " + user_details.lastName}]
                email_subject = "One Time Code for Logistics Gateway Registration"
                email_plain_text = "Please use following One Time Code for registering: " + request.session['OTP']
                email_html_text = get_otp_html(user_details.firstName + " " + user_details.lastName,otp)#"<html><head><title>OTP</title></head><body><h2>Please use following One Time Code for registering: " + request.session['OTP'] + "</h2><h3>Note: The Code is valid for " + str(int(OTP_EXPIRATION_SECONDS/60)) + " minutes</h3></body></html>"
                send_email_wrapper(email_from="", email_to_arr=email_to_arr, email_subject=email_subject, email_plain_text=email_plain_text, email_html_text=email_html_text)
            return render(request, 'bpglgindex.html', {'form': form, 'otp_flag': 'Y', 'otp':  request.session['OTP'], 'display_main_form': 'hidden', 'otp_validated_flag': otp_validated_flag,"response_message":response_message})
            # return HttpResponseRedirect('/thanks/')


def generateotp(request):
    print(request.method)
    if request.method == 'POST':   
        #Generate OTP  
        request = generate_otp_wrapper(request)
        #Send Email     
        email_to_arr=[{"address": request.POST['workEmail'],"displayName": request.POST['displayName']}]
        email_subject = "One Time Code for Logistics Gateway Registration"
        email_plain_text = "Please use following One Time Code for registering: " + request.session['OTP']
        email_html_text = get_otp_html(request.POST['displayName'],request.session['OTP'])#"<html><head><title>OTP</title></head><body><h2>Please use following One Time Code for registering: " + request.session['OTP'] + "</h2><h3>Note: The Code is valid for " + str(int(OTP_EXPIRATION_SECONDS/60)) + " minutes</h3></body></html>"
        send_email_wrapper(email_from="", email_to_arr=email_to_arr, email_subject=email_subject, email_plain_text=email_plain_text, email_html_text=email_html_text)            
        return HttpResponse('Test OTP: '+request.session['OTP'],status=200)

def testemail(request):
    response_text = ""
    if request.method == 'POST':
        #print(request.POST['url'])
        #print(request.POST['postheader'])
        print(request.POST['postbody'])
        #url = request.POST['url']
        payload = json.loads(request.POST['postbody'])
        print("Body Loaded")
        #headers = json.loads(request.POST['postheader'])
        #print("Header Loaded")
        #Send Email
        response_text=send_email(message=payload, debug_flag=True)
        if (response_text==""):
            response_text="Mail Sent"
    return render(request, 'testemail.html',{'response_text':response_text})

        
    