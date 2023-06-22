from SCSapp.models.Competition import Competition, VolleyballCompetition
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.models.MatchTeamResult import VolleyballMatchTeamResult
from SCSapp.models.VolleyballTeam import VolleyballTeam
from authorizationApp.models import User
from SCSapp.models.Faculty import Faculty
from SCSapp.models.Player import VolleyballPlayer
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
        roundPointLimit=15,
        lastRoundPointLimit=15,
        onePointLead=1, twoPointsLead=2,
        onePointLose=0, twoPointsLose=0,
        status = Competition.StatusChoices.ANNOUNSED,
    )

    competition_2 = VolleyballCompetition.objects.create(
        name = "Межвузовские соревнования. Кубок по футболу ТУСУР-ТПУ-ТГУ", 
        description = "Лучшие соревнования за последние 20, а то и 50 лет!",
        organizer = User.objects.get(username="user"),
        numOfRounds=3,
        roundPointLimit=15,
        lastRoundPointLimit=15,
        onePointLead=1, twoPointsLead=2,
        onePointLose=0, twoPointsLose=0,
        status = Competition.StatusChoices.CURRENT,
    )

    match_1 = VolleyballMatch.objects.create(
        competition = competition_2,
        judge = User.objects.get(username="user")
    )  

    match_2 = VolleyballMatch.objects.create(
        competition = competition_2,
        judge = User.objects.get(username="user")
    )

    match_3 = VolleyballMatch.objects.create(
        competition = competition_2,
        judge = User.objects.get(username="user")
    )

    match_4 = VolleyballMatch.objects.create(
        competition = competition_2,
        judge = User.objects.get(username="user")
    )

    participant_1 = Faculty.objects.create(name="РТФ", description="Ну, пойдёт")
    participant_2 = Faculty.objects.create(name="ФБ", description="Не лучший факультет")
    participant_3 = Faculty.objects.create(name="ГФ", description="Не лучший факультет")
    participant_4 = Faculty.objects.create(name="ФСУ", description="Лучший факультет")

    team_1 = VolleyballTeam.objects.create(participant=participant_1)
    team_2 = VolleyballTeam.objects.create(participant=participant_2)
    team_3 = VolleyballTeam.objects.create(participant=participant_3)
    team_4 = VolleyballTeam.objects.create(participant=participant_4)

    trainer_1 = VolleyballPlayer.objects.create(
        FIO = "Иванов Пётр Степанович",
        age = 22,
        height = 199,
        weight = 80,
        trainer = True,
        team = team_1,
    )
    player_1 = VolleyballPlayer.objects.create(
        FIO = "Степан Иванович Петров",
        age = 22,
        height = 199,
        weight = 80,
        trainer = False,
        team=team_1,
    )
    player_2 = VolleyballPlayer.objects.create(
        FIO = "Абдула Ибн Хатаб",
        age = 22,
        height = 199,
        weight = 80,
        trainer = False,
        team=team_1,
    )

    trainer_2 = VolleyballPlayer.objects.create(
        FIO = "Кириешкин Пётр Степанович",
        age = 22,
        height = 199,
        weight = 80,
        trainer = True,
        team = team_2,
    )
    player_3 = VolleyballPlayer.objects.create(
        FIO = "Виктор Иванович Петров",
        age = 22,
        height = 199,
        weight = 80,
        trainer = False,
        team=team_2,
    )
    player_4 = VolleyballPlayer.objects.create(
        FIO = "Аллах Ибн Исхазис",
        age = 22,
        height = 199,
        weight = 80,
        trainer = False,
        team=team_2,
    )
    
    match_team_res_1 = VolleyballMatchTeamResult.objects.create(
        team = team_4,
        match = match_1,
        teamScore = 2,
        fieldSide=VolleyballMatchTeamResult.fieldSideChoices.LEFT,
    )

    match_team_res_2 = VolleyballMatchTeamResult.objects.create(
        team = team_3,
        match = match_1,
        teamScore = 1,
        fieldSide=VolleyballMatchTeamResult.fieldSideChoices.RIGHT,
    )

    match_team_res_3 = VolleyballMatchTeamResult.objects.create(
        team = team_2,
        match = match_2,
        teamScore = 0,
        fieldSide = VolleyballMatchTeamResult.fieldSideChoices.LEFT
    )

    match_team_res_4 = VolleyballMatchTeamResult.objects.create(
        team = team_1,
        match = match_2,
        teamScore = 3,
        fieldSide=VolleyballMatchTeamResult.fieldSideChoices.RIGHT
    )

    match_team_res_5 = VolleyballMatchTeamResult.objects.create(
        team = team_4,
        match = match_3,
        teamScore = 2,
        fieldSide=VolleyballMatchTeamResult.fieldSideChoices.LEFT
    )

    match_team_res_6 = VolleyballMatchTeamResult.objects.create(
        team = team_2,
        match = match_3,
        teamScore = 2,
        fieldSide=VolleyballMatchTeamResult.fieldSideChoices.RIGHT
    )

    match_team_res_7 = VolleyballMatchTeamResult.objects.create(
        team = team_3,
        match = match_4,
        teamScore = 1,
        fieldSide=VolleyballMatchTeamResult.fieldSideChoices.LEFT
    )

    match_team_res_8 = VolleyballMatchTeamResult.objects.create(
        team = team_1,
        match = match_4,
        teamScore = 3,
        fieldSide=VolleyballMatchTeamResult.fieldSideChoices.RIGHT
    )

    action_1 = MatchAction.objects.create(
        eventType = "START_ROUND",
        team = team_1,
        match = match_2,
        roundEventTime=142,
        round = 2,
    )
    action_2 = MatchAction.objects.create(
        eventType = "GOAL",
        team = team_1,
        match = match_2,
        roundEventTime = 142,
        round=2,
    )
    action_3 = MatchAction.objects.create(
        eventType = "GOAL",
        team = team_1,
        match = match_2,
        roundEventTime=11,
        round=2,
    )
    action_4 = MatchAction.objects.create(
        eventType = "GOAL",
        team = team_1,
        match = match_2,
        roundEventTime=42,
        round=2,
    )
    action_5 = MatchAction.objects.create(
        eventType = "PAUSE_ROUND",
        team = team_2,
        match = match_2,
        roundEventTime=12,
        round=3,
    )
    action_6 = MatchAction.objects.create(
        eventType = "PAUSE_ROUND",
        team = team_1,
        match = match_2,
        roundEventTime=142,
        round=1,
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
