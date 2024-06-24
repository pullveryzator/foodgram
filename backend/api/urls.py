from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredientViewSet, RecipeViewSet, TagViewSet, ShoppingCartViewSet,
)

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/download_shopping_cart/', ShoppingCartViewSet.as_view(
        {'get': 'list', 'post': 'partial_update', 'del': 'partial_update'}
    ))
]
