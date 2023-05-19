from SCSapp.models.Competition import Competition, VolleyballCompetition
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.models.MatchTeamResult import VolleyballMatchTeamResult
from SCSapp.models.Team import Team
from authorizationApp.models import User
from SCSapp.models.Participant import Faculty
from translationApp.models import MatchAction

from django.shortcuts import redirect
from django.db import models
from django.contrib.auth.models import Group

def CreateTestDataView(request):
    user = User.objects.create(
        username = "user",
    )
    user.set_password("aaaa1234")
    user.save()


    competition_1 = VolleyballCompetition.objects.create(
        name = "Межфакультетские соревнования. Кубок по волейболу ТУСУР", 
        description = "Лучшие соревнования за последние 10, а то и 15 лет!",
        organizer = User.objects.get(username="admin"),
        numOfRounds=3,
        roundsPointLimit=15,
        lastRoundPointLimit=15,
        onePointsLead=1, twoPointsLead=2,
        onePointsLose=0, twoPointsLose=0,
    )

    competition_2 = VolleyballCompetition.objects.create(
        name = "Межфакультетские соревнования. Кубок по футболу ТУСУР", 
        description = "Вторые лучшие соревнования за последние 10, а то и 15 лет!",
        organizer = User.objects.get(username="user"),
        numOfRounds = 3,
        roundsPointLimit = 15,
        lastRoundPointLimit = 15,
        onePointsLead = 1, twoPointsLead = 2,
        onePointsLose = 0, twoPointsLose = 0,
    )

    competition_3 = VolleyballCompetition.objects.create(
        name = "Межвузовские соревнования. Кубок по футболу ТУСУР-ТПУ-ТГУ", 
        description = "Лучшие соревнования за последние 20, а то и 50 лет!",
        organizer = User.objects.get(username="user"),
        numOfRounds=3,
        roundsPointLimit=15,
        lastRoundPointLimit=15,
        onePointsLead=1, twoPointsLead=2,
        onePointsLose=0, twoPointsLose=0,
    )

    competition_4 = VolleyballCompetition.objects.create(
        name = "Пупок по полу ТУСУР", 
        description = "Худшие соревнование, без комментариев...",
        organizer = User.objects.get(username="admin"),
        numOfRounds=3,
        roundsPointLimit=15,
        lastRoundPointLimit=15,
        onePointsLead=1, twoPointsLead=2,
        onePointsLose=0, twoPointsLose=0,
    )

    competition_1.status = Competition.StatusChoices.PAST
    competition_3.status = Competition.StatusChoices.CURRENT
    competition_2.status = Competition.StatusChoices.CURRENT
    competition_1.save()
    competition_3.save()

    match_1 = VolleyballMatch.objects.create(
        competition = competition_2,
        judge = User.objects.get(username="admin")
    )  

    match_2 = VolleyballMatch.objects.create(
        competition = competition_3,
        judge = User.objects.get(username="user")
    )

    match_3 = VolleyballMatch.objects.create(
        competition = competition_3,
        judge = User.objects.get(username="admin")
    )

    match_4 = VolleyballMatch.objects.create(
        competition = competition_2,
        judge = User.objects.get(username="user")
    )

    participant_1 = Faculty.objects.create(name="РТФ")
    participant_2 = Faculty.objects.create(name="ФБ")
    participant_3 = Faculty.objects.create(name="ГФ")
    participant_4 = Faculty.objects.create(name="ФСУ")

    team_1 = Team.objects.create(participant=participant_1)
    team_2 = Team.objects.create(participant=participant_2)
    team_3 = Team.objects.create(participant=participant_3)
    team_4 = Team.objects.create(participant=participant_4)

    action_1 = MatchAction.objects.create(
        eventType = "Гол",
        team = team_1,
        match = match_2
    )
    action_2 = MatchAction.objects.create(
        eventType = "Перелёт",
        team = team_1,
        match = match_2
    )
    action_3 = MatchAction.objects.create(
        eventType = "Заступ",
        team = team_1,
        match = match_2
    )
    action_4 = MatchAction.objects.create(
        eventType = "Гол",
        team = team_1,
        match = match_2
    )
    
    match_team_res_1 = VolleyballMatchTeamResult.objects.create(
        team = team_1,
        match = match_1,
        teamScore = 5,
    )

    match_team_res_2 = VolleyballMatchTeamResult.objects.create(
        team = team_2,
        match = match_1,
        teamScore = 5,
    )

    match_team_res_3 = VolleyballMatchTeamResult.objects.create(
        team = team_3,
        match = match_2,
        teamScore = 5,
    )

    match_team_res_4 = VolleyballMatchTeamResult.objects.create(
        team = team_4,
        match = match_2,
        teamScore = 5,
    )

    match_team_res_5 = VolleyballMatchTeamResult.objects.create(
        team = team_1,
        match = match_3,
        teamScore = 5,
    )

    match_team_res_6 = VolleyballMatchTeamResult.objects.create(
        team = team_2,
        match = match_3,
        teamScore = 5,
    )

    match_team_res_7 = VolleyballMatchTeamResult.objects.create(
        team = team_3,
        match = match_4,
        teamScore = 5,
    )

    match_team_res_8 = VolleyballMatchTeamResult.objects.create(
        team = team_4,
        match = match_4,
        teamScore = 5,
    )

    group = Group.objects.create()
    group.name = "judges"
    group.save()

    group2 = Group.objects.create()
    group2.name = "organizer"
    group2.save()    

    user.groups.add(group)
    user.groups.add(group2)

    return redirect('homePage')
