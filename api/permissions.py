from rest_framework import permissions

from api.models import Role

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user == obj #надо подкрутить
                or request.user.role == Role.MODERATOR
                or request.user.role == Role.ADMIN)
