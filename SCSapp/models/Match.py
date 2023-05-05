from django.db import models

from SCSapp.models.MatchTeamResult import MatchTeamResult
from SCSapp.models.MatchActions import MatchAction
from SCSapp.models import User
from SCSapp.models.MatchTeamResult import VolleyballMatchTeamResult

class AbstractMatch(models.Model):
    isAnnounced = models.BooleanField(default=True)
    competition = models.ForeignKey("SCSapp.Competition", on_delete=models.CASCADE, null=True)
    matchDateTime = models.DateTimeField(null=True, blank=True)
    place = models.CharField(max_length=128, null=True, blank=True)
    protocol = models.FileField(upload_to='media/protocols/match', default=None, null=True, blank=True)
    judge = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    translated_now = models.BooleanField(default=False)

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

    def editMatch(self, date, place, judge):
        self.matchDateTime = date
        self.place = place
        self.judge = judge
        self.save()

    def startMatch(self):
        # self.translated_now = True
        pass
        #   Начало трансляции ?
        #   Жеребьёвка

    def endMatch(self):
        #   Генерация протокола
        self.isAnnounced = False
        self.save()

    def updateRoundsScore():
        results = VolleyballMatchTeamResult.objects.all().filter(match=self)
        results[0].updateRoundsScore(results[0].getCurrentRoundScore() > results[1].getCurrentRoundScore())
        results[1].updateRoundsScore(not results[0].getCurrentRoundScore() > results[1].getCurrentRoundScore())


    def getTranslationData(self):
        teamsResults = [tr for tr in VolleyballMatchTeamResult.objects.all().filter(match=self)]
        if len(teamsResults) != 2: return Response({"ERROR":"Ошибка сервера: количество команд не равно 2"})
        
        return {
            "message_type" : "translation_data",
            "time": "Пока что тут строковая заглушка",
            "data" : {
                "first_team":{
                    "result_id":teamsResults[0].id,
                    "participant_name":teamsResults[0].team.participant.name,
                    "score": teamsResults[0].getCurrentRoundScore(),
                    "rounds_score": teamsResults[0].teamScore
                },
                "second_team":{
                    "result_id":teamsResults[1].id,
                    "participant_name":teamsResults[1].team.participant.name,
                    "score": teamsResults[1].getCurrentRoundScore(),
                    "rounds_score": teamsResults[1].teamScore
                },
            }
        }

    def cancelLastAction(self):
        actions = MatchAction.objects.all().filter(match=self).order_by("-eventTime")
        if len(actions) != 0: actions[0].delete()
        
        

    # def cancelMatch(self):
    #     for act in MatchAction.objects.filter(match=self): act.delete()
    #     for res in MatchTeamResult.objects.filter(match=self):
    #         res.teamScore = 0
    #         res.save()
    