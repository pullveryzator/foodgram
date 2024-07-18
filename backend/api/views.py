from django.db.models import Sum
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import baseconv
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import IngredientFilter, RecipeFilter
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import CustomPagination
from .permissions import CurrentUserOrAdmin, CurrentUserOrAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeRecordSerializer, RecipeSimpleSerializer,
                          TagSerializer)
from .utils import create_shopping_list_file


class IngredientViewSet(ModelViewSet):
    """Представление для работы с ингредиентами."""
    queryset = Ingredient.objects.all()
    http_method_names = ['get', ]
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    """Представление для работы с рецептами."""
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Переопределяем встроенный метод выбора сериализатора."""
        if self.action in ('list', 'retrieve',):
            return RecipeReadSerializer
        elif self.action in ('create', 'update', 'partial_update', 'destroy',):
            return RecipeRecordSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        """Переопределяем встроенный метод выбора прав доступа."""
        if self.action in ('list', 'retrieve',):
            return (AllowAny(),)
        elif self.action in ('create', 'update', 'partial_update', 'destroy',):
            return (CurrentUserOrAdminOrReadOnly(),)
        return super().get_permissions()

    @action(
        methods=['get', ],
        detail=True,
        url_path='get-link',
        url_name='get-link',
        permission_classes=(AllowAny,)
    )
    def get_link(self, request, pk=None):
        """Функция получения короткой ссылки."""
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
        methods=['post', 'delete', ],
        detail=True,
    )
    def shopping_cart(self, request, pk=None):
        """Функция выбора метода для работы с корзиной покупок."""
        if request.method == 'POST':
            return self.add_recipe_to(ShoppingCart, request.user, pk)
        return self.delete_recipe_from(ShoppingCart, request.user, pk)

    @action(
        methods=['post', 'delete', ],
        detail=True,
    )
    def favorite(self, request, pk=None):
        """Функция выбора метода для работы с избранным."""
        if request.method == 'POST':
            return self.add_recipe_to(Favorite, request.user, pk)
        return self.delete_recipe_from(Favorite, request.user, pk)

    def add_recipe_to(self, model, user, pk):
        """Фукция добавления рецепта в объект модели."""
        if model.objects.filter(user=user, recipes_id=pk).exists():
            return Response(
                {'errors': f'Рецепт {pk} в {model.__name__} уже добавлен.'},
                status=HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, pk=pk)
        model.objects.create(user=user, recipes=recipe)
        serializer = RecipeSimpleSerializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete_recipe_from(self, model, user, pk):
        """Фукция удаления рецепта из объекта модели."""
        if not Recipe.objects.filter(pk=pk).exists():
            return Response(
                {'errors': f'Рецепта {pk} в базе данных не cуществует.'},
                status=HTTP_404_NOT_FOUND
            )
        if not model.objects.filter(user=user, recipes_id=pk).exists():
            return Response(
                {'errors': f'Рецепта {pk} в {model.__name__} нет.'},
                status=HTTP_400_BAD_REQUEST
            )
        object = get_object_or_404(model, user=user, recipes_id=pk)
        object.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=['get', ],
        detail=False,
        permission_classes=[CurrentUserOrAdmin, ]
    )
    def download_shopping_cart(self, request):
        """Функия для работы с загрузкой файла списка покупок."""
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(
            user=user).values(
                'recipes__ingredients__name',
                'recipes__ingredients__measurement_unit').annotate(
                    amount=Sum('recipes__ingredients_list__amount')).order_by(
                        'recipes__ingredients__name'
        )
        file = create_shopping_list_file(shopping_cart)
        return FileResponse(
            file,
            content_type='text/plain',
            as_attachment=True,
            filename=f'{user}_go_to_shop.txt'
        )


class TagViewSet(ModelViewSet):
    """Представление для работы с тегами."""
    queryset = Tag.objects.all()
    http_method_names = ['get', ]
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class ShortLinkView(APIView):
    """Представление для работы с короткой ссылкой."""
    permission_classes = (AllowAny,)

    def get(self, request, encoded_id):
        """Переопределение встроенного метода get()."""
        decoded_id = baseconv.base64.decode(encoded_id)
        recipe = get_object_or_404(Recipe, id=decoded_id)
        return HttpResponseRedirect(
            request.build_absolute_uri(
                f'/recipes/{recipe.id}/'
            )
        )
