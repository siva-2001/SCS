from django.urls import reverse
from django.db import models

from authorizationApp.models import User
from .Match import AbstractMatch
from .Team import Team

class CurrentCompetitionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Competition.StatusChoices.CURRENT, isHighLevelSportEvent=True)

class AnnouncedCompetitionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Competition.StatusChoices.ANNOUNSED, isHighLevelSportEvent=True)


class Competition(models.Model):
    objects = models.Manager()
    current_objects = CurrentCompetitionManager()
    announced_objects = AnnouncedCompetitionManager()

    class TypeChoices(models.TextChoices):
        INTERNAL = 'INTERNAL', 'Внутреннее'
        INTERCOLLEGIATE = 'INTERCOLLEGIATE', 'Межвузовское'

    class StatusChoices(models.TextChoices):
        ANNOUNSED = "ANNONCED", 'Анонсированное'
        CURRENT = 'CURRENT', 'Текущее'
        PAST = 'PAST', 'Прошедшее'

    status = models.CharField(
        max_length=128,
        choices = StatusChoices.choices,
        default = StatusChoices.ANNOUNSED,
        verbose_name = 'Статус',
    )

    type = models.CharField(
        verbose_name='Тип',
        max_length=128,
        choices = TypeChoices.choices,
        default = TypeChoices.INTERCOLLEGIATE,
    )

    class SportTypeChoices(models.TextChoices):
        FOOTBALL = 'BASKETBALL', 'Баскетбол'
        VOLLEYBALL = 'VOLLEYBALL', 'Волейбол'


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
    # olympics = models.ForeignKey('SCSapp.olympics', on_delete=models.CASCADE, verbose_name='Спартакиада', null=True, default=None, blank=True)
    isHighLevelSportEvent = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'

    def __str__(self):
        # if self.olympics: return f"{self.SportTypeChoices(self.sportType).label} в < {self.olympics} >"
        return self.name


    def get_absolute_url(self):
        return reverse('competition', args=[str(self.id)])

    @classmethod
    def create(cls, name, description, sportType, isHighLevel=True, type=None, startDate=None, organizer=None, regulations = None, olympics = None):
        object = cls()
        object.name = name
        object.description = description
        object.sportType = sportType
        object.dateTimeStartCompetition = startDate
        object.isHighLevelSportEvent = isHighLevel
        object.organizer = organizer
        object.type = type
        object.olympics = olympics
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
        data = self.__dict__
        if self.protocol: data['protocol'] = self.protocol.url
        data["isOlympics"] = False
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
            data.append(match.getGridData()['gameData'])
        return data


    def getRelatedPlayersByParticipant(self):
        pass


class CacheScore(models.Model):
    participantScore = models.IntegerField()
    participantRaiting = models.FloatField()
    participantPlace = models.IntegerField()
    competition = models.ForeignKey('SCSapp.Competition', on_delete=models.CASCADE)
    participant = models.ForeignKey('SCSapp.Faculty', on_delete=models.CASCADE)


    @classmethod
    def create(cls, participant, competition):
        object = cls()
        object.participantScore = 0
        object.participantPlace = 0
        object.participantRaiting = 0
        object.competition = competition
        object.participant = participant
        object.save()
        return object

    def update(self, score, raiting, place):
        self.participantRaiting = raiting
        self.participantScore = score
        self.participantPlace = place
        self.save()
