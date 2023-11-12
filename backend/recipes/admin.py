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
    list_display = ["name", "color", "slug"]
    search_fields = ["name", "color", "slug"]


class UnitAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "measurement_unit"]
    search_fields = ["name", "measurement_unit"]


class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "name",
        "cooking_time",
        "favorites_added",
    ]
    search_fields = ["author", "name", "text"]
    list_filter = ["tags__name", "ingredients__name"]
    readonly_fields = ["favorites_added"]

    def favorites_added(self, obj):
        return obj.favorites.all().count()

    favorites_added.short_description = "Количество добавлений в избранное"


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ["recipe", "tag"]
    search_fields = ["recipe", "tag"]


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["recipe", "ingredient", "amount"]
    search_fields = ["recipe", "ingredient"]


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["recipe", "user"]
    search_fields = ["recipe", "user"]


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ["recipe", "user"]
    search_fields = ["recipe", "user"]


admin.site.register(Tag, TagAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
