from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from constants import UsersModels


class User(AbstractUser):
    first_name = models.CharField(
        _("first name"), max_length=UsersModels.max_len_user_first_name.value
    )
    last_name = models.CharField(
        _("last name"), max_length=UsersModels.max_len_user_last_name.value
    )
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="Автор",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Подписчик",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "user"], name="unique_subscription"
            )
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.subscriber} подписан на {self.user}"
