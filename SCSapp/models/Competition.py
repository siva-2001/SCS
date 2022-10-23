from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from .Participant import AbstractParticipant
from .Match import AbstractMatch
from .MatchTeamResult import AbstractMatchTeamResult
from .Team import Team

class Competition(models.Model):

    class StatusChoices(models.TextChoices):
        ANNOUNSED = "AN", 'Анонсированное'
        CURRENT = 'CR', 'Текущее'
        PAST = 'P', 'Прошедшее'

    class SportTypeChoices(models.TextChoices):
        FOOTBALL = 'BB', 'Баскетбол'
        VOLLEYBALL = 'VB', 'Волейбол'

    class TypeChoices(models.TextChoices):
        INTERNAL = 'INT', 'Внутреннее'
        INTERCOLLEGIATE = 'IC', 'Межвузовское'

    name = models.CharField(max_length=256, verbose_name="Заголовок", null=True)
    status = models.CharField(
        max_length=2,
        choices = StatusChoices.choices,
        default = StatusChoices.ANNOUNSED,
        verbose_name = 'Статус',
    )
    sportType = models.CharField(
        max_length=128,
        verbose_name='Тип спорта',
        choices=SportTypeChoices.choices,
        default=SportTypeChoices.VOLLEYBALL
    )
    type = models.CharField(
        max_length=3,
        choices = TypeChoices.choices,
        default = TypeChoices.INTERCOLLEGIATE,
    )

    description = models.TextField(blank=True, verbose_name="Описание", null=True)
    dateStartCompetition = models.DateField(verbose_name="Заявки на участие принимаются до", default=None, null=True)
    dateFinishCompetition = models.DateField(blank=True, null=True, verbose_name="Соревнование завершилось")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Организатор")
    protocol = models.FileField(upload_to='protocols', null=True, blank=True, verbose_name="Протокол")
    regulations = models.FileField(upload_to='regulations', null=True, blank=True, verbose_name="Регламент соревнований")
    #_olympics = models.ForeignKey('SCSapp.olympics', on_delete=models.CASCADE, verbose_name='Спартакиада', null=True)
    isHightLevelSportEvent = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('competition', args=[str(self.id)])

    @classmethod
    def create(cls, name, description, sportType, isHighLevel, type, startDate, organizer, regulations, olympics):
        object = cls()
        object.name = name
        object.description = description
        object.sportType = sportType
        object.dateStartCompetition = startDate
        object.isHightLevelSportEvent = isHighLevel
        object.organizer = organizer
        object.type = type
        # object.olympics = olympics
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

        #   def getRelatedTeams(self)
        #   def getRelatedMatchesData(self)

        matchesData = list()
        for match in AbstractMatch.objects.filter(competition=self):
            matchesData.append(match.getData())
        data = {
            'name':self.name,
            'discription':self.description,
            'status':self.get_status_display(),
            'dateStartCompetition':self.dateStartCompetition,
            'matchesData': matchesData,
        }
        if self.dateFinishCompetition: data["dateEndCompetition"] = self.dateFinishCompetition
        if self.protocol: data['protocol_url'] = self.protocol.url
        return data

    def getRelatedMatchesData(self):
        relatedMatches = AbstractMatch.objects.filter(competition=self).order_by('status').order_by('matchDateTime')
        return [match.getData() for match in relatedMatches]

    #   Возвращает подтверждённые организатором команды
    def getRelatedTeams(self):
        return Team.objects.filter(competition=self).filter(confirmed=True)

      # Возвращает ещё не подтверждённые организатором команды
    def getApplicationsForParticipation(self):
        return Team.objects.filter(competition=self).filter(confirmed=False)


    #   Данные на основе которых формируется турнирная сетка
    def getTournamentGrid(self):
        data = list()
        for match in AbstractMatch.objects.filter(competition=self):
            data.append(match.getGridData())
        return data



