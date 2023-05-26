from rest_framework import serializers
from SCSapp.models.Match import AbstractMatch, VolleyballMatch
from SCSapp.models.Competition import Competition, VolleyballCompetition

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

    def save(self, user):
        organizer = user
        super().save()


class VolleyballCompetitionSerializer(serializers.ModelSerializer):
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = VolleyballCompetition
        fields = ['id', 'name', 'description', 'organizer', 'dateTimeStartCompetition', 'regulations',
                  'numOfRounds', 'roundPointLimit', 'lastRoundPointLimit',
                  'onePointLead', 'twoPointsLead', 'threePointsLead',
                  'onePointLose', 'twoPointsLose', 'threePointsLose']

    def save(self, user):
        organizer = user
        super().save()



class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractMatch
        fields = ["id", "isAnnounced", "matchDateTime", "place", "protocol", "judge", "match_translated_now"]


class VolleybalMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolleyballMatch
        fields = ["id", "isAnnounced", "competition", "matchDateTime", "place", "protocol",
                  "judge", "round_translated_now", "current_round", "match_translated_now"]

