from django_filters import rest_framework as filters

from recipes.models import Ingredients, Recipes, Tags


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="startswith")

    class Meta:
        model = Ingredients
        fields = ["name"]


class RecipesFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tags.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )

    class Meta:
        model = Recipes
        fields = ["tags", "author", "is_favorited", "is_in_shopping_cart"]

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset
