import pytest


@pytest.mark.django_db
def test_board_delete(client, create_login_user):
    board_create = client.post(
        '/goals/board/create',
        {'title': 'test board'},
        content_type='application/json')

    board_detail_response = client.delete(f'/goals/board/{int(board_create.data["id"])}')

    assert board_create.status_code == 201
    assert board_detail_response.status_code == 204
