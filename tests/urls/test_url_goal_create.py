import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_goal_view(client):
    url = reverse('create-goal')
    response = client.post(url)

    assert response.status_code == 403
    # Проверяем, что возвращается код 403 при попытке доступа к созданию цели
