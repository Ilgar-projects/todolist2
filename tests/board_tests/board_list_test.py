import pytest


@pytest.mark.django_db
def test_boards_list(client, create_login_user):

    board_create_1 = client.post(
        '/goals/board/create',
        {'title': 'test board 1'},
        content_type='application/json'
    )
    board_create_2 = client.post(
        '/goals/board/create',
        {'title': 'test board 2'},
        content_type='application/json'
    )
    board_create_3 = client.post(
        '/goals/board/create',
        {'title': 'test board 3'},
        content_type='application/json'
    )

    expected_response = [
        {
            'id': board_create_1.data['id'],
            'created': board_create_1.data['created'],
            'updated': board_create_1.data['updated'],
            'title': board_create_1.data['title'],
            'is_deleted': False
        },
        {
            'id': board_create_2.data['id'],
            'created': board_create_2.data['created'],
            'updated': board_create_2.data['updated'],
            'title': board_create_2.data['title'],
            'is_deleted': False
        },
        {
            'id': board_create_3.data['id'],
            'created': board_create_3.data['created'],
            'updated': board_create_3.data['updated'],
            'title': board_create_3.data['title'],
            'is_deleted': False
        }
    ]

    boards_list_response = client.get('/goals/board/list')

    assert board_create_1.status_code == 201
    assert board_create_2.status_code == 201
    assert board_create_3.status_code == 201
    assert boards_list_response.data == expected_response
