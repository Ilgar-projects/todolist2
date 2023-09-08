import pytest


@pytest.mark.django_db
def test_board_detail(client, create_login_user):
    board_create = client.post(
        '/goals/board/create',
        {'title': 'test board'},
        content_type='application/json')

    board_detail_response = client.get(f'/goals/board/{int(board_create.data["id"])}')

    expected_response = {
        'id': board_create.data['id'],
        'participants': board_detail_response.data['participants'],
        'created': board_create.data['created'],
        'updated': board_create.data['updated'],
        'title': 'test board',
        'is_deleted': False
    }

    assert board_create.status_code == 201
    assert board_detail_response.status_code == 200
    assert board_detail_response.data == expected_response
