from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from .models import Review, Comment, Title, Genre, Category

from .permissions import IsAuthorOrReadOnly
from .serializers import ReviewSerializer, CommentSerializer, TitleReadSerializer, TitleWriteSerializer, CategorySerializer, GenreSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, viewsets, permissions


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
    