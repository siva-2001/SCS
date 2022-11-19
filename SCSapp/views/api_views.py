from rest_framework import generics
from SCSapp.models.Olympics import Olympics
from SCSapp.serializers import OlympicsSerializer

class OlympicsAPIView(generics.ListAPIView):
    queryset = Olympics.objects.all()
    serializer_class = OlympicsSerializer