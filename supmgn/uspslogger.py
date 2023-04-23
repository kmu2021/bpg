import datetime
import inspect
from django.conf import settings
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

G_USERNAME = ""
G_CUSTOM_PREFIX = "APPLOG"
G_APPLICATION_LOG_LEVEL = settings.DJANGO_LOG_LEVEL

G_LOG_LEVELS = {"CRITICAL": 50, "ERROR": 40,
                "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOTSET": 0}

# Set the Log Environment Global variables like User Name
def setlogenv(request):
    global G_USERNAME
    try:
        G_USERNAME = request.headers.get('X-MS-CLIENT-PRINCIPAL-ID') 
        #May need to fetch it from .auth/me endpoint. Also can be checked if present in Session.               
        G_USERNAME = G_USERNAME if G_USERNAME is not None else ""
    except Exception as e:
        G_USERNAME = ""

# Print the Log
def printlog(message, log_level="INFO"):
    
    global G_USERNAME, G_CUSTOM_PREFIX, G_LOG_LEVELS, G_APPLICATION_LOG_LEVEL
    module_name = ""
    function_name = ""

    #Proceed only if Log level is greater than Application Log Level
    if (G_LOG_LEVELS.get(log_level)>=G_LOG_LEVELS.get(G_APPLICATION_LOG_LEVEL)):
        try:
            module_name = inspect.getmodulename(inspect.stack()[1][1])
            module_name = module_name if module_name is not None else ""
        except Exception as e:
            module_name = ""
        try:
            function_name = inspect.stack()[1][3]
            function_name = function_name if function_name is not None else ""
        except Exception as e:
            function_name = ""
        try:
            log_message = G_CUSTOM_PREFIX + " " + log_level + " " + str(datetime.datetime.now()) + " " + module_name + "." + function_name + " " + G_USERNAME + " " + message    
            print(log_message)
        except Exception as e:
            pass
        
