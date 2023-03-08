import math
import random
import time
OTP_EXPIRATION_SECONDS = 900
OTP_MAX_COUNTER = 3


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return str(OTP)


def generate_otp_wrapper(request):
    otp = generateOTP()
    request.session['OTP_COUNTER'] = '0'
    print("OTP is "+otp)
    request.session['OTP'] = otp
    request.session['OTP_EXPIRES_AT'] = str(
        int(time.time())+OTP_EXPIRATION_SECONDS)
    return request

def validate_otp_wrapper(otp, user_otp, otp_counter, otp_expires_at):
    error_msg = ""
    if (otp_counter>OTP_MAX_COUNTER):
        error_msg = 'Too Many Incorrect Attempts. Please Resend One Time Code.'
    elif (otp_expires_at < int(time.time())):
        error_msg = 'One Time Code has Expired. Please Resend.'
    elif (otp != user_otp):
        error_msg = 'Incorrect One Time Code. Please Try Again.'
    elif (otp == user_otp and otp_expires_at > int(time.time())):         
            error_msg = ""
    else:
         error_msg = 'Unable to validate One Time Code. Please Try Again.'
    
    return error_msg