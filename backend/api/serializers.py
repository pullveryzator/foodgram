from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic
from django.core.exceptions import ValidationError
from rest_framework import status
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

    def validate(self, data):
        request_method = self.context['request'].method
        required_fields = (
            'ingredients', 'tags',
            'image', 'name',
            'text', 'cooking_time'
        )
        if request_method in ('PATCH', 'POST'):
            for field in required_fields:
                if field not in data:
                    raise ValidationError(
                        message=f'Поле {field} обязательно в запросе.',
                        code=status.HTTP_400_BAD_REQUEST
                    )
            return data

    def validate_image(self, value):
        if not value:
            raise ValidationError(
                message='Поле image не может быть пустым.',
                code=status.HTTP_400_BAD_REQUEST
            )
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError(
                message='Нужен хотя бы один тег.',
                code=status.HTTP_400_BAD_REQUEST
            )
        if len(tags) != len(set(tags)):
            raise ValidationError(
                message='Теги должны быть уникальными.',
                code=status.HTTP_400_BAD_REQUEST
            )
        return value

    def validate_ingredients(self, value):
        ingredients = value
        for ingredient in ingredients:
            object = Ingredient.objects.filter(id=ingredient['id'])
            if not object.exists():
                raise ValidationError(
                    message=f'Ингредиент {ingredient["id"]} не существует.',
                    code=status.HTTP_400_BAD_REQUEST
                )
        if not ingredients:
            raise ValidationError(
                message='Нужен хотя бы один ингредиент.',
                code=status.HTTP_400_BAD_REQUEST
            )
        unique_values = set([ingredient['id'] for ingredient in ingredients])
        if len(unique_values) != len(ingredients):
            raise ValidationError(
                message='Ингредиенты должны быть уникальными.',
                code=status.HTTP_400_BAD_REQUEST
            )
        return value

    @atomic
    def create_ingredients_in_recipe(self, ingredients, recipe):
        for ingredient in ingredients:
            value = Ingredient.objects.filter(id=ingredient['id'])
            IngredientInRecipe.objects.create(
                ingredient=value.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            )

    @atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_in_recipe(
            ingredients=ingredients,
            recipe=recipe
        )
        return recipe

    @atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_in_recipe(
            ingredients=ingredients,
            recipe=instance
        )
        instance.save()
        return instance

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
