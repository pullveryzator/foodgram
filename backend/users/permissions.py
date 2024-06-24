from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'create', 'partial_update']:
            return True
        else:
            return False


class IsAuthorOrAdminPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """Object permissions."""
        return (request.user.is_staff or obj.username == request.user)


class CurrentUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff
