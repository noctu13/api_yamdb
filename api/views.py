from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework import viewsets, generics, filters, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Client
from api.serializers import (
    AuthSerializer,
    ClientSerializer,
    TokenSerializer,
)
from api.permissions import IsAdminClient, IsModeratorClient


class AuthViewSet(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = AuthSerializer

    def perform_create(self, serializer):
        email_to = serializer.validated_data['email']
        confirmation_code = get_random_string()
        serializer.save(
            confirmation_code=confirmation_code,
            is_active=False
        )
        send_mail(
            'Yambd account activation',
            'confirmation_code: ' + confirmation_code,
            'admin@yambd.com',
            [email_to],
            fail_silently=False,
        )

class TokenViewSet(TokenObtainPairView):
    serializer_class = TokenSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminClient]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username',]
    pagination_class = pagination.PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], permission_classes = [IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = ClientSerializer(request.user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = ClientSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
