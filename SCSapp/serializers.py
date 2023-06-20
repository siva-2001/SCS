from rest_framework import serializers
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.models.Competition import Competition, VolleyballCompetition
from SCSapp.models.VolleyballTeam import VolleyballTeam
from SCSapp.models.Player import VolleyballPlayer
from SCSapp.models.Faculty import Faculty

# from SCSapp.models.Olympics import Olympics
# class OlympicsSerializer(serializers.ModelSerializer):
#     dateTimeStartOlympics = serializers.DateTimeField(read_only=True)
#     organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Olympics
#         fields = ['name', 'description','type']

class CompetitionSerializer(serializers.ModelSerializer):
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Competition
        fields = ['id', 'name', 'description', 'organizer', 'dateTimeStartCompetition', 'sportType', 'type', 'regulations']



class VolleyballCompetitionSerializer(serializers.ModelSerializer):
    # organizer = serializers.ForeignKeyField(default=serializers.CurrentUserDefault())

    # organizer = serializers.SlugRelatedField(
    #     default=serializers.CurrentUserDefault(),
    #     read_only=True,
    #     # slug_field='id'
    # )
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    dateTimeStartCompetition = serializers.DateTimeField(format="%H:%M %d.%m.%Y", required=False)
    class Meta:
        model = VolleyballCompetition
        fields = ['id', 'name', 'description', 'status', 'organizer',
                  'dateTimeStartCompetition', 'regulations', 'protocol',
                  'numOfRounds', 'roundPointLimit', 'lastRoundPointLimit',
                  'onePointLead', 'twoPointsLead', 'threePointsLead',
                  'onePointLose', 'twoPointsLose', 'threePointsLose']

    # def save(self, user=None):
    #     organizer = user
    #     super().save()


#
# class MatchSerializer(serializers.ModelSerializer):
#
#
#     class Meta:
#         model = AbstractMatch
#         fields = ["id", "isAnnounced", "matchDateTime", "place", "protocol", "judge", "match_translated_now"]
#

class VolleyballMatchSerializer(serializers.ModelSerializer):
    matchDateTime = serializers.DateTimeField(format="%H:%M %d.%m.%Y", required=False)
    isAnnounced = serializers.BooleanField(read_only=True)
    round_translated_now = serializers.BooleanField(read_only=True)
    match_translated_now = serializers.BooleanField(read_only=True)
    class Meta:
        model = VolleyballMatch
        fields = ["id", "isAnnounced", "competition", "matchDateTime", "place", "protocol", "competitionStage",
                  "judge", "round_translated_now", "current_round", "match_translated_now"]

class VolleyballTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolleyballTeam
        fields = ["participant", "competition", "completed_games", "won", "lost", "score", "confirmed"]

class VolleyballPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolleyballPlayer
        fields = ["name", "surename", "patronymic", "team", 'age', 'height', 'weight']

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name', 'emblem', "description"]