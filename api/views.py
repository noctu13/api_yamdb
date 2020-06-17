from .models import Category, Genre, Title
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleReadSerializer, TitleWriteSerializer
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminOrReadOnly, ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [IsAdminOrReadOnly, ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # permission_classes = [IsAdminOrReadOnly,]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
