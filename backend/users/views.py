from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .permissions import CurrentUserOrAdmin
from .serializers import (AvatarSerializer, MyUserSerializer,
                          SubscribeSerializer)
from users.models import Subscribe

User = get_user_model()


class MyUserViewSet(UserViewSet):
    """Представление для пользователей."""
    serializer_class = MyUserSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'me':
            return (CurrentUserOrAdmin(),)
        return super().get_permissions()

    @action(
        ['put'],
        detail=False,
        url_path='me/avatar',
        permission_classes=(CurrentUserOrAdmin,),
        serializer_class=AvatarSerializer,
    )
    def avatar(self, request):
        user = request.user
        serializer = self.get_serializer(
            user, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @avatar.mapping.delete
    def delete_avatar(self, request):
        if request.user.avatar:
            request.user.avatar.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        ['post', 'delete'],
        detail=True,
        url_path='subscribe',
        permission_classes=(CurrentUserOrAdmin,)
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        subscriptions_id = self.kwargs.get('id')
        subscriptions = get_object_or_404(User, id=subscriptions_id)
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                subscriptions,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, subscriptions=subscriptions)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if request.method == 'DELETE':
            to_subscribe = Subscribe.objects.filter(
                subscriptions=subscriptions, user=user)
            if not to_subscribe.exists():
                return Response(
                    f'Вы уже отписаны от {subscriptions}.',
                    status=HTTP_400_BAD_REQUEST
                )
            to_subscribe.delete()
            return Response(status=HTTP_204_NO_CONTENT)

    @action(
        ['get'],
        permission_classes=(CurrentUserOrAdmin,),
        url_path='subscriptions',
        detail=False
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscriptions__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
