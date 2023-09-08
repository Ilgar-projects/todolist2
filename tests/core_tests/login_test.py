import pytest


@pytest.mark.django_db
def test_login(client):
    user_data = {
        'username': 'test',
        'first_name': 'Test',
        'last_name': 'test',
        'email': 'test@test.ru',
        'password': 'Ss12345678',
        'password_repeat': 'Ss12345678'
    }

    create_user_response = client.post(
        '/core/signup',
        data=user_data,
        content_type='application/json')

    login_user_response = client.post(
        '/core/login',
        {'username': user_data['username'], 'password': user_data['password']},
        content_type='application/json')

    assert create_user_response.status_code == 201
    assert login_user_response.status_code == 200
