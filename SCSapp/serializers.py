from rest_framework import serializers
from SCSapp.models.Olympics import Olympics
from SCSapp.models.Match import AbstractMatch
from SCSapp.models.Competition import Competition
from SCSapp.models.User import User

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




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            # email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user