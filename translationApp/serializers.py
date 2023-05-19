from SCSapp.models.MatchActions import MatchAction

class MatchActionSerializer(serializers.ModelSerializer):
    class Meta:
            model = MatchAction
            fields = ["eventType", "match", "team"]