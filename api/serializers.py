from rest_framework import serializers
from .models import Review, Comment, Title, Category, Genre

class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        fields = ('id', 'title', 'text', 'score','author', 'pub_date')
        model = Review

class CommentSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        fields = ('id', 'review', 'text', 'pub_date', 'author')
        model = Comment

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre

class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title

class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all(), required=False)
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
