from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register('users', views.ClientViewSet)

urlpatterns = [
    path('auth/email/', views.AuthViewSet.as_view()),
    path('', include(router.urls)),
]
