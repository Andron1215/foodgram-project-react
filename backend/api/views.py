from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import Subscription

from .filterts import IngredientFilter, RecipesFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CustomUserSerializer,
    FavoritesSerializer,
    IngredientsSerializer,
    RecipesReadSerializer,
    RecipesWriteSerializer,
    ShoppingCartSerializer,
    SubscriptionsSerializer,
    TagsSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination

    @action(
        ["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        author = self.get_object()
        user = request.user
        serializer = SubscriptionsSerializer(
            author, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            if request.method == "POST":
                Subscription.objects.create(author=author, user=user)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            if request.method == "DELETE":
                subscription = get_object_or_404(
                    Subscription, author=author, user=user
                )
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(["get"], detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribers__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipesReadSerializer
        return RecipesWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        ["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        serializer = FavoritesSerializer(
            recipe, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            if request.method == "POST":
                Favorite.objects.create(user=user, recipe=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            if request.method == "DELETE":
                favorite = get_object_or_404(
                    Favorite, user=user, recipe=recipe
                )
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        ["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()
        serializer = ShoppingCartSerializer(
            recipe, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            if request.method == "POST":
                ShoppingCart.objects.create(user=user, recipe=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            if request.method == "DELETE":
                shopping_cart_recipe = get_object_or_404(
                    ShoppingCart, user=user, recipe=recipe
                )
                shopping_cart_recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit__name")
            .annotate(amount=Sum("amount"))
        )
        print(ingredients)
        shopping_list = "Список покупок\n\n"
        shopping_list += "\n".join(
            [
                (
                    f'- {ingredient["ingredient__name"]} '
                    f'({ingredient["ingredient__measurement_unit__name"]})'
                    f' - {ingredient["amount"]}'
                )
                for ingredient in ingredients
            ]
        )
        response = FileResponse(shopping_list, content_type="txt")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={user.username}_shopping_list.txt"
        return response
