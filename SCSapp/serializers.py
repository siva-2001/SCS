from rest_framework import serializers
from SCSapp.models.Olympics import Olympics
from SCSapp.models.Match import AbstractMatch
from SCSapp.models.Competition import Competition
import traceback

class OlympicsSerializer(serializers.ModelSerializer):
    dateTimeStartOlympics = serializers.DateTimeField(read_only=True)
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Olympics
        fields = ['name', 'description','type']

class CompetitionSerializer(serializers.ModelSerializer):
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Competition
        fields = ['name', 'description', 'organizer', 'dateTimeStartCompetition', 'sportType', 'type', 'regulations']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractMatch
        fields = ["id", "isAnnounced", "competition", "matchDateTime", "place", "protocol", "judge"]