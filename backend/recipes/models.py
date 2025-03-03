from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .constants import (MAX_LENGTH_FOR_NAME, MIN_AMOUNT_OF_INGREDIENT,
                        MIN_COOKING_TIME)

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиент."""
    name = models.CharField(
        'Название',
        unique=True,
        max_length=MAX_LENGTH_FOR_NAME
    )
    measurement_unit = models.CharField(
        'Еденица измерения',
        max_length=MAX_LENGTH_FOR_NAME
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тег."""
    name = models.CharField(
        'Название',
        unique=True,
        max_length=MAX_LENGTH_FOR_NAME
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=MAX_LENGTH_FOR_NAME)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепт."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_FOR_NAME
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/recipe_images/'
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                message=f'Значение должно быть не меньше, '
                        f'чем {MIN_COOKING_TIME}.'
            )
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Промежуточная модель для ингредиента в рецепте."""
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredients_list',
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredients_list',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                MIN_AMOUNT_OF_INGREDIENT,
                message=f'Значение должно быть не меньше, '
                        f'чем {MIN_AMOUNT_OF_INGREDIENT}.'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return (
            f'{self.ingredient.name} '
            f'({self.ingredient.measurement_unit}) - {self.amount} '
        )


class Favorite(models.Model):
    """Модель избранное."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепты'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes'], name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipes}" в Избранное.'


class ShoppingCart(models.Model):
    """Модель корзина покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепты',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipes'], name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipes}" в Корзину покупок.'
