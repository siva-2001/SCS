from datetime import datetime
import pytz
import smtplib
from email.message import EmailMessage
from rest_framework.authtoken.models import Token
from SCSapp.models.MatchTeamResult import MatchTeamResult


def getTokenFromASGIScope(scope):
    for elem in scope['headers']:
        if(elem[0] == b'cookie'): cookie_mass = elem[1].decode("utf-8").split(";")
    for cookie in cookie_mass:
        if ("Authorization" in cookie) or ("Authorization=Token" in cookie): token_key = cookie.split(" ")[-1]
    token = Token.objects.all().get(key=token_key)
    return token
