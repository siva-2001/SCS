from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from SCSapp.models.Olympics import Olympics
from SCSapp.serializers import OlympicsSerializer
from SCSapp.models.Competition import Competition
from SCSapp.serializers import CompetitionSerializer

class OlympicsAPIView(generics.ListAPIView):
    queryset = Olympics.objects.all()
    serializer_class = OlympicsSerializer

class CompetitionAPIView(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
