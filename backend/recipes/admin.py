from django.contrib import admin

from .models import (
    Ingredient, IngredientInRecipe, Recipe,
    Tag, ShoppingCart, Favorite
)


class IngredientInline(admin.TabularInline):
    model = IngredientInRecipe


class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'measurement_unit',
    )
    list_per_page = 15
    list_display_links = ('name',)
    inlines = (IngredientInline,)


class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'recipes',
    )


class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'recipes',
    )


class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'author',
        'pub_date',
    )
    list_per_page = 15
    list_display_links = ('name',)
    inlines = (IngredientInline,)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_per_page = 15
    list_display_links = ('name',)


admin.site.empty_value_display = 'Не задано'
admin.site.site_header = 'Управление проектом "Foodgram"'
admin.site.site_title = 'Foodgram'
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
