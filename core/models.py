from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""
    # чтобы поле email было уникальным
    # email = models.EmailField(unique=True, null=True)
    REQUIRED_FIELDS = []
