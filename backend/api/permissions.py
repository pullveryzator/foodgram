from rest_framework.permissions import (SAFE_METHODS,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class CurrentUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Полные права только у автора объекта либо у админа.

    Остальные пользователи - только чтение.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_staff
                or obj.author == request.user)


class CurrentUserOrAdmin(IsAuthenticated):
    """Полные права только у автора объекта либо у админа."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user
