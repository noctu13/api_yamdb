from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework import viewsets, generics, filters, pagination, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Category, Genre, Title, Review, Comment, Client
from .serializers import CategorySerializer, GenreSerializer, TitleReadSerializer, TitleWriteSerializer, \
    AuthSerializer, ClientSerializer, TokenSerializer, ReviewSerializer, CommentSerializer
from .permissions import IsAdminClient, IsAdminOrReadOnly, IsAuthorOrReadOnly
from .filters import TitleFilter


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
    queryset = Title.objects.annotate(rating=Avg('review_title__score')).all()
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = Review.objects.filter(title=title)
        return queryset

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))

        if Review.objects.filter(author=request.user, title=title).all().count() != 0:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            if not (1 <= serializer.validated_data['score'] <= 10):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(author=request.user, title=title)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def create(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = Review.objects.get(title=title, id=self.kwargs.get('review_id'))
        queryset = Comment.objects.filter(review=review)
        return queryset
