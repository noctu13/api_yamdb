from .models import Category, Genre, Title
from .filters import TitleFilter
from .serializers import CategorySerializer, GenreSerializer, TitleReadSerializer, TitleWriteSerializer
from django_filters.rest_framework import DjangoFilterBackend

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework import viewsets, generics, filters, pagination, mixins
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
from .permissions import IsAdminClient, IsAdminOrReadOnly


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
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]
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


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
