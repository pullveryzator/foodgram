from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from djoser.permissions import CurrentUserOrAdminOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


from .serializers import MyUserSerializer, AvatarSerializer
from .permissions import UserPermission, IsAuthorOrAdminPermission
from users.models import Subscribe

User = get_user_model()


class MyUserViewSet(UserViewSet):
    serializer_class = MyUserSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == "me":
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(
        ["put"],
        detail=False,
        url_path="me/avatar",
        permission_classes=[IsAuthenticated],
        serializer_class=AvatarSerializer,
    )
    def avatar(self, request):
        user = request.user
        serializer = self.get_serializer(
            user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @avatar.mapping.delete
    def delete_avatar(self, request):
        if request.user.avatar:
            request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
