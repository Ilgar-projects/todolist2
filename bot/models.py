import os

from django.db import models

from core.models import User
from goals.models import Category


class TgUser(models.Model):
    chat_id = models.BigIntegerField(verbose_name='Chat ID', unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=50, null=True, blank=True, default=None)
    state = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)

    @staticmethod
    def _generate_verification_code() -> str:
        return os.urandom(12).hex()

    def set_verification_code(self) -> str:
        code = self._generate_verification_code()
        self.verification_code = code
        self.save(update_fields=('verification_code',))
        return code
