from django.db import models
from authorizationApp.models import User

class Faculty(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название')
    emblem = models.ImageField(upload_to='media/emblems', default=None, null=True, blank=True)
    description = models.CharField(max_length=512, verbose_name='Описание', default="")

    representative = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True)

    class Meta():
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.name