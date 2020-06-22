from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
]
