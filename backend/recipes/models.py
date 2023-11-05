from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribers"
    )
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )

    def __str__(self):
        return f"{self.subscriber} subscribed to {self.user}"


class Tags(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Units(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.ForeignKey(
        Units, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


from django.core.validators import MinValueValidator


class Recipes(models.Model):
    tags = models.ManyToManyField(Tags, through="RecipesTags")
    author = models.ForeignKey(
        User, related_name="recipes", on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredients, through="RecipesIngredients"
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="recipes/images/")
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.name


class RecipesTags(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} - {self.tag}"


class RecipesIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipes, related_name="recipe_ingredients", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.recipe} - {self.amount} {self.ingredient}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, related_name="favorites", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes, related_name="favorites", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} - {self.recipe}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, related_name="shopping_cart", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes, related_name="shopping_cart", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} - {self.recipe}"
