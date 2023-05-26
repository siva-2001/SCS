from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
import json
from SCSapp.models.Competition import Competition, VolleyballCompetition
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.serializers import MatchSerializer, CompetitionSerializer, VolleyballCompetitionSerializer, VolleybalMatchSerializer
from authorizationApp.models import User
from SCSapp.models.MatchTeamResult import MatchTeamResult
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
            match.isAnnounced)]
        serializer = VolleybalMatchSerializer(matches, many=True)
        
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
            if AbstractMatch.objects.get(id=json.loads(request.body)["match_id"]).competition.sportType == Competition.SportTypeChoices.VOLLEYBALL:
                match = VolleyballMatch.objects.get(id=json.loads(request.body)["match_id"])
                response = actionsDict["volleyball"]
            else: return Response({"ERROR": "Нет события для этого вида спорта"})
        except: return Response({"ERROR":"Матч с указанным ID не существует"})

        if match.judge != self.request.auth.user:
            return Response({"ERROR":"Судейство в этом матче недоступно под этой учётной записью"})
        response["teams_data"] = match.getTranslationData()
        response["info"] = socketINFO
        response["WSLink"] = match.startMatch()

        return Response(response)


class CompetitionAPIView(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    def perform_create(self, serializer):
        serializer.save(self.request.auth.user)

class VolleyballCompetitionAPIView(generics.ListCreateAPIView):
    queryset = VolleyballCompetition.objects.all()
    serializer_class = VolleyballCompetitionSerializer

    def perform_create(self, serializer):
        print(self.request.auth.user)
        serializer.save(self.request.auth.user)



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