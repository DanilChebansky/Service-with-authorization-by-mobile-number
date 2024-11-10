from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import phone_validator

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Email", **NULLABLE)
    phone = models.CharField(
        unique=True,
        validators=[phone_validator],
        max_length=11,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=100, verbose_name="Город", **NULLABLE, help_text="Введите город"
    )
    invite_code = models.CharField(max_length=6, verbose_name="Инвайт-код", **NULLABLE)
    invite_input = models.CharField(
        max_length=6,
        verbose_name="Введенный инвайт-код",
        **NULLABLE,
        help_text="Введите инвайт-код"
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email