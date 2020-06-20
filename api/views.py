from rest_framework import viewsets, generics

from rest_framework_jwt.views import ObtainJSONWebToken

from api.models import Client
from api.serializers import (
    ClientSerializer,
    AuthSerializer,
    TokenSerializer,
)


class AuthViewSet(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = AuthSerializer

class TokenViewSet(ObtainJSONWebToken):
    serializer_class = TokenSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
