from datetime import datetime
import pytz
import smtplib
from email.message import EmailMessage
from rest_framework.authtoken.models import Token

def getUserAuthData(user):
    return {
        'userAuth' : user.is_authenticated,
        "userIsJudge" : user.has_perm('SCS.control_competition'),
    }

def getTokenFromASGIScope(scope):
    # for elem in scope['headers']:
    #     if(elem[0] == b'Authorization'): token = elem[1].decode("utf-8")
    # print(token)
    # return token
    
    print(scope['headers'])
    for elem in scope['headers']:
        if(elem[0] == b'cookie'): cookie_mass = elem[1].decode("utf-8").split(";")
    for cookie in cookie_mass:
        if ("Authorization" in cookie) or ("Authorization=Token" in cookie): token_key = cookie.split(" ")[-1]
    token = Token.objects.all().get(key=token_key)
    return token
