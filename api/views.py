from rest_framework import viewsets

from api.models import Client
from api.serializers import ClientSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
