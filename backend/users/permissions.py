from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class CurrentUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Полные права только у автора объекта либо у админа.

    Остальные пользователи - только чтение.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) is type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff


class CurrentUserOrAdmin(IsAuthenticated):
    """Полные права только у автора объекта либо у админа."""
    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff or obj.author == request.user)
