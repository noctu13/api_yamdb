from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api.views import UserViewSet


router = routers.DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
