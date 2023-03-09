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
from SCSapp.serializers import CompetitionSerializer
from SCSapp.serializers import MatchSerializer
from SCSapp.models.User import User


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

        print(data)
        return Response(data)


class SignUpAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OlympicsAPIView(generics.ListAPIView):
    queryset = Olympics.objects.all()
    serializer_class = OlympicsSerializer

class CompetitionAPIView(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

# class AnnouncedEventsAPIView(generics.ListAPIView):
class TestAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
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








