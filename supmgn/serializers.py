from rest_framework import serializers
from .models import supplierUser, suppResp
class SupplierUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = supplierUser
        fields = ['emailAddress']

class SuppRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = suppResp
        fields = ['suppAzureId','status','errorMessage']