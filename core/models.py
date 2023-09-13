from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомная модель пользователя"""
    REQUIRED_FIELDS = []
