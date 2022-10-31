from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    participant = models.ForeignKey("SCSapp.AbstractParticipant", on_delete=models.CASCADE, default=None, null=True)
    class Meta:
            verbose_name = 'Команда'
            verbose_name_plural = 'Команды'
