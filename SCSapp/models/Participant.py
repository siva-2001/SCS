from django.db import models

class Faculty(models.Model):

    name = models.CharField(max_length=64, verbose_name='Название', default='ФСУ')
    class Meta():
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'