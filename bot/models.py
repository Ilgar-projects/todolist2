from django.db import models
# from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from core.models import User


# User = get_user_model()


class TgUser(models.Model):
    chat_id = models.PositiveBigIntegerField(primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    verification_code = models.CharField(max_length=20, unique=True, null=True, blank=True)

    @property
    def is_verified(self) -> bool:
        return bool(self.user)

    @staticmethod
    def _generate_verification_code() -> str:
        return get_random_string(20)

    def update_verification_code(self) -> None:
        self.verification_code = self._generate_verification_code()
        self.save(update_fields=['verification_code'])

    def __str__(self):
        return f'{self.__class__.__name__} ({self.chat_id})'


# class VerificationCode(models.Model):
#     verification_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
#     tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
#     expired_date = models.DateTimeField()
#     is_valid = models.BooleanField(default=False)

