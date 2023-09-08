import pytest


@pytest.mark.django_db
def test_board_update(client, create_login_user, create_another_user):
    board_create = client.post('/goals/board/create', {'title': 'test board'}, content_type='application/json')
    board_detail_response = client.get(f'/goals/board/{int(board_create.data["id"])}')
    update_board_response = client.put(
        f'/goals/board/{int(board_create.data["id"])}',
        data={
            'participants': [{'role': 3, 'user': create_another_user.data['username'], }],
            'title': 'updated board',
            'is_deleted': False
        },
        content_type='application/json'
    )

    updated_response = client.get(f'/goals/board/{int(board_create.data["id"])}')
    check_added_participant_response = client.get(f'/goals/board/{int(board_create.data["id"])}')
    expected_response = {
        'id': board_create.data['id'],
        'participants': [
            {
                'id': updated_response.data['participants'][0]['id'],
                'role': 1,
                'user': updated_response.data['participants'][0]['user'],
                'created': updated_response.data['participants'][0]['created'],
                'updated': updated_response.data['participants'][0]['updated'],
                'board': board_create.data['id']
            },
            {
                'id': updated_response.data['participants'][1]['id'],
                'role': 3,
                'user': create_another_user.data['username'],
                'created': updated_response.data['participants'][1]['created'],
                'updated': updated_response.data['participants'][1]['updated'],
                'board': board_create.data['id']
            }
        ],
        'created': board_create.data['created'],
        'updated': updated_response.data['updated'],
        'title': 'updated board',
        'is_deleted': False
    }

    assert board_create.status_code == 201
    assert board_detail_response.status_code == 200
    assert update_board_response.status_code == 200
    assert updated_response.data['title'] == 'updated board'
    assert expected_response == check_added_participant_response.data
