from django.db import models

# Create your models here.
class supplierUser(models.Model):
    emailAddress = models.CharField(max_length=100)

class suppResp(models.Model):
    status = models.CharField(max_length=10)
    errorMessage = models.CharField(max_length=2000,default="TextError")
