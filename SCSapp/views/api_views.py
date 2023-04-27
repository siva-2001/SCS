from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser

from SCSapp.models.Olympics import Olympics
from SCSapp.serializers import OlympicsSerializer, UserSerializer
from SCSapp.models.Competition import Competition
from SCSapp.models.Match import AbstractMatch
from SCSapp.serializers import MatchSerializer, CompetitionSerializer
from SCSapp.models.User import User
from SCSapp.models.MatchTeamResult import MatchTeamResult
from SCSapp.matchActionsDict import actionsDict



socketINFO = [    # FOR_DEBUG
        "Обмен данными происходит по технологии websocket. В сообщении скорей всего мобилка будет передавать JSON-запись с указанием сигнала и, для событий команд - название команды (участника)",
        "None в button_color окрашивает кнопку в стандартный серый цвет. '_FFFFFF' - нижнее подчёркивание говорит что текст кнопки должен быть белым. Кнопка отмены окрашивается отдельно, смотри фигму",
    ]



class PermissionsAPIView(APIView):
    def get(self, request):
        data = {}
        user = request.user
        data["isAnonymousUser"] = True if (type(user) == AnonymousUser) else False
        if not data["isAnonymousUser"]:
            if user.last_name:
                data["FIO"] = user.last_name + ' ' + ((user.first_name[0]+'.') if user.first_name else "") 
            else: data["FIO"] = 'NoName'
            data["isOrganizer"] = user.groups.filter(name="organizer").exists()
        return Response(data)


class SignUpAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CurrentOlympicsAPIView(generics.ListAPIView):
    queryset = Olympics.current_objects.all()
    serializer_class = OlympicsSerializer

class CurrentCompetitionAPIView(generics.ListAPIView):
    queryset =  Competition.current_objects.all()
    serializer_class = CompetitionSerializer

class JudgeCompetitionsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.GET.get("olympics_id"):
            competitions = [match.competition for match in AbstractMatch.objects.all() 
                if request.user == match.judge and
                match.competition.status == Competition.StatusChoices.CURRENT]       
        else:
            competitions = [match.competition for match in AbstractMatch.objects.all() 
                if request.user == match.judge and
                int(request.GET.get("olympics_id")) == match.competition.olympics.id and
                match.competition.status == Competition.StatusChoices.CURRENT] 

        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)

class JudgeMatchesAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.GET.get("competition_id"): return Response({"error":"Не указан competition_id параметр HTTP-запроса"})
        
        matches = [match for match in AbstractMatch.objects.all() 
            if (request.user == match.judge and 
            int(request.GET.get("competition_id")) == match.competition.id and 
            match.isAnnounced)]
        serializer = MatchSerializer(matches, many=True)
        
        for matchDataDict in serializer.data:
            abstrTeamRes = MatchTeamResult.objects.filter(match = matchDataDict["id"])
            matchDataDict["firstTeam"] = abstrTeamRes[0].team.participant.name
            matchDataDict["secondTeam"] = abstrTeamRes[1].team.participant.name

        return Response(serializer.data)

class MatchManagmentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try: match = AbstractMatch.objects.get(id=request.GET.get("match_id"))
        except: return Response({"ERROR":"Матч с указанным ID не существует"})
        if match.judge != self.request.auth.user: 
            return Response({"ERROR":"Судейство в этом матче недоступно под этой учётной записью"})
    
        if match.competition.sportType == Competition.SportTypeChoices.VOLLEYBALL: 
            response = actionsDict["volleyball"]    # Другие виды спорта
        else: response = {"ERROR":"Нет события для этого вида спорта"}

        teamsResults = [tr for tr in MatchTeamResult.objects.all().filter(match=match)]
        if len(teamsResults) != 2: return Response({"ERROR":"Ошибка сервера: количество команд не равно 2"})
           
        response["teams_data"] = getMatchTranslationData(match)
        response["info"] = socketINFO

        return Response(response)

class OlympicsAPIView(generics.ListAPIView):
    queryset = Olympics.objects.all()
    serializer_class = OlympicsSerializer

class CompetitionAPIView(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    def perform_create(self, serializer):
        serializer.save(self.request.auth.user)

class AnnouncedEventsAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Competition.announced_objects.all()
    serializer_class = CompetitionSerializer