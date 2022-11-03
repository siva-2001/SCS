from django.db import models
from django.contrib.auth.models import User
import datetime
class CurrentOlympicsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Olympics.StatusChoices.CURRENT)

class Olympics(models.Model):
    current_objects = CurrentOlympicsManager()
    class TypeChoices(models.TextChoices):
        INTERNAL = 'INT', 'Внутреннее'
        INTERCOLLEGIATE = 'IC', 'Межвузовское'

    class StatusChoices(models.TextChoices):
        CURRENT = 'CR', 'Текущее'
        PAST = 'P', 'Прошедшее'

    status = models.CharField(
        max_length=2,
        choices = StatusChoices.choices,
        default = StatusChoices.CURRENT,
        verbose_name = 'Статус',
    )

    type = models.CharField(
        max_length=3,
        choices = TypeChoices.choices,
        default = TypeChoices.INTERCOLLEGIATE,
    )

    name = models.CharField(max_length=255, verbose_name= 'Название спартакиады')
    description = models.CharField(max_length=255, verbose_name= 'Описание спартакиады')
    dateTimeStartOlympics = models.DateField(verbose_name='Дата начала спартакиады', auto_now_add=True)
    dateTimeFinishOlympics = models.DateField(verbose_name='Дата конца спартакиады', auto_now_add=True)
    protocol = models.FileField(verbose_name='Протокол', upload_to='protocols', null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Организатор")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Спартакаиада'
        verbose_name_plural = 'Спартакиады'

    @classmethod
    def create(cls, name, description, organizer, type):
        object = cls()
        object.name = name
        object.organizer = organizer
        object.description = description
        object.type = type
        object.save()
        return object

    def getData(self):
        data = {
            'name': self.name,
            'description': self.description,
            'dateTimeStartOlympics': self.dateTimeStartOlympics,
            #'dateTimeFinishOlympics': self.dateTimeFinishOlympics,
            'organizer': self.organizer,
            'status': self.status,
        }
        if self.dateTimeFinishOlympics: data["dateTimeFinishCompetition"] = self.dateTimeFinishOlympics
        if self.protocol: data['protocol'] = self.protocol.url
        return data

    def editOlympics(self, status, name, description, startDate):
        if name and len(name) > 0: self.name = name
        if description and len(description) > 0: self.description = description
        if startDate and len(startDate) > 0: self.dateStartCompetition = startDate
        if status and len(status) > 0: self.status = status
        self.save()