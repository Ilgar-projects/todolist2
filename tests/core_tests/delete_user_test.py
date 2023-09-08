import pytest


@pytest.mark.django_db
def test_delete_user(client):
    user_data = {
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.ru',
        'password': 'Ss1234678',
        'password_repeat': 'Ss12345678'
    }

    create_user_response = client.post(
        '/core/signup',
        data=user_data,
        content_type='application/json')

    login_user_response = client.post(
        '/core/login',
        {'username': 'test', 'password': 'Ss12345678'},
        content_type='application/json')

    user_delete_response = client.delete(
        '/core/profile',
    )

    assert create_user_response.status_code == 201
    assert login_user_response.status_code == 403
    assert user_delete_response.status_code == 403
