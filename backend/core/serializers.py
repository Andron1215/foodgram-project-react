from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )
