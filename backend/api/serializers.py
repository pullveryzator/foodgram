from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField

from recipes.models import Ingredient, Recipe, Tag, ShoppingCart
from users.serializers import MyUserSerializer


class IngredientSerializer(ModelSerializer):
    amount = SerializerMethodField(read_only=True)

    def get_amount(self, obj):
        return 333

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug',)


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorite = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    def get_is_favorite(self, obj):  # todo
        return False

    def get_is_in_shopping_cart(self, obj):  # todo
        return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags',
            'author', 'ingredients',
            'is_favorite', 'is_in_shopping_cart',
            'name', 'image',
            'text', 'cooking_time',
        )


class ShoppingCartSerializer(ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipes',)
