from rest_framework import serializers
from SCSapp.models.Olympics import Olympics
from SCSapp.models.Competition import Competition
import traceback

class OlympicsSerializer(serializers.ModelSerializer):
    dateTimeStartOlympics = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Olympics
        fields = ['name', 'type']



class CompetitionSerializer(serializers.ModelSerializer):
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Competition
        fields = ['name', 'description', 'organizer', 'dateTimeStartCompetition', 'sportType', 'type', 'regulations']
