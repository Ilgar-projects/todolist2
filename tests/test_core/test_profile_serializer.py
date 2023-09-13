import pytest
from core.models import User
from core.serializers import ProfileSerializer


@pytest.mark.django_db
def test_profile_serializer():
    user = User.objects.create(username="test_user", first_name="John", last_name="Doe", email="johndoe@example.com")
    serializer = ProfileSerializer(instance=user)

    expected_data = {
        'id': user.id,
        'username': 'test_user',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com'
    }

    assert serializer.data == expected_data
