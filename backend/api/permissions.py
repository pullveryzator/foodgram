from rest_framework. permissions import (
    BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS,)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_staff))


class CurrentUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) is type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff
