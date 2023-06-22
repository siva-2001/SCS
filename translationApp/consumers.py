import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from SCSapp.models.Competition import Competition
from translationApp.models import MatchAction
from SCSapp.models.MatchTeamResult import VolleyballMatchTeamResult
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.models.VolleyballTeam import VolleyballTeam
from authorizationApp.func import getTokenFromASGIScope
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

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def connect(self):
        self.room_group_name = "match_%s" % self.scope["url_route"]["kwargs"]["match_id"]
        async_to_sync(self.channel_layer.group_add)( self.room_group_name, self.channel_name )
        self.accept()
        if self.match.match_translated_now:
            for action in MatchAction.objects.all().filter(match=self.match).order_by("eventTime"):   # order by
                self.send_to_channel(json.dumps(action.getActionMessage(), ensure_ascii=False))
            self.send_to_channel(json.dumps(self.match.getTranslationDataMessage(), ensure_ascii=False))
            print(self.match.getTranslationDataMessage())

        else:
            self.send_to_channel(json.dumps({"ERROR":"Трансляция матча не ведётся в данный момент"}, ensure_ascii=False))
            self.disconnect("translation close")

    def createAction(self, signal, team_res):
        action = MatchAction.objects.create(
            eventType=signal,
            match=self.match,
            team=(team_res.team if team_res else None),
            round = self.match.current_round,
            roundEventTime = self.match.getRoundTimer()
        )
        return action

    def getInfoWindowMessage(self, message):
        return {
            "message_type" : "Info_message",
            "data" : message
        }




class VolleyballConsumer(ChatConsumer):

    def connect(self):
        # ошибка при отсутствии матча в БД
        self.match = VolleyballMatch.objects.all().get(id=self.scope["url_route"]["kwargs"]["match_id"])
        super().connect()

    def receive(self, text_data):
        try:
            token = getTokenFromASGIScope(self.scope)
        except:
            self.send_to_channel("Пользователь не авторизован")
            return
        if not self.match.judge == token.user:
            self.send_to_channel("Вы не имеете судейских прав")
        else:
            message = json.loads(text_data)['message']
            teamRes = VolleyballMatchTeamResult.objects.all().get(id=message["team_result_id"]) if message["team_result_id"] else None

            if message["signal"] == "GOAL" and self.match.round_translated_now:
                action = self.createAction(message["signal"], teamRes)
                self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))
                teamRes.goal()
                if self.match.checkEndRound():
                    action = self.createAction("END_ROUND", teamRes)
                    self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))
                    self.match.endRound()
                if self.match.checkEndGame():
                    action = self.createAction("END_GAME", teamRes)
                    self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))

            if message["signal"] == "START_ROUND" and not self.match.round_translated_now:
                # ограничитель на количество событий данного типа в раунде
                self.match.startRound()
                action = self.createAction(message["signal"], teamRes)
                self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))

            if message["signal"] == "CANCEL":
                action = self.createAction(message["signal"], teamRes)
                self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))
                self.match.cancelLastGoal()

            if message["signal"] == "PAUSE_ROUND" and self.match.round_translated_now:
                if teamRes.getPauseCount() < 2:
                    action = self.createAction(message["signal"], teamRes)
                    self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))
                    self.match.pauseRound()
                else:
                    self.send_to_channel(json.dumps(
                        self.getInfoWindowMessage("Команда использовала все доступные ей перерывы"),
                        ensure_ascii=False
                    ))

            matchActions = MatchAction.objects.all().filter(match=self.match)
            if message["signal"] == "CONTINUE_ROUND" and not self.match.round_translated_now and self.match.current_round != 0\
                    and (len(matchActions.filter(eventType="PAUSE_ROUND")) != len(matchActions.filter(eventType="CONTINUE_ROUND"))):

                action = self.createAction(message["signal"], teamRes)
                self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))
                self.match.continueRound()

            if message['signal'] == "SWAP_FIELD_SIDE": self.match.swapFieldSide()

            if message['signal'] == "STOP_MATCH" and self.match.match_translated_now:
                action = self.createAction(message["signal"], teamRes)
                self.send_to_group(json.dumps(action.getActionMessage(), ensure_ascii=False))
                self.match.stopMatch()
                self.disconnect("translation close")

        self.send_to_group(json.dumps(self.match.getTranslationDataMessage(), ensure_ascii=False))
