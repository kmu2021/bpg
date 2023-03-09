from azure.communication.email import EmailClient
from azure.core.exceptions import HttpResponseError
from django.conf import settings

EMAIL_ENDPOINT = settings.AZURE_EMAIL_ENDPOINT
EMAIL_ACCESS_KEY = settings.AZURE_EMAIL_ACCESS_KEY
EMAIL_FROM_ADDRESS = settings.AZURE_EMAIL_FROM_ADDRESS


def send_email(message):
    error_message = ""
    try:
        connection_string = "endpoint=" + EMAIL_ENDPOINT+";accessKey=" + EMAIL_ACCESS_KEY
        email_client = EmailClient.from_connection_string(connection_string)
        poller = email_client.begin_send(message)    
        error_message = poller.result()
    except HttpResponseError as ex:        
        print(ex)
        error_message = str(ex)    
    except Exception as e:
        print(e)   
        error_message = str(e)     
    return error_message


def send_email_wrapper(email_from, email_to_arr, email_subject, email_plain_text, email_html_text):
    error_message = ""

    try:
        if (not email_from):
            email_from = EMAIL_FROM_ADDRESS

        content = {"subject": email_subject,
                    "plainText": email_plain_text,
                    "html": email_html_text
                    }
        recipients = {"to":email_to_arr}
        message = {"senderAddress":email_from, "content":content, "recipients":recipients}
        error_message = send_email(message)
    except Exception as e:
        print(e)   
        error_message = str(e) 
    return error_message