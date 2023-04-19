#from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
#import json
#from time import sleep
#import os
#import random
from .models import UserDetails

import requests
from django.conf import settings


def fetch_supplier(scac_duns, search_by):
    print('Fetch Supplier using '+search_by + ' Number :'+scac_duns)
    if (search_by == 'SCAC'):
        url_p2 = '/cls/supplier/bySCAC/'
    elif (search_by == 'DUNS'):
        url_p2 = '/cls/supplier/byDUNS/'
    else:
        print('Invalid search Option '+search_by)
        return_dict = {"statusCode": 999,
                       "statusDesc": 'Invalid search by Option '+search_by
                       }
        return return_dict

    clsHostanme = settings.CLS_HOST_NAME
    ClsApikey = settings.CLS_API_KEY
    ClsVerify = eval(settings.CLS_VERIFY)

    url = 'https://{}{}{}'.format(clsHostanme, url_p2, scac_duns)
    print("Fetch Supplier URL : "+url)
    req_header = {"X-Api-Key": ClsApikey}
    try:
        response = requests.get(url, headers=req_header, verify=ClsVerify)
        print('Fetch Supplier API Call')
        # print(response.json())
        # 200: Successfully processed and supplier JSON is included in the response.
        # 204: Successfully processed but the supplier was not found.
        # 400: Invalid or blank SCAC/DUNS value.
        # 401: Unauthenticated request or authentication failure.

        if (response.status_code == 200):
            try:
                response_dict = response.json()
                return_dict = {"statusCode": 200,
                               "statusDesc": "Successfully processed and supplier JSON is included in the response.",
                               "erpNumber": response_dict['erpNumber'],
                               "j1Id": response_dict['j1Id'],
                               "apexSupplierNumber": response_dict['apexSupplierNumber']
                               }

            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in while parsing the Status code 200 response - "+str(e)
                               }
        elif (response.status_code == 204):
            try:
                return_dict = {"statusCode": 204,
                               "statusDesc": "Successfully processed but the supplier was not found."
                               }
            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in while parsing the Status code 204 response - "+str(e)
                               }
        elif (response.status_code == 400):

            try:
                return_dict = {"statusCode": 400,
                               "statusDesc": "Invalid or blank SCAC/DUNS value."
                               }
                print(response.json())
            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in while parsing the Status code 400 response - "+str(e)
                               }
        elif (response.status_code == 401):

            try:
                return_dict = {"statusCode": 401,
                               "statusDesc": "Unauthenticated request or authentication failure."
                               }
                print(response.json())
            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in while parsing the Status code 401 response - "+str(e)
                               }
        else:
            try:
                return_dict = {"statusCode":  response.status_code,
                           "statusDesc": "Invalid FETCH SUPPLIER API response "+str(response.json()) 
                           }
            except Exception as e:
                return_dict = {"statusCode": 999,
                           "statusDesc": "Invalid FETCH SUPPLIER API response"+str(e)
                           }
    except Exception as e:
        return_dict = {"statusCode": 999,
                       "statusDesc": "Exception while Calling FETCH SUPPLIER API - "+str(e)
                       }
    return return_dict


def create_supplier(company_name, scac, duns, first_name, last_name, work_email):
    print('Calling Create Supplier API for :' + company_name)

    try:
        clsHostanme = settings.CLS_HOST_NAME
        ClsApikey = settings.CLS_API_KEY
        ClsVerify = eval(settings.CLS_VERIFY)

        url_p2 = '/cls/supplier'
        url = 'https://{}{}'.format(clsHostanme, url_p2)
        print("Create Supplier URL : "+url)
        req_header = {"X-Api-Key": ClsApikey}
        req_body = {
            "companyName": company_name,
            "scac": scac,
            "duns": duns,
            "adminFirstName": first_name,
            "adminLastName": last_name,
            "adminEmail": work_email
        }

        response = requests.post(
            url, json=req_body, headers=req_header, verify=ClsVerify)
        print('Create Supplier API Call')
        # print(response.json())

        # 200: Successfully processed, JSON follows
        # 400: Validation error, response includes description of error.
        # 401: Unauthenticated request or authentication failure

        # SUCCESSFUL RESPONSE EXAMPLE
        #     {
        #         "success": true,
        #         "erpNumber": "cls_12321",
        #         "j1Id": "3212321"
        #     }
        #     UNSUCCESSFUL RESPONSE EXAMPLE
        #     {
        #         "success": false,
        #         "errorDetails": "Invalid or blank admin email address."
        #     }

        if (response.status_code == 200):
            try:
                response_dict = response.json()
                return_dict = {"statusCode": 200,
                               "statusDesc": "Successfully processed, JSON follows",
                               "success": response_dict['success'],
                               "erpNumber": response_dict['erpNumber'],
                               "j1Id": response_dict['j1Id']
                               }

            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in Cleate Supplier API call while parsing the Status code 200 response - "+str(e)
                               }
        elif (response.status_code == 400):
            try:
                response_dict = response.json()
                return_dict = {"statusCode": 400,
                               "statusDesc": "Validation error, response includes description of error.",
                               "success": response_dict['success'],
                               "errorDetails": response_dict['errorDetails']
                               }
            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in Cleate Supplier API call while parsing the Status code 400 response - "+str(e)
                               }
        elif (response.status_code == 401):
            try:
                return_dict = {"statusCode": 401,
                               "statusDesc": "Unauthenticated request or authentication failure."
                               }
            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in Cleate Supplier API call while parsing the Status code 401 response - "+str(e)
                               }
        else:
            try:
                return_dict = {"statusCode":  response.status_code,
                           "statusDesc": "Invalid CREATE SUPPLIER API response "+str(response.json()) 
                           }
            except Exception as e:
                return_dict = {"statusCode": 999,
                           "statusDesc": "Invalid CREATE SUPPLIER API response"+str(e)
                           }
    except Exception as e:
        return_dict = {"statusCode": 999,
                       "statusDesc": "Exception while Calling CREATE SUPPLIER API - "+str(e)
                       }
    return return_dict


def create_supuser_upsert(erpNumber, j1Id, active, first_name, last_name, work_email):
    print('Call Supplier User upsert for erpNumber :' +
          erpNumber + ' and j1Id :'+j1Id)

    try:
        clsHostanme = settings.CLS_HOST_NAME
        ClsApikey = settings.CLS_API_KEY
        ClsVerify = eval(settings.CLS_VERIFY)

        url_p2 = '/cls/supplier/user'
        url = 'https://{}{}'.format(clsHostanme, url_p2)
        print("Supplier User Upsert URL : "+url)
        req_header = {"X-Api-Key": ClsApikey}

        req_body = {
            "erpNumber": erpNumber,
            "j1Id": j1Id,
            "active": active,
            "userFirstName": first_name,
            "userLastName": last_name,
            "userEmail": work_email
        }

        response = requests.post(
            url, json=req_body, headers=req_header, verify=ClsVerify)
        print('Supplier User upsert API Call -->')
        # print(response.json())

        # 204: Successfully processed – no response
        # 400: Validation error, response includes description of error.
        # 401: Unauthenticated request or authentication failure

        # SUCCESSFUL RESPONSE EXAMPLE
        # Response will be blank.
        # UNSUCCESSFUL RESPONSE EXAMPLE
        # {
        #     "errorDetails": "Cannot deactivate user that is not associated with the supplier. "
        # }

        if (response.status_code == 204):
            try:
                return_dict = {"statusCode": 204,
                               "statusDesc": "Successfully processed – no response"
                               }
            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in User upsert API call while parsing the Status code 200 response - "+str(e)
                               }
        elif (response.status_code == 400):
            try:
                response_dict = response.json()
                return_dict = {"statusCode": 400,
                               "statusDesc": "Validation error, response includes description of error.",
                               "errorDetails": response_dict['errorDetails']
                               }
            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in User upsert API call while parsing the Status code 400 response - "+str(e)
                               }
        elif (response.status_code == 401):
            try:
                return_dict = {"statusCode": 401,
                               "statusDesc": "Unauthenticated request or authentication failure."
                               }
            except Exception as e:
                return_dict = {"statusCode": 999,
                               "statusDesc": "Exception in User upsert API call while parsing the Status code 401 response - "+str(e)
                               }
        else:
            try:
                return_dict = {"statusCode":  response.status_code,
                           "statusDesc": "Invalid User upsert API response "+str(response.json()) 
                           }
            except Exception as e:
                return_dict = {"statusCode": 999,
                           "statusDesc": "Invalid User upsert API response"+str(e)
                           }
    except Exception as e:
        return_dict = {"statusCode": 999,
                       "statusDesc": "Exception while Calling USER UPSERT API - "+str(e)
                       }
    return return_dict

# Fetch Supplier Wrapper to be called from views passing UserDetails model


def fetch_supplier_wrapper(user_details):
    clserpNum = ""
    clsj1Id = ""
    statusCode = 999
    statusMessage = ""

    # Call CLS API Start
    try:
        # Call Fetch supplier to check if supplier exists in CLS
        fsapi_response = fetch_supplier(user_details.scac, 'SCAC')
        print('Fetch Supplier API Response')
        print(fsapi_response)
        statusCode = fsapi_response['statusCode']

        if (fsapi_response['statusCode'] == 204):
            # Successfully processed but the supplier was not found.
            print(fsapi_response["statusDesc"])
            # Call Create Supplier
            try:
                csapi_response = create_supplier(user_details.company, user_details.scac, user_details.duns,
                                                 user_details.firstname, user_details.lastname, user_details.workEmail)
                print('Create Supplier API Response ')
                print(csapi_response)
                statusCode = csapi_response['statusCode']
                if (csapi_response['statusCode'] == 200):
                    # create_supplier success
                    clserpNum = csapi_response['erpNumber']
                    clsj1Id = csapi_response['j1Id']

                    try:
                        csuapi_response = create_supuser_upsert(
                            clserpNum, clsj1Id, user_details.firstname, user_details.lastname, user_details.workEmail)
                        statusCode = csuapi_response['statusCode']
                        print('Supplier User Upsert API Response')
                        print(csuapi_response)
                        if (csuapi_response['statusCode'] == 204):
                            # create_supuser_upsert success
                            print(csuapi_response['statusDesc'])
                        elif (csuapi_response['statusCode'] == 400):
                            # create_supuser_upsert validation error
                            print(csuapi_response['statusDesc'])
                            print(csuapi_response['errorDetails'])

                        else:
                            # Other exception
                            print(csuapi_response['statusDesc'])
                    except Exception as e:
                        print(
                            "Exception while calling CLS API Supplier User Upsert - " + str(e))
                elif (csapi_response['statusCode'] == 400):
                    # Validation Error
                    print(csapi_response['statusDesc'])
                    print(csapi_response['errorDetails'])
                else:
                    # Other exception
                    print(csapi_response['statusCode'])
                    print(csapi_response['statusDesc'])
            except Exception as e:
                print("Exception while calling CLS API Create Supplier - "+str(e))

        elif (fsapi_response['statusCode'] == 200):
            # Successfully processed and supplier JSON is included in the response.
            print(fsapi_response["statusDesc"])
            print(fsapi_response['statusDesc'])
            clserpNum = fsapi_response['erpNumber']
            clsj1Id = fsapi_response['j1Id']

            # Check if Supplier is Admin in AD if yes display message saying contact your supplier Admin and STOP the process
            # Else call CLS User Upsert API as below

            # Existing Supplier but defirrent user
            try:
                csuapi_response = create_supuser_upsert(
                    clserpNum, clsj1Id, user_details.firstname, user_details.lastname, user_details.workEmail)
                print('Supplier User Upsert API Response')
                print(csuapi_response)
                statusCode = csuapi_response['statusCode']
                if (csuapi_response['statusCode'] == 204):
                    # create_supuser_upsert success
                    print(csuapi_response['statusDesc'])
                elif (csuapi_response['statusCode'] == 400):
                    # create_supuser_upsert validation error
                    print(csuapi_response['statusDesc'])
                    print(csuapi_response['errorDetails'])
                else:
                    # Other exception
                    print(csuapi_response['statusDesc'])
            except Exception as e:
                print("Exception while calling CLS API Supplier User Upsert - "+str(e))

        elif (fsapi_response['statusCode'] == 400):
            # Validation errors
            print(fsapi_response["statusDesc"])
            print(fsapi_response['errorDetails'])
        else:
            # Other exception
            print(fsapi_response['statusCode'])
            print(fsapi_response['statusDesc'])
    except Exception as e:
        print("Exception while calling CLS API Fetch Supplier - "+str(e))
        statusCode = 999
        statusMessage = "Error while checking Supplier at CLS. Please try again"
    if 200 <= statusCode <= 299:
        statusMessage = ""
    else:
        statusMessage = "Unable to call CLS API"
    return_dict = {"clserpNum": clserpNum, "clsj1Id": clsj1Id, "statusCode": statusCode, "statusMessage": statusMessage}
    print(return_dict)
    return (return_dict)
    # Call CLS API End