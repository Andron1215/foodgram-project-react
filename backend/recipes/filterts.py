from django_filters import rest_framework as django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import filters

from .models import (
    Recipes,
    Tags,
)


class CustomSearchFilterIngredients(filters.SearchFilter):
    search_param = "name"


class RecipesFilter(FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tags.objects.all(),
    )

    class Meta:
        model = Recipes
        fields = ["author", "tags"]
