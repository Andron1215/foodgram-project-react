from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Ingredients, Recipes, Tags
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from users.models import Subscriptions

from .filterts import CustomSearchFilterIngredients, RecipesFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CustomUserReadSerializer,
    IngredientsSerializer,
    RecipesReadSerializer,
    RecipesWriteSerializer,
    SubscriptionsReadSerializer,
    SubscriptionsWriteSerializer,
    TagsSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserReadSerializer

    @action(
        ["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        author = self.get_object()
        user = request.user
        serializer = SubscriptionsWriteSerializer(
            author, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            if request.method == "POST":
                Subscriptions.objects.create(author=author, user=user)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            if request.method == "DELETE":
                subscription = get_object_or_404(
                    Subscriptions, author=author, user=user
                )
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(["get"], detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscriptions__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsReadSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class SubscriptionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsReadSerializer
    permission_classes = [IsAuthenticated]


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
