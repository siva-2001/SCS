import json

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from .Match import Match
from .AbstractEvent import AbstractEvent
from django.core.serializers import serialize

class Competition(AbstractEvent):

    class SportTypeChoices(models.TextChoices):
        FOOTBALL = 'BB', 'Баскетбол'
        VOLLEYBALL = 'VB', 'Волейбол'


    sportType = models.CharField(
        max_length=128,
        verbose_name='Тип спорта',
        choices=SportTypeChoices.choices,
        default=SportTypeChoices.VOLLEYBALL
    )

    name = models.CharField(max_length=256, verbose_name="Заголовок", null=True)
    description = models.TextField(blank=True, verbose_name="Описание", null=True)
    dateTimeStartCompetition = models.DateTimeField(verbose_name="Заявки на участие принимаются до", default=None, null=True)
    dateTimeFinishCompetition = models.DateTimeField(blank=True, null=True, verbose_name="Соревнование завершилось")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Организатор")
    protocol = models.FileField(upload_to='protocols', null=True, blank=True, verbose_name="Протокол")
    regulations = models.FileField(upload_to='regulations', null=True, blank=True, verbose_name="Регламент соревнований")
    #_olympics = models.ForeignKey('SCSapp.olympics', on_delete=models.CASCADE, verbose_name='Спартакиада', null=True)
    isHighLevelSportEvent = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('competition', args=[str(self.id)])

    @classmethod
    def create(cls, name, description, sportType, isHighLevel, type, startDate, organizer, regulations):
        object = cls()
        object.name = name
        object.description = description
        object.sportType = sportType
        object.dateTimeStartCompetition = startDate
        object.isHighLevelSportEvent = isHighLevel
        object.organizer = organizer
        object.type = type
        object.regulations = regulations
        object.status = cls.StatusChoices.ANNOUNSED
        object.save()
        return object

    def editCompetition(self, name, description, startDate):
        if name and len(name) > 0: self.name = name
        if description and len(description) > 0: self.description = description
        if startDate and len(startDate) > 0: self.dateStartCompetition = startDate
        self.save()

    def getDateTimeStartCompetition(self):
        return self.dateTimeStartCompetition.strftime("%H:%M   %Y:%m:%d")
    def getDateTimeFinishCompetition(self):
        return self.dateTimeFinishCompetition.strftime("%H:%M   %Y:%m:%d")


    def getData(self):
        data = {
            'name':self.name,
            'description':self.description,
            'status':self.get_status_display(),
            'dateStartCompetition':self.dateTimeStartCompetition,
            'sportType':self.sportType,
            'type':self.type,
            'dateTimeFinishCompetition':self.dateTimeFinishCompetition,
        }
        if self.dateTimeFinishCompetition: data["dateTimeFinishCompetition"] = self.dateTimeFinishCompetition
        if self.protocol: data['protocol'] = self.protocol.url
        return data

    def getRelatedMatchesData(self):
        relatedMatches = Match.objects.filter(competition=self).order_by('status').order_by('matchDateTime')
        return [match.getData() for match in relatedMatches]

    #   Возвращает подтверждённые организатором команды
    def getRelatedTeams(self):
        pass

    #   Возвращает ещё не подтверждённые организатором команды
    def getApplicationsForParticipation(self):
        pass

    #   Данные на основе которых формируется турнирная сетка
    def getTournamentGrid(self):
        pass


    def getRelatedPlayersByParticipant(self):
        pass
