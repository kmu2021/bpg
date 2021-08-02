from django.db import models

# Create your models here.
class UspsServices:
    id : int
    serviceName : str    
    serviceDescription : str
    url : str    
    accessFlag : bool

class UserDetails:
    uid: int
    userName: str