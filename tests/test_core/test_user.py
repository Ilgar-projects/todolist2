import pytest
from django.contrib.auth.models import AbstractUser
from core.models import User


@pytest.mark.django_db
def test_user_model():
    user = User(username="test_user", first_name="John", last_name="Doe", email="johndoe@example.com")
    assert isinstance(user, AbstractUser)
    assert user.REQUIRED_FIELDS == []
