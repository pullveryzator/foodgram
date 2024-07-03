from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.fields import SerializerMethodField, IntegerField
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    Ingredient, IngredientInRecipe, Recipe, Tag, ShoppingCart
)
from users.serializers import MyUserSerializer


class IngredientForRecipeReadSerializer(ModelSerializer):
    amount = SerializerMethodField(read_only=True)

    def get_amount(self, obj):
        amount = obj.ingredients_list.last().amount
        return amount

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientForRecipeRecordSerializer(ModelSerializer):
    id = IntegerField(write_only=True)

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount',)


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug',)


class RecipeReadSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientForRecipeReadSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)
    image = Base64ImageField(required=True)

    def get_is_favorited(self, obj):  # todo
        return False

    def get_is_in_shopping_cart(self, obj):  # todo
        return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags',
            'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image',
            'text', 'cooking_time',
        )


class RecipeRecordSerializer(ModelSerializer):
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientForRecipeRecordSerializer(many=True)
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField(required=True)

    def validate_image(self, value):
        if not value:
            raise ValidationError(message='Поле image не может быть пустым.')
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError('Нужен хотя бы один тег.')
        if len(tags) != len(set(tags)):
            raise ValidationError('Теги должны быть уникальными.')
        return value

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError('Нужен хотя бы один ингредиент.')
        unique_values = set([ingredient['id'] for ingredient in ingredients])
        if len(unique_values) != len(ingredients):
            raise ValidationError('Ингредиенты должны быть уникальными.')
        return value

    def create_ingredients_amounts(self, ingredients, recipe):
        IngredientInRecipe.objects.bulk_create(
            [IngredientInRecipe(
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount'],
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_amounts(recipe=recipe, ingredients=ingredients)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'author',
            'image', 'name', 'id',
            'text', 'cooking_time',
        )


class ShoppingCartSerializer(ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipes',)
