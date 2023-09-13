import pytest

from core.serializers import LoginSerializer


@pytest.mark.django_db
def test_login_serializer():
    data = {
        'username': 'test_user',
        'password': 'password123'
    }
    serializer = LoginSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data['username'] == 'test_user'
    assert serializer.validated_data['password'] == 'password123'
