from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    phone = models.CharField(max_length=100, verbose_name="Телефон", **NULLABLE)
    city = models.CharField(max_length=100, verbose_name="Город", **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    chat_id = models.CharField(max_length=250, verbose_name="Номер чата", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
