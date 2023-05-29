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
    class fieldSideChoices(models.TextChoices):
        LEFT = "LEFT", 'Левая'
        RIGHT = 'RIGHT', 'Правая'

    firstRoundScore = models.IntegerField(default=None, null=True, blank=True)
    secondRoundScore = models.IntegerField(default=None, null=True, blank=True)
    thirdRoundScore = models.IntegerField(default=None, null=True, blank=True)
    fourthRoundScore = models.IntegerField(default=None, null=True, blank=True)
    fifthRoundScore = models.IntegerField(default=None, null=True, blank=True)
    currentRoundScore = models.IntegerField(default=None, null=True, blank=True)

    fieldSide = models.CharField(
        max_length=128,
        choices = fieldSideChoices.choices,
        verbose_name = 'Часть поля',
        null = True,
    )

    class Meta:
        verbose_name = 'Результат в матче по волейболу'
        verbose_name_plural = 'Результаты в матче по волейболу'


    def startMatch(self):
        self.currentRoundScore = 0
        self.teamScore = 0
        self.save()

    def getPauseCount(self):
        return len(MatchAction.objects.filter(match=self.match).filter(team=self.team).filter(eventType="PAUSE_ROUND"))

    def cancelLastGoal(self):
        if self.currentRoundScore != 0: self.currentRoundScore -= 1
        self.save()

    def updateRoundsScore(self, isWinner, currentRound):
        self.teamScore = (self.teamScore + 1) if isWinner else self.teamScore
        if currentRound == 1: self.firstRoundScore = self.currentRoundScore
        elif currentRound == 2: self.secondRoundScore = self.currentRoundScore
        elif currentRound == 3: self.thirdRoundScore = self.currentRoundScore
        elif currentRound == 4: self.fourthRoundScore = self.currentRoundScore
        elif currentRound == 5: self.fifthRoundScore = self.currentRoundScore
        self.currentRoundScore = 0
        print("__method__updateRoundsScore")
        self.save()

    def startNextRound(self):
        if self.firstRoundScore is None: self.firstRoundScore = 0
        elif self.secondRoundScore is None: self.secondRoundScore = 0
        elif self.thirdRoundScore is None: self.thirdRoundScore = 0
        elif self.fourthRoundScore is None: self.fourthRoundScore = 0
        elif self.fifthRoundScore is None: self.fifthRoundScore = 0
        if self.firstRoundScore: self.swapFieldSide()
        print("__method__startNextRound")
        self.save()

    def swapFieldSide(self):
        if self.fieldSide == self.fieldSideChoices.LEFT: self.fieldSide = self.fieldSideChoices.RIGHT
        else: self.fieldSide = self.fieldSideChoices.LEFT
        self.save()

    def goal(self):
        self.currentRoundScore += 1
        self.save()

    def getCurrentRoundScore(self):
        return self.currentRoundScore

