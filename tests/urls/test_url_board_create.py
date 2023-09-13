import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_view(client):
    response = client.post(reverse('create-board'))

    assert response.status_code == 403
    # Проверяем, что возвращается код 403 при отсутствии авторизации пользователя
