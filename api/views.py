from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from rest_framework import viewsets, generics, filters, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import (
    AuthSerializer,
    ClientSerializer,
    TokenSerializer,
    ReviewSerializer, 
    CommentSerializer, 
    TitleReadSerializer, 
    TitleWriteSerializer, 
    CategorySerializer, 
    GenreSerializer
)
from api.permissions import IsAdminClient, IsAuthorOrReadOnly
from .models import Review, Comment, Title, Genre, Category, Client

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
    search_fields = ['username',]
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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminOrReadOnly, ]
    #lookup_field = 'slug'
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['name', ]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [IsAdminOrReadOnly, ]
    #lookup_field = 'slug'
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['name', ]

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # permission_classes = [IsAdminOrReadOnly,]
    #filter_backends = [DjangoFilterBackend]
    #filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,) 
    #permission_classes = [IsAdminOrReadOnly, ]
    #lookup_field = ''
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['', ]

    def get_queryset(self):
        title = get_object_or_404(Title, id = self.kwargs.get('title_id'))
        queryset = Review.objects.filter(title=title)
        return queryset 

    def create(self, request, *args, **kwargs):
        
        title = get_object_or_404(Title, id = self.kwargs.get('title_id'))
        serializer = TitleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #permission_classes = [IsAdminOrReadOnly, ]
    #lookup_field = 'review'
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['', ]

    def get_queryset(self):
        title = get_object_or_404(Title, id = self.kwargs.get('title_id'))
        review = Review.objects.get(title=title, id = self.kwargs.get('review_id'))
        queryset = Comment.objects.filter(review=review)
        return queryset 

