from django.urls import include, path
from rest_framework import routers

from .views import (
    CustomUserViewSet,
    IngredientsViewSet,
    RecipesViewSet,
    TagsViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
router.register(r"users", CustomUserViewSet)
router.register(r"tags", TagsViewSet)
router.register(r"ingredients", IngredientsViewSet)
router.register(r"recipes", RecipesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
