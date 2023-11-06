import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (
    Favorites,
    Ingredients,
    Recipes,
    RecipesIngredients,
    RecipesTags,
    Tags,
    Units,
)
from rest_framework import serializers
from users.models import Subscriptions

User = get_user_model()


class CustomUserReadSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        ]
        read_only_fields = ["email", "username"]

    def get_is_subscribed(self, obj):
        return False


class CustomUserWriteSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        ]


class SubscriptionsReadSerializer(CustomUserReadSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserReadSerializer.Meta):
        fields = [
            *CustomUserReadSerializer.Meta.fields,
            "recipes",
            "recipes_count",
        ]

    def get_recipes(self, user):
        print(user.recipes.all())
        request = self.context.get("request")
        print(request)
        recipes_limit = request.GET.get("recipes_limit")
        recipes = user.recipes.all()
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = RecipesShortSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, user):
        return user.recipes.count()


class SubscriptionsWriteSerializer(serializers.ModelSerializer):
    class Meta(CustomUserReadSerializer.Meta):
        model = Subscriptions
        fields = ["author", "user"]
        read_only_fields = ["author", "user"]

    def validate(self, data):
        request = self.context.get("request")
        author = self.instance
        user = request.user
        if request.method == "POST":
            if Subscriptions.objects.filter(author=author, user=user).exists():
                raise serializers.ValidationError(
                    detail="Вы уже подписаны на этого пользователя."
                )
            if author == user:
                raise serializers.ValidationError(
                    detail="Нельзя подписаться на самого себя."
                )
        if request.method == "DELETE":
            if not Subscriptions.objects.filter(
                author=author, user=user
            ).exists():
                raise serializers.ValidationError(
                    detail="Вы не подписаны на этого пользователя."
                )
        return data

    def to_representation(self, instance):
        serializer = SubscriptionsReadSerializer(
            instance, context={"request": self.context.get("request")}
        )
        return serializer.data


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "name", "color", "slug"]


class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ["id", "name"]


class IngredientsSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Ingredients
        fields = ["id", "name", "measurement_unit"]


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class RecipesIngredientsReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient.id", read_only=True
    )
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit.name"
    )

    class Meta:
        model = RecipesIngredients
        fields = ["id", "name", "measurement_unit", "amount"]


class RecipesIngredientsWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())

    class Meta:
        model = RecipesIngredients
        fields = ["id", "amount"]


class RecipesReadSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = CustomUserReadSerializer(read_only=True)
    ingredients = RecipesIngredientsReadSerializer(
        source="recipe_ingredients", many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = [
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class RecipesWriteSerializer(serializers.ModelSerializer):
    ingredients = RecipesIngredientsWriteSerializer(required=True, many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = [
            "id",
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        ]

    def validate(self, data):
        if not data.get("ingredients"):
            raise serializers.ValidationError(
                {"ingredients": "Обязательное поле."}
            )
        if not data.get("tags"):
            raise serializers.ValidationError({"tags": "Обязательное поле."})

        return data

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                {"ingredients": "Это поле не может быть пустым."}
            )

        ingredients_list = []
        for item in value:
            ingredient = item.get("id")
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    {"ingredients": "Ингридиенты не должны повторяться."}
                )
            ingredients_list.append(ingredient)

        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                {"tags": "Это поле не может быть пустым."}
            )

        tags_set = set(value)
        if len(value) != len(tags_set):
            raise serializers.ValidationError(
                {"tags": "Теги не должны повторяться."}
            )

        return value

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        instance = super().create(validated_data)

        for ingredient in ingredients:
            ingredient_instance = ingredient.get("id")
            amount = ingredient.get("amount")
            RecipesIngredients.objects.create(
                recipe=instance, ingredient=ingredient_instance, amount=amount
            )

        for tag_instance in tags:
            RecipesTags.objects.create(recipe=instance, tag=tag_instance)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        instance.ingredients.clear()
        for ingredient in ingredients:
            ingredient_instance = ingredient.get("id")
            amount = ingredient.get("amount")
            RecipesIngredients.objects.create(
                recipe=instance, ingredient=ingredient_instance, amount=amount
            )

        instance.tags.clear()
        for tag_instance in tags:
            RecipesTags.objects.create(recipe=instance, tag=tag_instance)

        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipesReadSerializer(instance)
        return serializer.data


class RecipesShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipes
        fields = [
            "id",
            "name",
            "image",
            "cooking_time",
        ]
        read_only_fields = [
            "id",
            "name",
            "cooking_time",
        ]


class FavoritesSerializer(RecipesShortSerializer):
    class Meta(RecipesShortSerializer.Meta):
        fields = [*RecipesShortSerializer.Meta.fields]

    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        recipe = self.instance
        if request.method == "POST":
            if Favorites.objects.filter(user=user, recipe=recipe).exists():
                raise serializers.ValidationError(
                    detail="Рецепт уже в избранном."
                )
        if request.method == "DELETE":
            if not Favorites.objects.filter(user=user, recipe=recipe).exists():
                raise serializers.ValidationError(
                    detail="Рецепт нет в избранном."
                )
        return data