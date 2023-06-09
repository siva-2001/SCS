from django.db import models


class Team(models.Model):
    participant = models.ForeignKey("SCSapp.Faculty", on_delete=models.CASCADE, default=None, null=True)


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


    class Meta:
            verbose_name = 'Волейбольная команда'
            verbose_name_plural = 'Волейбольные команды'