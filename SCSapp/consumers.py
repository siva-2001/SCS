import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from SCSapp.models.Competition import Competition
from SCSapp.models.MatchActions import MatchAction
from SCSapp.models.MatchTeamResult import AbstractMatchTeamResult
from SCSapp.models.Match import AbstractMatch
from SCSapp.models.Team import Team
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.number_of_sending_events = 15
        self.match = AbstractMatch.objects.all().get(id=self.scope["url_route"]["kwargs"]["match_id"])
        self.room_group_name = "match_%s" % self.scope["url_route"]["kwargs"]["match_id"]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": "Connecconnection established"}
            )

        matchActions = MatchAction.objects.all().filter(match=self.match)
        for action in matchActions:#[(len(matchActions) - self.number_of_sending_events):]:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": f"{action.eventType}"}
            )

    def receive(self, text_data):
        for elem in self.scope['headers']:
            if(elem[0] == b'cookie'): cookie_mass = elem[1].decode("utf-8").split(";")
        for cookie in cookie_mass:
            if ("Authorization" in cookie) or ("Authorization=Token" in cookie): token_key = cookie.split(" ")[-1]
        try: 
            token = Token.objects.all().get(key=token_key)
        except: 
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": "Пользователь не авторизован"}
            )
            return       
        
        if self.match.judge == token.user:
            message = json.loads(text_data)['message']
            if message["team_result_id"]:
                team = AbstractMatchTeamResult.objects.all().get(id=message["team_result_id"]).team
            else: team = None

            matchAction = MatchAction.objects.create(
                eventType = message["signal"],
                match = self.match,
                team = team,
            )
                
            answerMessage = json.dumps({
                "id":matchAction.id,
                "signal": message["signal"],
                "team": team.participant.name,
                "datetime": str(matchAction.eventTime)
            }, ensure_ascii=False)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": answerMessage}
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": "Вы не имеете судейских прав"}
            ) 

                
    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"]}))
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )