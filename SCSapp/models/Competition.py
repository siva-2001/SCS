from django.urls import reverse
from django.db import models
import random

from authorizationApp.models import User
from .Match import AbstractMatch, VolleyballMatch
from .VolleyballTeam import VolleyballTeam

class CurrentCompetitionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Competition.StatusChoices.CURRENT)#, isHighLevelSportEvent=True)

class AnnouncedCompetitionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Competition.StatusChoices.ANNOUNSED)#, isHighLevelSportEvent=True)


class Competition(models.Model):
    objects = models.Manager()
    current_objects = CurrentCompetitionManager()
    announced_objects = AnnouncedCompetitionManager()


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

    name = models.CharField(max_length=256, verbose_name="Заголовок", null=True)
    description = models.TextField(blank=True, verbose_name="Описание", null=True)
    dateTimeStartCompetition = models.DateTimeField(verbose_name="Заявки на участие принимаются до", default=None, null=True, blank=True)
    dateTimeFinishCompetition = models.DateTimeField(blank=True, null=True, verbose_name="Соревнование завершилось")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Организатор")
    protocol = models.FileField(upload_to='protocols', null=True, blank=True, verbose_name="Протокол")
    regulations = models.FileField(upload_to='regulations', null=True, blank=True, verbose_name="Регламент соревнований")

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('competition', args=[str(self.id)])


    @classmethod
    def create(cls, name, description, startDate=None, organizer=None, regulations = None):
        object = cls()
        object.name = name
        object.description = description
        object.dateTimeStartCompetition = startDate
        object.organizer = organizer
        object.regulations = regulations
        object.status = cls.StatusChoices.ANNOUNSED
        object.save()
        return object


class VolleyballCompetition(Competition):
    class Meta:
        verbose_name = 'Соревнование по волейболу'
        verbose_name_plural = 'Соревнования по волейболу'

    numOfRounds = models.IntegerField(null=True, blank=True, verbose_name='Максимальное количество раундов')
    roundPointLimit = models.IntegerField(null = True,blank = True, verbose_name='Раунд идёт до')
    lastRoundPointLimit = models.IntegerField(null=True, blank=True, verbose_name='Последний раунд идёт до')

    onePointLead = models.IntegerField(verbose_name="Балл за отрыв в 1 очко", null=True, blank=True)
    twoPointsLead = models.IntegerField(verbose_name="Балл за отрыв в 2 очка", null=True, blank=True)
    threePointsLead = models.IntegerField(verbose_name="Балл за отрыв в 3 очка", null=True, blank=True)

    onePointLose = models.IntegerField(verbose_name="Балл за проигрыш в 1 очко", null=True, blank=True)
    twoPointsLose = models.IntegerField(verbose_name="Балл за проигрыш в 2 очка", null=True, blank=True)
    threePointsLose = models.IntegerField(verbose_name="Балл за проигрыш в 3 очка", null=True, blank=True)

    def getData(self):
        pass

    @classmethod
    def create(cls, name, description, startDate=None, organizer=None, regulations = None,
               numOfRounds=5, roundPointLimit=25, lastRoundPointLimit=15,
               onePointsLead = 1, twoPointsLead = 2, threePointsLead = None,
               onePointsLose = 0, twoPointsLose = 0, threePointsLose = None):
        object = super().create(name, description, startDate, organizer, regulations)

        object.numOfRounds = numOfRounds
        object.roundPointLimit = roundPointLimit
        object.lastRoundPointLimit = lastRoundPointLimit

        object.onePointsLead = onePointsLead
        object.twoPointsLead = twoPointsLead
        object.threePointsLead = threePointsLead

        object.onePointsLose = onePointsLose
        object.twoPointsLose = twoPointsLose
        object.threePointsLose = threePointsLose

        object.save()
        return object


    def draw(self):
        if(self.status == self.StatusChoices.ANNOUNSED):
            self.status = self.StatusChoices.CURRENT
            teams = list(VolleyballTeam.objects.all().filter(competition=self).filter(confirmed=True))

            for i in range(len(teams)):
                for j in range(i+1, len(teams)):
                    print("create")
                    VolleyballMatch.create(
                        firstTeam = teams[i],
                        secondTeam = teams[j],
                        competition = self,
                    )
            self.save()