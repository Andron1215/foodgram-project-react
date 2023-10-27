from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Units(models.Model):
    name = models.TextField()


class Ingredients(models.Model):
    name = models.TextField()
    unit = models.ForeignKey(
        Units, related_name="cats", on_delete=models.CASCADE
    )


class Tags(models.Model):
    name = models.TextField()
    color_code = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)


class Recipes(models.Model):
    author = models.ForeignKey(
        User, related_name="recipes", on_delete=models.CASCADE
    )
    name = models.TextField()
    image = models.ImageField(
        upload_to="recipes/images/", null=True, default=None
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredients, through="RecipesIngredients"
    )
    tags = models.ManyToManyField(Tags, through="RecipesTags")
    cooking_time = models.IntegerField()


class RecipesIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class RecipesTags(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
