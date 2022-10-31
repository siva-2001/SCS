from django.db import models
from django.contrib.auth.models import User
from SCSapp.models.MatchTeamResult import AbstractMatchTeamResult
from SCSapp.models.MatchActions import MatchAction

class AbstractMatch(models.Model):
    isAnnounced = models.BooleanField(default=True)
    competition = models.ForeignKey("SCSapp.Competition", on_delete=models.CASCADE, null=True)
    matchDateTime = models.DateTimeField(null=True)
    place = models.CharField(max_length=128, null=True, blank=True)
    protocol = models.FileField(upload_to='media/protocols/match', default=None, null=True, blank=True)
    judge = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True)

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

    def getData(self):
        matchTeamResults = AbstractMatchTeamResult.objects.filter(match=self)
        gameData = {
            'firstParticipantName':matchTeamResults[0].team.participant.name,
            'secondParticipantName':matchTeamResults[1].team.participant.name,
            'isAnnounced':True,
        }
        if not self.isAnnounced:
            gameData['firstTeamScore'] = matchTeamResults[0].teamScore
            gameData['secondTeamScore'] = matchTeamResults[1].teamScore
            gameData['isAnnounced'] = False
        data = {
            'matchDate':self.matchDateTime,
            'place':self.place,
            'gameData':gameData
        }
        if self.protocol: data['protocol'] = self.protocol.url

        #   Изменить способ определения наличия судьи
        if self.judge.first_name or self.judge.last_name:
            data['judge'] = self.judge.first_name + " " + self.judge.last_name
        return data


    def startMatch(self):
        pass
        #   Начало трансляции ?
        #   Жеребьёвка

    def endMatch(self):
        #   Генерация протокола
        self.isAnnounced = False
        self.save()

    def cancelMatch(self):
        for act in MatchAction.objects.filter(match=self): act.delete()
        for res in AbstractMatchTeamResult.objects.filter(match=self):
            res.teamScore = 0
            res.save()
