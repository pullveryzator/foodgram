from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import baseconv
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
)
from .permissions import CurrentUserOrAdminOrReadOnly, CurrentUserOrAdmin
from .serializers import (
    IngredientSerializer, RecipeReadSerializer, RecipeRecordSerializer,
    TagSerializer, RecipeSimpleSerializer
)

from recipes.models import Ingredient, Recipe, ShoppingCart, Tag, Favorite
from api.filters import RecipeFilter, IngredientFilter


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    http_method_names = ['get',]
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return RecipeReadSerializer
        elif self.action in ('create', 'update', 'partial_update', 'destroy',):
            return RecipeRecordSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('list', 'retrieve',):
            return (AllowAny(),)
        elif self.action in ('create', 'update', 'partial_update', 'destroy',):
            return (CurrentUserOrAdminOrReadOnly(),)
        return super().get_permissions()

    @action(
        methods=['get',],
        detail=True,
        url_path='get-link',
        url_name='get-link',
        permission_classes=(AllowAny,)
    )
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        encoded_id = baseconv.base64.encode(recipe.id)
        short_link = self.request.build_absolute_uri(
            reverse(
                'short_link',
                kwargs={'encoded_id': encoded_id}
            )
        )
        return Response({"short-link": short_link}, status=HTTP_200_OK)

    @action(
        methods=['post', 'delete',],
        detail=True,
        permission_classes=[CurrentUserOrAdmin,]
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe_to(ShoppingCart, request.user, pk)
        else:
            return self.delete_recipe_from(ShoppingCart, request.user, pk)

    @action(
        methods=['post', 'delete',],
        detail=True,
        permission_classes=[CurrentUserOrAdmin,]
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe_to(Favorite, request.user, pk)
        else:
            return self.delete_recipe_from(Favorite, request.user, pk)

    def add_recipe_to(self, model, user, pk):
        if model.objects.filter(user=user, recipes_id=pk).exists():
            return Response(
                {'errors': f'Рецепт {pk} уже добавлен.'},
                exception=True,
                status=HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, pk=pk)
        model.objects.create(user=user, recipes=recipe)
        serializer = RecipeSimpleSerializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete_recipe_from(self, model, user, pk):
        if not model.objects.filter(user=user, recipes_id=pk).exists():
            return Response(
                {'errors': f'Рецепт {pk} не существует.'},
                status=HTTP_400_BAD_REQUEST
            )
        object = get_object_or_404(model, user=user, recipes_id=pk)
        object.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=['get',],
        detail=True,
        permission_classes=[CurrentUserOrAdmin,]
    )
    def download_shopping_cart(self, request, user):
        return Response('Vot tvoi spisok pokupok s@ka.')


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    http_method_names = ['get',]
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class ShortLinkView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, encoded_id):
        decoded_id = baseconv.base64.decode(encoded_id)
        recipe = get_object_or_404(Recipe, id=decoded_id)
        return HttpResponseRedirect(
            request.build_absolute_uri(
                    f'/api/recipes/{recipe.id}/'
                ), status=HTTP_200_OK
        )
