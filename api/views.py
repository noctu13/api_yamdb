from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from api.models import Client
from api.serializers import ClientSerializer, AuthSerializer


class AuthViewSet(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = AuthSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
