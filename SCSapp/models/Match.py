from django.db import models

from SCSapp.models.MatchTeamResult import MatchTeamResult
from translationApp.models import MatchAction
from authorizationApp.models import User
from SCSapp.models.MatchTeamResult import VolleyballMatchTeamResult
from django.db.models import Q
import datetime
import time

class AbstractMatch(models.Model):
    isAnnounced = models.BooleanField(default=True)
    # competition = models.ForeignKey("SCSapp.Competition", on_delete=models.CASCADE, null=True)
    matchDateTime = models.DateTimeField(null=True, blank=True)
    place = models.CharField(max_length=128, null=True, blank=True)
    protocol = models.FileField(upload_to='media/protocols/match', default=None, null=True, blank=True)
    judge = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    match_translated_now = models.BooleanField(default=False)

    class competitionStageChoices(models.TextChoices):
        FINAL = "1/1", 'Финал'
        SEMI_FINAL = '1/2', 'Полуфинал'
        QUARTER_FINAL = '1/4', '1/4-финал'
        EIGHTH_FINALS = '1/8', '1/8-финал'

    competitionStage = models.CharField(
        max_length=16,
        choices=competitionStageChoices.choices,
        verbose_name='Круг розыгрыша',
        null=True,
    )

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

    @classmethod
    def create(cls, firstTeam, secondTeam, competition, judge=None):
        object = cls()
        object.competition = competition
        object.judge = judge
        object.save()
        return object
        #   При переопределении в дочерних классах создаются объекты результатов
        #   AbstractMatchTeamResult.create(firstTeam, object)
        #   AbstractMatchTeamResult.create(secondTeam, object)


    def startMatch(self):
        if self.isAnnounced:
            self.match_translated_now = True
            self.isAnnounced = False
            self.save()
            return True
        else: return False

    def cancelLastGoal(self):
        actions = MatchAction.objects.all().filter(match=self).order_by("-eventTime")
        if ((len(actions) > 1) and (actions[0].eventType == "CANCEL") and (actions[1].eventType == "GOAL")):
            VolleyballMatchTeamResult.objects.all().filter(match=self).get(team=actions[1].team).cancelLastGoal()
            actions[1].delete()
            actions[0].delete()
            return True
        actions[0].delete()
        return False


class VolleyballMatch(AbstractMatch):
    competition = models.ForeignKey("SCSapp.VolleyballCompetition", on_delete=models.CASCADE, null=True)
    round_translated_now = models.BooleanField(default=False)
    current_round = models.IntegerField(default=0, null=True, blank=True)


    class Meta:
        verbose_name = 'Волейбольный матч'
        verbose_name_plural = 'Волейбольные матчи'

    def create(cls, firstTeam, secondTeam, competition, judge=None):
        object = super().create()
        VolleyballMatchTeamResult.create(secondTeam, object)
        VolleyballMatchTeamResult.create(firstTeam, object)
        return object

    def startRound(self):
        if (not self.round_translated_now) and (self.competition.numOfRounds >  self.current_round):
            print("here")
            self.round_translated_now = True
            self.current_round += 1
            self.save()
            results = VolleyballMatchTeamResult.objects.all().filter(match=self)
            for res in results: res.startNextRound()

    def swapFieldSide(self):
        results = VolleyballMatchTeamResult.objects.all().filter(match=self)
        for res in results: res.swapFieldSide()

    def startMatch(self):
        if super().startMatch():
            results = VolleyballMatchTeamResult.objects.all().filter(match=self)
            for res in results: res.startMatch()
            return True
        else: return False

    def getWSAdress(self):
        return '/ws/volleyballTranslation/' + str(self.id) + '/'

    def checkEndRound(self):
        if self.current_round == self.competition.numOfRounds: maxRoundScore = self.competition.lastRoundPointLimit
        else: maxRoundScore = self.competition.roundPointLimit

        results = VolleyballMatchTeamResult.objects.all().filter(match=self)
        firstTeamScore = results[0].getCurrentRoundScore()
        secondTeamScore = results[1].getCurrentRoundScore()

        if ((firstTeamScore >= maxRoundScore and secondTeamScore < maxRoundScore-1) 
            or (secondTeamScore >= maxRoundScore and firstTeamScore < maxRoundScore-1) 
            or (secondTeamScore >= maxRoundScore - 1 and firstTeamScore >= maxRoundScore - 1 and
                abs(firstTeamScore-secondTeamScore) > 1 )): return True
        else: return False

    def endRound(self):
        print("__method__checkEndRound")
        results = VolleyballMatchTeamResult.objects.all().filter(match=self)
        firstTeamScore = results[0].getCurrentRoundScore()
        secondTeamScore = results[1].getCurrentRoundScore()
        results[0].updateRoundsScore(firstTeamScore > secondTeamScore, self.current_round)
        results[1].updateRoundsScore(firstTeamScore < secondTeamScore, self.current_round)
        self.round_translated_now = False
        self.save()

        #   завершить счёт времени таймера




    def checkEndGame(self):
        if self.current_round == self.competition.numOfRounds and not self.round_translated_now: return True



        else: return False

    def endGame(self):
        self.match_translated_now = False
        self.save()


    def getRoundTimer(self):
        def timeToSec(time):
            return time.hour * 3600 + time.minute * 60 + time.second

        match_actions = MatchAction.objects.all().filter(match=self)
        try: start_action = match_actions.filter(eventType="START_ROUND").get(round=self.current_round)
        except MatchAction.DoesNotExist: start_action = None
        actions = match_actions.filter(Q(eventType="CONTINUE_ROUND") | Q(eventType="PAUSE_ROUND")).filter(round=self.current_round)
        try: end_action = match_actions.filter(eventType="END_ROUND").get(round=self.current_round)
        except MatchAction.DoesNotExist: end_action = None

        if end_action or not start_action: return 0

        if self.round_translated_now: roundTimer = timeToSec(datetime.datetime.now().time())
        else: roundTimer = 0
        for action in actions:
            if action.eventType == "CONTINUE_ROUND": roundTimer -= timeToSec(action.eventTime)
            else: roundTimer += timeToSec(action.eventTime)
        roundTimer -= timeToSec(start_action.eventTime)
        return roundTimer

    def stopMatch(self):
        for act in MatchAction.objects.all().filter(match=self): act.delete()
        for res in VolleyballMatchTeamResult.objects.all().filter(match=self): res.stopMatch()
        self.match_translated_now = False
        self.round_translated_now = False
        self.current_round = 0
        self.isAnnounced = True
        self.save()

    def pauseRound(self):
        self.round_translated_now = False
        self.save()

    def continueRound(self):
        self.round_translated_now = True
        self.save()




    def getTranslationDataMessage(self):
        teamsResults = VolleyballMatchTeamResult.objects.all().filter(match=self)
        if len(teamsResults) != 2: return Response({"ERROR":"Ошибка сервера: количество команд не равно 2"})

        goalActions = MatchAction.objects.all().filter(match=self).filter(eventType="GOAL")

        try: lastGoalActionTeam = goalActions.order_by("-eventTime")[0].team.participant.name
        except: lastGoalActionTeam = teamsResults[0].team.participant.name

        return {
            "message_type" : "translation_data",
            "time" : self.getRoundTimer(),
            "round_time_is_run" : self.round_translated_now,
            "part" : self.current_round if (self.current_round != 0) else 1,
            "servesTheBall" : lastGoalActionTeam,
            "data" : {
                "first_team":{
                    "result_id" : teamsResults[0].id,
                    "participant_name" : teamsResults[0].team.participant.name,
                    "score" : teamsResults[0].getCurrentRoundScore(),
                    "rounds_score" : teamsResults[0].teamScore,
                    "fieldSide" : teamsResults[0].fieldSide,
                    "pauseCount" : teamsResults[0].getPauseCount()
                },
                "second_team":{
                    "result_id":teamsResults[1].id,
                    "participant_name":teamsResults[1].team.participant.name,
                    "score": teamsResults[1].getCurrentRoundScore(),
                    "rounds_score": teamsResults[1].teamScore,
                    "fieldSide": teamsResults[1].fieldSide,
                    "pauseCount": teamsResults[1].getPauseCount()
                },
            }
        }
