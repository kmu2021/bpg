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
import pyotp
from rest_framework.response import Response

from .search import search_users
from .models import RegistrationForm, UserDetails, EmailDetail
from .graph import processForm




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
        #displayName = request.
        display_name=request.POST['srchDisplayName']
        email=request.POST['srchEmail']
        company_name = request.POST['srchCompanyName']
        invitation_status = request.POST.get('srchInvitationStatus','')
        #user_details = UserDetails()      
        users_list =search_users(email,display_name,company_name, invitation_status)
        print("CONTEXT****")
        #print(context['users_list'][0].uid)

        return render(request, "bpgrgsearch.html", {"users_list":users_list})
    else:
        return render(request, "bpgrgsearch.html", context)

# Main Init Function
def init(request):
    # if this is a GET request present a Blank Form
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'bpglgindex.html',{'form': form})
    
    # if this is a POST request we need to process the form data
    elif request.method == 'POST':
        print(request.POST)
        print("POST Printed")
        form = RegistrationForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user_details = {
                        "uid": "",
                        "firstName": form.cleaned_data['firstName'].strip(),
                        "lastName": form.cleaned_data['lastName'].strip(),
                        "workEmail": form.cleaned_data['workEmail'].strip(),
                        "company": form.cleaned_data['company'].strip(),
                        "responseText": ""
                    }
            print(user_details);

            otp_validated_flag = 'N'          
            otp = ""
            if (request.POST.get('twoFactorCode',False)):
                if (OTPFeatures.verifyOTP(user_details['workEmail'],request.POST['twoFactorCode'])):
                    otp_validated_flag = 'Y'
                    return HttpResponse("<H1>OTP has been validated</H1>")
                else:
                    otp_validated_flag = 'N'
            else:
                otp=OTPFeatures.getOTP(user_details['workEmail'])

            return render(request, 'bpglgindex.html',{'form': form,'otp_flag':'Y','otp':otp, 'display_main_form':'hidden','otp_validated_flag':otp_validated_flag})
            #return HttpResponseRedirect('/thanks/')

# This class returns the string needed to generate the key
class generateKey:
    #@staticmethod
    def getOtpKey(email):
        randomKey = "123456@#41354787"        
        return base64.b32encode((str(email) + str(datetime.date(datetime.now())) + randomKey).encode())

class OTPFeatures:    
    # Get to Create a call for OTP
    KEY_DURATION = 60
    @staticmethod
    def getOTP(email):
        #KEY_DURATION = 60 #in seconds
        key = generateKey.getOtpKey(email)        
        OTP = pyotp.TOTP(key,interval = OTPFeatures.KEY_DURATION)  # TOTP Model for OTP is created
        current_otp = OTP.now()
        print("Current OTP: "+ str(current_otp))
        return current_otp
    
# This Method verifies the OTP
    @staticmethod
    def verifyOTP(email, user_otp):
        
        key = generateKey.getOtpKey(email)
        OTP = pyotp.TOTP(key,interval = OTPFeatures.KEY_DURATION)  # TOTP Model 
        if OTP.verify(user_otp):
            return True
        else:
            return False