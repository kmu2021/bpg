from django.shortcuts import render
from django.http import JsonResponse
from supmgn.models import supplierUser, suppResp
from supmgn.serializers import SupplierUserSerializer,SuppRespSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .graphCall import get_access_token,get_user_id,get_group_id,add_to_group,check_user_group
from django.conf import settings
from .uspslogger import printlog,setlogenv
import os
import traceback

# Create your views here.
@api_view(['GET','POST'])
def createUser(request):

    if request.method == 'POST':
        supSer = SupplierUserSerializer(data=request.data)
        if supSer.is_valid():
            respfiled1= supSer.data['supplierID']
            respfiled2= supSer.data['DUNS']
            respfiled3= supSer.data['SCAC']
            respfiled4= supSer.data['emailAddress']
            respData = '{'+'"supplierID": "'+respfiled1+'",'+'"SCAC": "'+respfiled2+'",'+'"DUNS": "'+respfiled3+'",'+ '"emailAddress": "'+respfiled4+'"}'
        supRec = supplierUser()
        supRec = supSer
        
        if supSer.is_valid():
            return Response(respData,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        #supRec = supplierUser()
        lsupplierID = 'Supp_101'
        lDUNS = 'DUNS-201'
        lSCAC = 'SCAC-301'
        lemailAddress = 'supRec101@email.com'

        respdata = {
        "supplierID": lsupplierID,
        "DUNS": lDUNS,
        "SCAC": lSCAC,
        "emailAddress": lemailAddress
                }
        
        return  JsonResponse(respdata)
            

class authTest(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class postMethod(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def post(self, request):
        setlogenv(request)
        supSer = SupplierUserSerializer(data=request.data)
        
        tenantId = settings.TENANT_ID
        clientScret = settings.CLIENT_SECRET
        clientId = settings.CLIENT_ID
        bpgAdminGrpName = settings.BPG_ADMIN_GRP_NAME

        #tenantId = "a3170d40-4927-4e03-801e-aa8bf4316a77"
        #clientScret = "rDP8Q~FNxSPmVWF.Ssi0YQe47lAwctnqM_Xy4c03"
        #clientId = "fe10b6b4-6b9f-4cb6-8747-ccf08f83782a"
        errorMessage=""
        errorCode=""
        statusCode="Sucess"
        print(request.data)
        try:
            if supSer.is_valid():
                userEmailId= supSer.data['emailAddress']
                if (userEmailId != ""):
                    print(' userEmailId:'+ userEmailId);
                    print(' TenantId:'+ str(tenantId));
                    print(' ClientScret:'+ str(clientScret));
                    print(' ClientId:'+ str(clientId));
                    tokenValue = get_access_token(tenantId,clientId,clientScret)
                    if(tokenValue != ""):
                        print('Token Value: '+tokenValue)
                        #BPG_GRP_NAME="NAT_AZURE_BPG_ILE_USR_DEV"#will be read from Env later
                        grp_id = get_group_id (bpgAdminGrpName,tokenValue)
                        if(grp_id != ""):
                            print('bpg_grp_id: '+grp_id)
                            user_id = get_user_id(userEmailId, tokenValue)
                            if(user_id != ""):
                                print('User id:'+user_id)
                                grp_id_exists = check_user_group(user_id,grp_id,tokenValue)
                                if(grp_id_exists != ""):
                                    print('group_id: '+grp_id_exists)
                                    errorCode="200"
                                    statusCode="Sucess"
                                else:
                                    resultStatus = add_to_group(user_id,grp_id,tokenValue)
                                    if(resultStatus == "Added to Group"):
                                        print('resultStatus:'+resultStatus)
                                        errorCode="200"
                                        statusCode="Sucess"
                                    else:
                                        errorCode="500"
                                        statusCode="Error"
                                        errorMessage="Internal Error - unable to add to Admin Group"
                                        printlog('errorMessage:'+resultStatus,'ERROR')
                            else:
                                errorCode="204"
                                statusCode="Error"
                                errorMessage="Invalid emailAddress, emailAddrss not found in AzureAd"    
                        else:
                            errorCode="500"
                            statusCode="Error"
                            errorMessage="Internal Error - unable to get group Id"    
                    else:
                        errorCode="500"
                        statusCode="Error"
                        errorMessage="Internal Error - unable to get token"
                else:
                    statusCode = "Error"
                    errorCode = "400"
                    errorMessage ="Invalid or blank emailAddress value"
            else:
                statusCode = "Error"
                errorCode = "400"
                errorMessage ="Invalid Request Payload"

        except:
            print("Exception")
            errorMessage = traceback.format_exc()
            statusCode="Error"
            print('errorMessage:'+errorMessage)
            printlog('errorMessage:'+errorMessage,'ERROR')
            errorMessage = "Internal Error - contact SEAM IT support"
        
        respdata = {
                    "status": statusCode,
                    "errorMessage": errorMessage
                   }
        
        if (errorCode=="400"):
            return Response(respdata,status=status.HTTP_400_BAD_REQUEST)
        elif(errorCode=="204"):
            return Response(respdata,status=status.HTTP_204_NO_CONTENT)
        elif(errorCode=="500"):
            return Response(respdata,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif(errorCode=="200"):
            return Response(respdata,status=status.HTTP_200_OK)
        else:
            return Response(respdata,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       