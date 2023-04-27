import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from SCSapp.models.Competition import Competition
from SCSapp.models.MatchActions import MatchAction
from SCSapp.models.MatchTeamResult import MatchTeamResult
from SCSapp.models.Match import AbstractMatch
from SCSapp.models.Team import Team
from SCSapp.func import getTokenFromASGIScope, getMatchTranslationData
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.match = AbstractMatch.objects.all().get(id=self.scope["url_route"]["kwargs"]["match_id"])
        self.room_group_name = "match_%s" % self.scope["url_route"]["kwargs"]["match_id"]

        async_to_sync(self.channel_layer.group_add)( self.room_group_name, self.channel_name )
        self.accept()

        for action in MatchAction.objects.all().filter(match=self.match):
            async_to_sync(self.channel_layer.send)(
                self.channel_name, {"type": "chat_message", "message": json.dumps({
                        "id": action.id,
                        "signal": action.eventType,
                        "datetime": str(action.eventTime),
                        "team":(action.team.participant.name if action.team else None),
                        "teams_data" : getMatchTranslationData(self.match)
                    }, ensure_ascii=False)}
            )

        async_to_sync(self.channel_layer.send)(
            self.channel_name, {"type": "chat_message", "message": json.dumps({
                "message_type" : ""
            })}
        )

        


    def receive(self, text_data):
        try: token = getTokenFromASGIScope(self.scope)
        except: 
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": "Пользователь не авторизован"}
            )
            return
        if not self.match.judge == token.user:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": "Вы не имеете судейских прав"}
            ) 
        else:
            message = json.loads(text_data)['message']
            action = MatchAction.objects.create(
                eventType = message["signal"],
                match = self.match,
                team = (MatchTeamResult.objects.all().get(id=message["team_result_id"]).team if teamResID else None),
            )
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": json.dumps({
                        "id":action.id,
                        "signal": action.eventType,
                        "datetime": str(action.eventTime),
                        "team":(action.team.participant.name if action.team else None),
                        "teams_data" : getMatchTranslationData(self.match)
                    }, ensure_ascii=False )}
            )



    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"]}))
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )