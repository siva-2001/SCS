from django.db import models
from SCSapp.models.MatchActions import MatchAction

class MatchTeamResult(models.Model):
    team = models.ForeignKey('SCSapp.Team', on_delete=models.CASCADE)
    teamScore = models.IntegerField(default=None, null=True, blank=True)
    match = models.ForeignKey("SCSapp.AbstractMatch", on_delete=models.CASCADE)

    @classmethod
    def create(cls, team, match):
        object = cls()
        object.team = team
        object.match = match
        object.save()
        

class VolleyballMatchTeamResult(MatchTeamResult):
    firstRoundScore = models.IntegerField(default=None, null=True, blank=True)
    secondRoundScore = models.IntegerField(default=None, null=True, blank=True)
    thirdRoundScore = models.IntegerField(default=None, null=True, blank=True)
    currentRoundScore = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Результат в матче по волейболу'
        verbose_name_plural = 'Результаты в матче по волейболу'

    def startMatch(self):
        self.firstRoundScore = 0
        self.currentRoundScore = 0
        self.teamScore = 0
        self.save()

    def updateRoundsScore(self, isWinner=False):        
        if self.thirdRoundScore is not None: 
            print("error : счёт всех раундов уже сохранён")
            return {"ERROR" : "счёт всех раундов уже сохранён"}
        else:
            self.teamScore = (self.teamScore + 1) if isWinner else self.teamScore
            if self.firstRoundScore is None: self.firstRoundScore = self.currentRoundScore
            elif self.secondRoundScore is None: self.secondRoundScore = self.currentRoundScore
            else: self.thirdRoundScore = self.currentRoundScore
            self.currentRoundScore = 0
            self.save()


    def goal(self):
        self.currentRoundScore = len(MatchAction.objects.all().filter(match=self.match).filter(team=self.team).filter(eventType="GOAL"))
        self.save()

    def getCurrentRoundScore(self):
        return self.currentRoundScore

