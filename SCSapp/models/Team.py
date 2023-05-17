from django.db import models


class Team(models.Model):
    participant = models.ForeignKey("SCSapp.Faculty", on_delete=models.CASCADE, default=None, null=True)
    class Meta:
            verbose_name = 'Команда'
            verbose_name_plural = 'Команды'
