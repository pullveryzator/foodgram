from django.contrib import admin

from .constants import LIST_PER_PAGE, MIN_AMOUNT_OF_INGREDIENT
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientInline(admin.TabularInline):
    min_num = MIN_AMOUNT_OF_INGREDIENT
    model = IngredientInRecipe


class CommonRecipesAdmin(admin.ModelAdmin):
    """Общий класс для админки приложения recipes."""
    list_per_page = LIST_PER_PAGE


class IngredientAdmin(CommonRecipesAdmin):

    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_display_links = ('name',)
    inlines = (IngredientInline,)


class FavoriteAdmin(CommonRecipesAdmin):

    list_display = (
        'user',
        'recipes',
    )


class ShoppingCartAdmin(CommonRecipesAdmin):

    list_display = (
        'user',
        'recipes',
    )


class RecipeAdmin(CommonRecipesAdmin):
    list_display = (
        'name',
        'author',
        'pub_date',
        'count_in_favorite',
    )

    def count_in_favorite(self, obj):
        return Favorite.objects.filter(recipes=obj).count()
    count_in_favorite.short_description = 'раз в избранном'

    search_fields = (
        'name', 'author__username',
        'author__email', 'tags__name',
        'tags__slug',
    )
    list_filter = ('tags',)
    list_display_links = ('name',)
    inlines = (IngredientInline,)


class TagAdmin(CommonRecipesAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_display_links = ('name',)


admin.site.empty_value_display = 'Не задано'
admin.site.site_header = 'Управление проектом "Foodgram"'
admin.site.site_title = 'Foodgram'
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
