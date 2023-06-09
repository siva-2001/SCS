from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
import json
from SCSapp.models.Competition import Competition, VolleyballCompetition
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.models.VolleyballTeam import VolleyballTeam
from SCSapp.models.Player import VolleyballPlayer
from SCSapp.serializers import CompetitionSerializer, VolleyballCompetitionSerializer, VolleyballMatchSerializer
from SCSapp.serializers import VolleyballTeamSerializer, VolleyballPlayerSerializer, FacultySerializer
from authorizationApp.models import User
from SCSapp.models.MatchTeamResult import MatchTeamResult, VolleyballMatchTeamResult
from SCSapp.models.Faculty import Faculty
from translationApp.matchActionsDict import actionsDict



socketINFO = [    # FOR_DEBUG
        "Обмен данными происходит по технологии websocket. В сообщении скорей всего мобилка будет передавать JSON-запись с указанием сигнала и, для событий команд - название команды (участника)",
        "None в button_color окрашивает кнопку в стандартный серый цвет. '_FFFFFF' - нижнее подчёркивание говорит что текст кнопки должен быть белым. Кнопка отмены окрашивается отдельно, смотри фигму",
    ]

class JudgeCompetitionsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.GET.get("olympics_id"):
            competitions = [match.competition for match in VolleyballMatch.objects.all()
                if request.user == match.judge and
                match.competition.status == Competition.StatusChoices.CURRENT]       
        else:
            competitions = [match.competition for match in AbstractMatch.objects.all() 
                if request.user == match.judge and
                int(request.GET.get("olympics_id")) == match.competition.olympics.id and
                match.competition.status == Competition.StatusChoices.CURRENT] 

        serializer = VolleyballCompetitionSerializer(competitions, many=True)
        return Response(serializer.data)

class JudgeMatchesAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.GET.get("competition_id"): return Response({"error":"Не указан competition_id параметр HTTP-запроса"})
        
        matches = [match for match in VolleyballMatch.objects.all()
            if (request.user == match.judge and 
            int(request.GET.get("competition_id")) == match.competition.id and
            (match.isAnnounced or match.match_translated_now))]
        serializer = VolleyballMatchSerializer(matches, many=True)
        
        for matchDataDict in serializer.data:
            abstrTeamRes = MatchTeamResult.objects.filter(match = matchDataDict["id"])
            matchDataDict["firstTeam"] = abstrTeamRes[0].team.participant.name
            matchDataDict["secondTeam"] = abstrTeamRes[1].team.participant.name

        return Response(serializer.data)


class MatchManagmentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            match = VolleyballMatch.objects.get(id=json.loads(request.body)["match_id"])
            response = actionsDict["volleyball"]

            # if AbstractMatch.objects.get(id=json.loads(request.body)["match_id"]).competition.sportType == Competition.SportTypeChoices.VOLLEYBALL:
            #     match = VolleyballMatch.objects.get(id=json.loads(request.body)["match_id"])
            #     response = actionsDict["volleyball"]
            # else: return Response({"ERROR": "Нет события для этого вида спорта"})
        except: return Response({"ERROR":"Матч с указанным ID не существует"})

        if match.judge != self.request.auth.user:
            return Response({"ERROR":"Судейство в этом матче недоступно под этой учётной записью"})
        response["teams_data"] = match.getTranslationDataMessage()
        response["info"] = socketINFO
        if not match.match_translated_now: match.startMatch()
        response["WSLink"] = match.getWSAdress()

        return Response(response)

class VolleyballCompetitionAPIView(generics.ListCreateAPIView):
    queryset = VolleyballCompetition.objects.all()
    serializer_class = VolleyballCompetitionSerializer

class AnnouncedEventsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Competition.announced_objects.all()
    serializer_class = CompetitionSerializer

class CurrentCompetitionAPIView(generics.ListAPIView):
    queryset =  Competition.current_objects.all()
    serializer_class = CompetitionSerializer


# class OlympicsAPIView(generics.ListAPIView):
#     queryset = Olympics.objects.all()
#     serializer_class = OlympicsSerializer

# class CurrentOlympicsAPIView(generics.ListAPIView):
#     queryset = Olympics.current_objects.all()
#     serializer_class = OlympicsSerializer





# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________



class CertainVolleyballCompetitionAPIView(generics.RetrieveUpdateAPIView):
    queryset = VolleyballCompetition.objects.all()
    serializer_class = VolleyballCompetitionSerializer
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        if type(request.user) == AnonymousUser:
            return Response({"ERROR":"Пользователь не авторизован"})
        if request.user != VolleyballCompetition.objects.all().get(id=kwargs['pk']).organizer:
            return Response({"ERROR": "Нет доступа для редактирования"})
        return self.update(request, *args, **kwargs)

class VolleyballMatchesOfCompetitionAPIView(generics.ListAPIView):
    queryset = VolleyballMatch.objects.all().order_by('competitionStage', "matchDateTime")
    serializer_class = VolleyballMatchSerializer

    def get_queryset(self, comp_id):
        if comp_id: return self.queryset.filter(competition = comp_id)
        else: return self.queryset.all()

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(kwargs['pk']), many=True)

        for matchDataDict in serializer.data:
            teamRes = VolleyballMatchTeamResult.objects.filter(match=matchDataDict["id"])
            matchDataDict["firstTeam"] = teamRes[0].team.participant.name
            matchDataDict["firstTeamScore"] = teamRes[0].teamScore
            matchDataDict["firstTeamEmblem"] = teamRes[0].team.participant.emblem.url if teamRes[0].team.participant.emblem else None

            matchDataDict["secondTeam"] = teamRes[1].team.participant.name
            matchDataDict["secondTeamScore"] = teamRes[1].teamScore
            matchDataDict["secondTeamEmblem"] = teamRes[1].team.participant.emblem.url if teamRes[1].team.participant.emblem else None



            roundsScore = ''
            if not matchDataDict["isAnnounced"]:
                if teamRes[0].firstRoundScore and teamRes[1].firstRoundScore:
                    roundsScore += ('(' + str(teamRes[0].firstRoundScore) + ":" + str(teamRes[1].firstRoundScore) + ';  ')
                if teamRes[0].secondRoundScore and teamRes[1].secondRoundScore:
                    roundsScore += (str(teamRes[0].secondRoundScore) + ":" + str(teamRes[1].secondRoundScore) + ';  ')
                if teamRes[0].thirdRoundScore and teamRes[1].thirdRoundScore:
                    roundsScore += (str(teamRes[0].thirdRoundScore) + ":" + str(teamRes[1].thirdRoundScore) + ';  ')
                if teamRes[0].fourthRoundScore and teamRes[1].fourthRoundScore:
                    roundsScore += (str(teamRes[0].fourthRoundScore) + ":" + str(teamRes[1].fourthRoundScore) + ';  ')
                if teamRes[0].fifthRoundScore and teamRes[1].fifthRoundScore:
                    roundsScore += (str(teamRes[0].fifthRoundScore) + ":" + str(teamRes[1].fifthRoundScore) + ';')
                roundsScore += ")"
            matchDataDict["roundsScore"] = roundsScore



        return Response(serializer.data)

class CertainVolleyballMatch(generics.RetrieveUpdateAPIView):
    queryset = VolleyballMatch.objects.all()
    serializer_class = VolleyballMatchSerializer

    def put(self, request, *args, **kwargs):
        if type(request.user) == AnonymousUser:
            return Response({"ERROR":"Пользователь не авторизован"})
        if request.user != VolleyballMatch.objects.all().get(id=kwargs['pk']).competition.organizer:
            return Response({"ERROR": "Нет доступа для редактирования"})
        return self.update(request, *args, **kwargs)

class VolleyballTeamAPIView(generics.ListCreateAPIView):
    queryset = VolleyballTeam.objects.all()
    serializer_class = VolleyballTeamSerializer

    def get_queryset(self, comp_id):
        if comp_id: return self.queryset.filter(competition = comp_id)
        else: return self.queryset.all()

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(kwargs['pk']), many=True)

        competition = VolleyballCompetition.objects.get(id=kwargs["pk"])
        competition.draw()

        for teamDataDict in serializer.data:
            teamDataDict['icon_url'] = Faculty.objects.get(id=teamDataDict['participant']).emblem.url
            teamDataDict['participant_name'] = Faculty.objects.get(id=teamDataDict['participant']).name
        return Response(serializer.data)



class PlayerAPIView(generics.ListCreateAPIView):
    queryset = VolleyballPlayer.objects.all()
    serializer_class = VolleyballPlayerSerializer

    def get_queryset(self):
        if self.request.GET.get("team_id"): return self.queryset.filter(team=self.request.GET.get("team_id"))
        else: return self.queryset.all()

# ПРОПИСАТЬ ТЕСТЫ

class FacultyDetailAPIView(generics.RetrieveAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer