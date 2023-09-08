import pytest

from core.models import User


@pytest.mark.django_db
def test_sign_up(client):
    user_data = {
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.ru',
        'password': 'Ss12345678',
        'password_repeat': 'Ss12345678'
    }

    create_user_response = client.post(
        '/core/signup',
        data=user_data,
        content_type='application/json')

    user = User.objects.filter(username=user_data['username']).first()

    assert create_user_response.status_code == 201
    assert user.username == user_data['username']
