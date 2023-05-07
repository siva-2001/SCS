import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from SCSapp.models.Competition import Competition
from SCSapp.models.MatchActions import MatchAction
from SCSapp.models.MatchTeamResult import VolleyballMatchTeamResult
from SCSapp.models.Match import AbstractMatch
from SCSapp.models.Team import Team
from SCSapp.func import getTokenFromASGIScope
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


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

    def connect(self):
        # ошибка при отсутствии матча в БД
        self.match = AbstractMatch.objects.all().get(id=self.scope["url_route"]["kwargs"]["match_id"])
        self.room_group_name = "match_%s" % self.scope["url_route"]["kwargs"]["match_id"]
        async_to_sync(self.channel_layer.group_add)( self.room_group_name, self.channel_name )
        self.accept()
        if self.match.translated_now:
            for action in MatchAction.objects.all().filter(match=self.match).order_by("eventTime"):   # order by
                self.send_to_channel(json.dumps(action.getActionMessage(), ensure_ascii=False))
            self.send_to_channel(json.dumps(self.match.getTranslationData(), ensure_ascii=False))
        else:
            self.send_to_channel(json.dumps({"ERROR":"Трансляция матча не ведётся в данный момент"}, ensure_ascii=False))
            self.disconnect("translation close")
            


    def receive(self, text_data):
        try: token = getTokenFromASGIScope(self.scope)
        except: 
            self.send_to_group("Пользователь не авторизован")
            return
        if not self.match.judge == token.user: self.send_to_group("Вы не имеете судейских прав")
        else:
            message = json.loads(text_data)['message']

            if message["signal"] == "CANCEL": self.match.cancelLastAction()
            else: 
                teamRes = VolleyballMatchTeamResult.objects.all().get(id=message["team_result_id"]) if message["team_result_id"] else None
                
                action = MatchAction.objects.create(
                    eventType = message["signal"],
                    match = self.match,
                    team = (teamRes.team if teamRes else None),
                )

                self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))
                if action.eventType == "GOAL":
                    teamRes.goal()
                    if self.match.checkEndRound(): 
                        action = MatchAction.objects.create(
                            eventType = "END_ROUND",
                            match = self.match,
                            team = (teamRes.team if teamRes else None),
                        )


                    self.send_to_group(json.dumps(self.match.getTranslationData(), ensure_ascii=False))


        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )