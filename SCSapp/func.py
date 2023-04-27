from datetime import datetime
import pytz
import smtplib
from email.message import EmailMessage
from rest_framework.authtoken.models import Token
from SCSapp.models.MatchTeamResult import MatchTeamResult

def getMatchTranslationData(match):
        teamsResults = [tr for tr in MatchTeamResult.objects.all().filter(match=match)]
        if len(teamsResults) != 2: return Response({"ERROR":"Ошибка сервера: количество команд не равно 2"})
        
        

        return {
            "first":{
                "team_result_id":teamsResults[0].id,
                "participant_name":teamsResults[0].team.participant.name,
                "team_score":teamsResults[0].teamScore,
            },
            "second":{
                "team_result_id":teamsResults[1].id,
                "participant_name":teamsResults[1].team.participant.name,
                "team_score":teamsResults[1].teamScore,
            },
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
