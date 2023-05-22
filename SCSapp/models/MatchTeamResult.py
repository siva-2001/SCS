from django.db import models
from translationApp.models import MatchAction

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
    fourthRoundScore = models.IntegerField(default=None, null=True, blank=True)
    fifthRoundScore = models.IntegerField(default=None, null=True, blank=True)

    currentRoundScore = models.IntegerField(default=None, null=True, blank=True)

    def startNextRound(self):
        if self.firstRoundScore is None: self.firstRoundScore = 0
        elif self.secondRoundScore is None: self.secondRoundScore = 0
        elif self.thirdRoundScore is None: self.thirdRoundScore = 0
        elif self.fourthRoundScore is None: self.fourthRoundScore = 0
        elif self.fifthRoundScore is None: self.fifthRoundScore = 0
        self.save()

    class Meta:
        verbose_name = 'Результат в матче по волейболу'
        verbose_name_plural = 'Результаты в матче по волейболу'

    def startMatch(self):
        self.currentRoundScore = 0
        self.teamScore = 0
        self.save()

    def updateRoundsScore(self, isWinner, currentRound):
        if self.thirdRoundScore is not None: 
            print("error : счёт всех раундов уже сохранён")
            return {"ERROR" : "счёт всех раундов уже сохранён"}
        else:
            self.teamScore = (self.teamScore + 1) if isWinner else self.teamScore
            if currentRound == 1: self.firstRoundScore = self.currentRoundScore
            elif currentRound == 2: self.secondRoundScore = self.currentRoundScore
            elif currentRound == 3: self.thirdRoundScore = self.currentRoundScore
            elif currentRound == 4: self.fourthRoundScore = self.currentRoundScore
            elif currentRound == 5: self.fifthRoundScore = self.currentRoundScore
            self.currentRoundScore = 0
            self.save()


    def goal(self):
        # self.currentRoundScore = len(MatchAction.objects.all().filter(match=self.match).filter(team=self.team).filter(eventType="GOAL"))
        self.currentRoundScore += 1
        self.save()

    def getCurrentRoundScore(self):
        return self.currentRoundScore

