import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from SCSapp.models.Competition import Competition
from SCSapp.models.MatchActions import MatchAction
from SCSapp.models.MatchTeamResult import MatchTeamResult
from SCSapp.models.Match import AbstractMatch
from SCSapp.models.Team import Team
from SCSapp.func import getTokenFromASGIScope
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist


class ChatConsumer(WebsocketConsumer):
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def send_to_channel(self, message):
        async_to_sync(self.channel_layer.send)(
            self.channel_name, {"type": "chat_message", "message": message}
        )

    def send_to_group(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def getActionMessage(self, action):
        return {
            "message_type" : "action_info",
            "data" : {
                "id" : action.id,
                "signal" : action.eventType,
                "datetime" : str(action.eventTime),
                "team" : (action.team.participant.name if action.team else None),
            }
        }


    def getMatchTranslationData(self):
        teamsResults = [tr for tr in MatchTeamResult.objects.all().filter(match=self.match)]
        if len(teamsResults) != 2: return Response({"ERROR":"Ошибка сервера: количество команд не равно 2"})
        matchGoals = MatchAction.objects.all().filter(match=self.match).filter(eventType="GOAL")
        
        return {
            "message_type" : "translation_data",
            "time": "Пока что тут строковая заглушка",
            "data" : {
                "first_team":{
                    "result_id":teamsResults[0].id,
                    "participant_name":teamsResults[0].team.participant.name,
                    "score": str(len(matchGoals.filter(team=teamsResults[0].team))),
                    "rounds_score": "Заглушка. отображает количество выигранных раундов"
                },
                "second_team":{
                    "result_id":teamsResults[1].id,
                    "participant_name":teamsResults[1].team.participant.name,
                    "score": str(len(matchGoals.filter(team=teamsResults[1].team))),
                    "rounds_score": "Заглушка. отображает количество выигранных раундов"
                },
            }
        }

    def connect(self):
        self.match = AbstractMatch.objects.all().get(id=self.scope["url_route"]["kwargs"]["match_id"])
        self.room_group_name = "match_%s" % self.scope["url_route"]["kwargs"]["match_id"]
        async_to_sync(self.channel_layer.group_add)( self.room_group_name, self.channel_name )
        self.accept()

        for action in MatchAction.objects.all().filter(match=self.match):   # order by
            self.send_to_channel(json.dumps(self.getActionMessage(action), ensure_ascii=False))
        self.send_to_channel(json.dumps(self.getMatchTranslationData(), ensure_ascii=False))


    def receive(self, text_data):
        try: token = getTokenFromASGIScope()
        except: 
            self.send_to_group("Пользователь не авторизован")
            return
        if not self.match.judge == token.user:
            self.send_to_group("Вы не имеете судейских прав")
        else:
            message = json.loads(text_data)['message']
            teamResID = MatchTeamResult.objects.all().get(id=message["team_result_id"]) if message["team_result_id"] else None
            action = MatchAction.objects.create(
                eventType = message["signal"],
                match = self.match,
                team = (teamResID.team if teamResID else None),
            )
            self.send_to_group(self.getActionMessage(action))
            
            if action.eventType == "GOAL": 
            #   ||  action.eventType == "STOP_MATCH":
                send_to_group(self.getMatchTranslationData())

            


        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


        # {
        #     "message" : {
        #         "message_type" : "action_info",
        #         "data" : {
        #             "id" : action.id,
        #             "signal" : action.eventType,
        #             "datetime" : str(action.eventTime),
        #             "team" : (action.team.participant.name if action.team else None),
        #         }
        #     }
        # }

        # {
        #     "message" : {
        #         "message_type" : "translation_data",
        #         "time": "Пока что тут строковая заглушка",
        #         "data" : {
        #             "first_team":{
        #                 "result_id":teamsResults[0].id,
        #                 "participant_name":teamsResults[0].team.participant.name,
        #                 "score": str(len(matchActions.filter(team=teamsResults[0].team)))
        #                 "rounds_score": "Заглушка. отображает количество выигранных раундов"
        #             },
        #             "second_team":{
        #                 "result_id":teamsResults[1].id,
        #                 "participant_name":teamsResults[1].team.participant.name,
        #                 "score": str(len(matchActions.filter(team=teamsResults[1].team)))
        #                 "rounds_score": "Заглушка. отображает количество выигранных раундов"
        #             },
        #         }
        #     }
        # }