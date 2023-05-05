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
    matchGoalsNumber = models.IntegerField(default=None, null=True, blank=True)

    def updateRoundsScore(self, isWinner=False):        
        if self.thirdRoundScore is not None: return "error : счёт всех раундов уже сохранён"
        else:
            self.teamScore = (self.teamScore + 1) if isWinner else self.teamScore
            if self.firstRoundScore is None: self.firstRoundScore = self.matchGoalsNumber
            elif self.secondRoundScore is None: self.secondRoundScore = self.matchGoalsNumber - self.firstRoundScore
            else: self.thirdRoundScore = self.matchGoalsNumber - (self.firstRoundScore + self.secondRoundScore)
            self.save()

    def getCurrentRoundScore(self):
        if self.firstRoundScore is None: return self.matchGoalsNumber
        elif self.secondRoundScore is None: return self.matchGoalsNumber- self.firstRoundScore
        else: return self.matchGoalsNumber - (self.firstRoundScore + self.secondRoundScore)



    def getData(self):
        data = super().getData()
        data['firstRoundScore'] = self.firstRoundScore
        data['secondRoundScore'] = self.secondRoundScore
        data['thirdRoundScore'] = self.thirdRoundScore
        return data
