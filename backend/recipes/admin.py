from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag,
    Unit,
)


class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "color", "slug"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name", "color", "slug"]


class UnitAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name"]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "measurement_unit"]
    list_display_links = ["id", "name", "measurement_unit"]
    search_fields = ["id", "name", "measurement_unit"]
    list_filter = ["measurement_unit"]


class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "tags",
        "author",
        "ingredients",
        "name",
        "image",
        "text",
        "cooking_time",
    ]
    list_display_links = ["id", "tags", "author", "ingredients"]
    search_fields = ["id", "tags", "author", "ingredients", "name", "text"]
    list_filter = ["tags", "author", "ingredients"]


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe", "tag"]
    list_display_links = ["id", "recipe", "tag"]
    search_fields = ["id", "recipe", "tag"]


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe", "ingredient", "amount"]
    list_display_links = ["id", "recipe", "ingredient"]
    search_fields = ["id", "recipe", "ingredient"]


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe", "user"]
    list_display_links = ["id", "recipe", "user"]
    search_fields = ["id", "recipe", "user"]


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe", "user"]
    list_display_links = ["id", "recipe", "user"]
    search_fields = ["id", "recipe", "user"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
