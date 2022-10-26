from django.db import models
from django.contrib.auth.models import User

class Olympics(models.Model):

    class StatusChoices(models.TextChoices):
        ANNOUNSED = "AN", 'Анонсированное'
        CURRENT = 'CR', 'Текущее'
        PAST = 'P', 'Прошедшее'

    statusOlympics = models.CharField(
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.ANNOUNSED,
        verbose_name='Статус спартакиады',
    )

    name = models.CharField(max_length=255, verbose_name= 'Название спартакиады')
    discription = models.CharField(max_length=255, verbose_name= 'Описание спартакиады')
    dateTimeStartOlympics = models.DateField(verbose_name='Дата начала спартакиады')
    dateTimeFinishOlympics = models.DateField(verbose_name='Дата конца спартакиады')
    protocol = models.FileField(verbose_name='Протокол', upload_to='protocols', null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Организатор")

    @classmethod
    def create(cls, name, description, dateTimeStartOlympics):
        object = cls()
        object.name = name
        object.description = description
        object.dateTimeStartOlympics = dateTimeStartOlympics
        object.save()
        return object

    def getData(self):
        data = {
            'name': self.name,
            'discription': self.discription,
            'dateTimeStartOlympics': self.dateTimeStartOlympics,
            'dateTimeFinishOlympics': self.dateTimeFinishOlympics,
            'protocol': self.protocol,
            'organizer': self.organizer,
            'status': self.statusOlympics,
        }
        return data

    def editCompetition(self, statusOlympics, name, description, startDate):
        if name and len(name) > 0: self.name = name
        if description and len(description) > 0: self.description = description
        if startDate and len(startDate) > 0: self.dateStartCompetition = startDate
        if statusOlympics and len(statusOlympics) > 0: self.statusOlympics = statusOlympics
        self.save()