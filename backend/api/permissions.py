from rest_framework. permissions import (
    BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated, SAFE_METHODS,)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_staff))


class CurrentUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_staff
                or obj.author == request.user)


class CurrentUserOrAdmin(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff or obj.author == request.user)
