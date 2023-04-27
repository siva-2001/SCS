from django.db import models

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

    def getData(self):
        data = super().getData()
        data['firstRoundScore'] = self.firstRoundScore
        data['secondRoundScore'] = self.secondRoundScore
        data['thirdRoundScore'] = self.thirdRoundScore
        return data


