from django.db import models

from SCSapp.models.MatchTeamResult import MatchTeamResult
from translationApp.models import MatchAction
from authorizationApp.models import User
from SCSapp.models.MatchTeamResult import VolleyballMatchTeamResult

class AbstractMatch(models.Model):
    isAnnounced = models.BooleanField(default=True)
    # competition = models.ForeignKey("SCSapp.Competition", on_delete=models.CASCADE, null=True)
    matchDateTime = models.DateTimeField(null=True, blank=True)
    place = models.CharField(max_length=128, null=True, blank=True)
    protocol = models.FileField(upload_to='media/protocols/match', default=None, null=True, blank=True)
    judge = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True)

    match_translated_now = models.BooleanField(default=False)



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
        self.match_translated_now = True
        self.isAnnounced = False
        self.save()

    def endMatch(self):
        #   Генерация протокола

        self.match_translated_now = False
        self.save()

    def cancelLastAction(self):
        actions = MatchAction.objects.all().filter(match=self).order_by("-eventTime")
        if len(actions) > 1: actions[1].delete()

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
            self.round_translated_now = True
            self.current_round += 1
            self.save()
            results = VolleyballMatchTeamResult.objects.all().filter(match=self)
            for res in results: res.startNextRound()


    def startMatch(self):
        if self.isAnnounced:
            super().startMatch()
            results = VolleyballMatchTeamResult.objects.all().filter(match=self)
            for res in results: res.startMatch()
            return 'ws://127.0.0.1:8000/ws/volleyballTranslation/'+ str(self.id) +'/'



    def checkEndRound(self):
        if self.current_round == self.competition.numOfRounds: maxRoundScore = self.competition.lastRoundPointLimit
        else: maxRoundScore = self.competition.roundPointLimit

        results = VolleyballMatchTeamResult.objects.all().filter(match=self)
        firstTeamScore = results[0].getCurrentRoundScore()
        secondTeamScore = results[1].getCurrentRoundScore()

        if ((firstTeamScore >= maxRoundScore and secondTeamScore < maxRoundScore-1) 
            or (secondTeamScore >= maxRoundScore and firstTeamScore < maxRoundScore-1) 
            or (secondTeamScore >= maxRoundScore - 1 and firstTeamScore >= maxRoundScore - 1 and
                abs(firstTeamScore-secondTeamScore) > 1 )):
            print("mde")
            results[0].updateRoundsScore(firstTeamScore > secondTeamScore, self.current_round)
            results[1].updateRoundsScore(firstTeamScore < secondTeamScore, self.current_round)

            #   завершить счёт времени таймера

            return True
        else: return False
        # если раунд закончился - соответствующие действия

    def getTranslationData(self):
        teamsResults = VolleyballMatchTeamResult.objects.all().filter(match=self)
        if len(teamsResults) != 2: return Response({"ERROR":"Ошибка сервера: количество команд не равно 2"})
        
        return {
            "message_type" : "translation_data",
            "time" : "Пока что тут строковая заглушка",
            "part" : "Заглушка",
            "data" : {
                "first_team":{
                    "result_id" : teamsResults[0].id,
                    "participant_name" : teamsResults[0].team.participant.name,
                    "score" : teamsResults[0].getCurrentRoundScore(),
                    "rounds_score" : teamsResults[0].teamScore,
                    # "PlaceSide" : "LEFT"
                },
                "second_team":{
                    "result_id":teamsResults[1].id,
                    "participant_name":teamsResults[1].team.participant.name,
                    "score": teamsResults[1].getCurrentRoundScore(),
                    "rounds_score": teamsResults[1].teamScore
                },
            }
        }
