from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filterts import CustomSearchFilterIngredients, RecipesFilter
from .models import Ingredients, Recipes, Tags
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientsSerializer,
    RecipesReadSerializer,
    RecipesWriteSerializer,
    TagsSerializer,
)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None
    filter_backends = [CustomSearchFilterIngredients]
    search_fields = ["^name"]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = {"name": ["startswith"]}


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipesReadSerializer
        return RecipesWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
