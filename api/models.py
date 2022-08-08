from django.db import models
import json

# Create your models here.
# Model to capture User details


class UserDetails:
    uid: int
    firstName: str
    lastName: str
    email: str
    company: str
    supplierId: str
    responseText: str
    user_id: str