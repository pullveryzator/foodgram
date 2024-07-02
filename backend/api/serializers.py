from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Ingredient, Recipe, Tag, ShoppingCart
from users.serializers import MyUserSerializer


class IngredientForRecipeReadSerializer(ModelSerializer):
    amount = SerializerMethodField(read_only=True)

    def get_amount(self, obj):
        return 333

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientForRecipeRecordSerializer(ModelSerializer):
    amount = SerializerMethodField(read_only=True)

    def get_amount(self, obj):
        return 555

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagForRecipeRecordSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id',)


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug',)


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientForRecipeReadSerializer(many=True, read_only=True)
    is_favorite = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    image = Base64ImageField(required=True)

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


class RecipeRecordSerializer(ModelSerializer):
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientForRecipeRecordSerializer(
        read_only=True, many=True
    )
    tags = TagForRecipeRecordSerializer(read_only=True, many=True)
    image = Base64ImageField(required=True)

    def validate_image(self, value):
        if not value:
            raise ValidationError(message='Передано пустое поле image.')
        return value

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'author',
            'image', 'name',
            'text', 'cooking_time',
        )


class ShoppingCartSerializer(ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipes',)
