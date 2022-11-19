from rest_framework import serializers
from SCSapp.models.Olympics import Olympics

class OlympicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Olympics
        fields = ['name', 'type']
