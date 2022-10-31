from django.db import models

class AbstractParticipant(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название', default='ФСУ')
    class Meta():
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'