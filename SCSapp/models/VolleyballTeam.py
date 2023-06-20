from django.db import models


class Team(models.Model):
    participant = models.ForeignKey("SCSapp.Faculty", on_delete=models.CASCADE, default=None, null=True)
    # registratedDateTime = models.DateTimeField(auto_add=True)


    class Meta:
            verbose_name = 'Команда'
            verbose_name_plural = 'Команды'

class VolleyballTeam(Team):
    competition = models.ForeignKey("SCSapp.VolleyballCompetition", on_delete=models.CASCADE, default=None, null=True)
    confirmed = models.BooleanField(default=False)
    completed_games = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.participant.name + " в " + (self.competition.name if self.competition else " ")

    class Meta:
        verbose_name = 'Волейбольная команда'
        verbose_name_plural = 'Волейбольные команды'