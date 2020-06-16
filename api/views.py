from .models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer
from rest_framework import filters, viewsets


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


class TitleViewSet(viewsets.GenericViewSet):
    pass
