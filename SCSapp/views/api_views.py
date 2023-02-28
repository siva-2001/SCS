from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from SCSapp.models.Olympics import Olympics
from SCSapp.serializers import OlympicsSerializer
from SCSapp.models.Competition import Competition
from SCSapp.models.Match import AbstractMatch
from SCSapp.serializers import CompetitionSerializer
from SCSapp.serializers import MatchSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class OlympicsAPIView(generics.ListAPIView):
    queryset = Olympics.objects.all()
    serializer_class = OlympicsSerializer

class CompetitionAPIView(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

class AnnouncedEventsAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Competition.announced_objects.all()
    serializer_class = CompetitionSerializer

class CurrentOlympicsAPIView(generics.ListAPIView):
    queryset = Olympics.current_objects.all()
    serializer_class = OlympicsSerializer

class CurrentCompetitionAPIView(generics.ListAPIView):
    queryset =  Competition.current_objects.all()
    serializer_class = CompetitionSerializer

class JudgeMatchesAPIView(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        matches = [match for match in AbstractMatch.objects.all() if request.user == match.judge]
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)








