from django.urls import reverse
from django.db import models
import random
from django.contrib.auth.models import User
import pytz
from datetime import datetime
from SCSapp.func import sentMail
from SCSapp.protocolCreator import PDF
from .Match import Match
from django.core.files import File
import os
from SCSapp.models.VolleyballTeam import VolleyballTeam

class Competition(models.Model):

    class StatusChoices(models.TextChoices):
        ANNOUNSED = "AN", 'Анонсированное'
        CURRENT = 'CR', 'Текущее'
        PAST = 'P', 'Прошедшее'

    class SportTypeChoices(models.TextChoices):
        FOOTBALL = 'FB', 'Футбол'
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
    dateTimeStartCompetition = models.DateTimeField(verbose_name="Заявки на участие принимаются до")
    dateTimeFinishCompetition = models.DateTimeField(blank=True, null=True, verbose_name="Соревнование завершилось")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Организатор")
    protocol = models.FileField(upload_to='protocols', null=True, blank=True, verbose_name="Протокол")
    #_olympics = models.ForeignKey('SCSapp.olympics', on_delete=models.CASCADE, verbose_name='Спартакиада', null=True)
    isHightLevelSportEvent = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'

    def __str__(self):
        return self._name

    def get_absolute_url(self):
        return reverse('competition', args=[str(self.id)])

    @classmethod
    def create(cls, name, discription, sportType, type, startDate, isHighLevel, orginizer):
        object = cls()
        object._name = name
        object._discription = discription
        object._sportType = sportType
        object._dateTimeStartCompetition = startDate
        object._isHightLevelSportEvent = isHighLevel
        object._organizer = orginizer
        object._type = type
        object.save()
        return object

    def editCompetition(self, name, discription, startDate):
        if name and len(name) > 0: self._name = name
        if discription and len(discription) > 0: self._discription = discription
        if startDate and len(startDate) > 0: self._dateTimeStartCompetition = startDate
        self.save()

    def getDateTimeStartCompetition(self):
        return self._dateTimeStartCompetition.strftime("%H:%M   %Y:%m:%d")
    def getDateTimeFinishCompetition(self):
        return self._dateTimeFinishCompetition.strftime("%H:%M   %Y:%m:%d")

    def getData(self):
        data = {
            'name':self._name,
            'discription':self._discription,
            'status':self.get__status_display(),
            'dateTimeStartCompetition':self.getDateTimeStartCompetition(),
        }
        if self._dateTimeFinishCompetition: data["dateTimeEndCompetition"] = self.getDateTimeFinishCompetition()
        if self._protocol: data['protocol_url'] = self._protocol.url
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


# class Competition(models.Model):
#     ANNOUNSED = 'Announsed'
#     CURRENT = 'Current'
#     PAST = 'Past'
#     competitionStatusChoises = [
#         (ANNOUNSED, 'Announsed'),
#         (CURRENT, 'Current'),
#         (PAST, 'Past'),
#     ]
#     status = models.CharField(
#         max_length=12,
#         choices=competitionStatusChoises
#     )
#     name = models.CharField(max_length=100, verbose_name="Заголовок", null=True)
#     discription = models.TextField(blank=True, verbose_name="Описание", null=True)
#     sportType = models.CharField(max_length=32, verbose_name='Тип спорта')
#     dateTimeStartCompetition = models.DateTimeField(verbose_name="Заявки на участие принимаются до")
#     dateTimeFinishCompetition = models.DateTimeField(blank=True, null=True, verbose_name="Соревнование завершилось")
#     organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Организатор")
#     protocol = models.FileField(upload_to='protocols', null=True, blank=True, verbose_name="Протокол")
#     olympics = models.ForeignKey('SCSapp.olympics', on_delete=models.CASCADE, verbose_name='Спартакиада')
#
#
#     class Meta:
#         permissions = [
#             ('control_competition','the user must be the judge')
#         ]
#         verbose_name = 'Соревнование'
#         verbose_name_plural = 'Соревнования'
#
#
#     def __str__(self):
#         return f" Title: {self.name}"
#
#     def get_absolute_url(self):
#         return reverse('competition', args=[str(self.id)])
#
#
#     def getLastTimeForApplicationStr(self):
#         return self.dateTimeStartCompetition.strftime("%H:%M   %Y:%m:%d")
#
#     def getEndDateTimeStr(self):
#         return self.dateTimeFinishCompetition.strftime("%H:%M   %Y:%m:%d")
#
#     def makeStandings(self):
#         teams = VolleyballTeam.objects.all().filter(competition=self)
#
#         self.status = Competition.CURRENT
#         self.save()
#         standingElemets = []
#
#         while(len(standingElemets) < len(teams)):
#             num = random.randint(0, len(teams)-1)
#             if not teams[num] in standingElemets:
#                 standingElemets.append(teams[num])
#
#         tours = 0
#         while(pow(tours, 2) <= len(teams)):
#             for ind, elem in enumerate(standingElemets):
#                 if ind < len(standingElemets)-1:
#                     if type(elem) == VolleyballTeam and type(standingElemets[ind+1]) == VolleyballTeam:
#                         match = Match(
#                             name= f"{elem.name} vs {standingElemets[ind+1].name}",
#                             firstTeam = elem,
#                             secondTeam = standingElemets[ind+1],
#                             competition=self,
#                         )
#                         match.save()
#                         standingElemets.remove(elem)
#                         standingElemets.remove(standingElemets[ind])
#                         standingElemets.insert(ind, match)
#                     elif type(elem) == VolleyballTeam and type(standingElemets[ind+1]) == Match:
#                         match = Match(
#                             name=f"{elem.name} vs _______",
#                             firstTeam = elem,
#                             competition = self
#                         )
#                         match.save()
#                         standingElemets[ind + 1].nextMatch = match
#                         standingElemets[ind + 1].save()
#                         standingElemets.remove(elem)
#                         standingElemets.remove(standingElemets[ind])
#                         standingElemets.insert(ind, match)
#                     elif type(elem) == Match and type(standingElemets[ind+1]) == Match:
#                         match = Match(
#                             name=f"_______ vs ________",
#                             competition = self,
#                         )
#                         match.save()
#                         elem.nextMatch = match
#                         elem.save()
#                         standingElemets[ind+1].nextMatch = match
#                         standingElemets[ind+1].save()
#                         standingElemets.remove(elem)
#                         standingElemets.remove(standingElemets[ind])
#                         standingElemets.insert(ind, match)
#             standingElemets.reverse()
#             tours += 1
#         return True
#
#     def updateStanding(self, matchID):
#         match = Match.objects.all().get(id=matchID)
#         nextMatch = match.nextMatch
#         if(nextMatch):
#             if nextMatch.firstTeam:
#                 if match.firstTeamScore > match.secondTeamScore:
#                     nextMatch.secondTeam = match.firstTeam
#                 else:
#                     nextMatch.secondTeam = match.secondTeam
#                 nextMatch.name = f"{nextMatch.firstTeam} vs {nextMatch.secondTeam}"
#             else:
#                 if match.firstTeamScore > match.secondTeamScore:
#                     nextMatch.firstTeam = match.firstTeam
#                 else:
#                     nextMatch.firstTeam = match.secondTeam
#                 nextMatch.name = f"{nextMatch.firstTeam} vs _____________"
#             nextMatch.save()
#         else:
#             self.status = Competition.PAST
#             self.dateTimeFinishCompetition = pytz.UTC.localize(datetime.now())
#             self.save()
#             self.GenerateProtocol()
#         self.DoMailingAboutStart()
#
#     def GenerateProtocol(self):
#         pdf = PDF()
#         teams = VolleyballTeam.objects.all().filter(competition=self)
#         matches = Match.objects.all().filter(competition=self)
#         teamsPF, matchesPF = [], []
#         for team in teams:
#             teamsPF.append(team.getProtocolFormat())
#         for match in matches:
#             matchesPF.append( match.getProtocolFormat())
#         pdf.CompetitionProtocol(self.name, teamsPF, matchesPF,
#                                 self.organizer.first_name + "  " + self.organizer.last_name, str(self.getEndDateTimeStr()))
#         with open("tempFile.pdf", 'rb') as protocol:
#             self.protocol.save(self.name+".pdf", File(protocol), save=False)
#         os.remove("tempFile.pdf")
#         self.save()
#
#
#     def DoMailingAboutStart(self):
#         users = User.objects.all()
#         strRecipients = ''
#         for user in users:
#             if user.email:
#                 strRecipients = strRecipients + user.email + ', '
#         strRecipients = strRecipients[:-2]
#         message = f"Соревнования {self.name} стартовали!"
#         sentMail(message=message, strRecipients=strRecipients)
