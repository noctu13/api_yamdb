from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, \
    TitleViewSet, ClientViewSet, AuthViewSet, TokenViewSet, CommentViewSet, ReviewViewSet

router = DefaultRouter()
router.register('users', ClientViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/email/', AuthViewSet.as_view()),
    path('auth/token/', TokenViewSet.as_view()),
    path('', include(router.urls)),
]
