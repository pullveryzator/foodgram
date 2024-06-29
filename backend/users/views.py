from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


from .serializers import (
    MyUserSerializer, AvatarSerializer,
    # SubscribeReadSerializer, SubscribeRecordSerializer,
    SubscribeSerializer
)
from users.models import Subscribe

User = get_user_model()


class MyUserViewSet(UserViewSet):
    serializer_class = MyUserSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(
        ['put'],
        detail=False,
        url_path='me/avatar',
        permission_classes=(IsAuthenticated,),
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
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ['post', 'delete'],
        detail=True,
        url_path='subscribe',
        permission_classes=(IsAuthenticated,)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscriptions = get_object_or_404(
                Subscribe,
                user=user,
                subscriptions=subscriptions
            )
            subscriptions.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ['get'],
        permission_classes=(IsAuthenticated,),
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
