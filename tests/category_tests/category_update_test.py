import pytest


@pytest.mark.django_db
def test_category_update(client, create_login_user):
    board_create = client.post('/goals/board/create', {'title': 'test board'}, content_type='application/json')

    board_detail_response = client.get(f'/goals/board/{int(board_create.data["id"])}')

    create_category = client.post('/goals/goal_category/create',
                                  {'title': 'test category 1',
                                   'board': {int(board_create.data['id'])}},
                                  format='json')

    category_response = client.get(f'/goals/goal_category/{int(create_category.data["id"])}')

    update_category_response = client.patch(f'/goals/goal_category/{int(create_category.data["id"])}',
                                            {'title': 'test category 2'},
                                            content_type='application/json')

    expected_response = {
        'id': create_category.data['id'],
        'user': create_login_user[0].data,
        'created': create_category.data['created'],
        'updated': update_category_response.data['updated'],
        'title': 'test category 2',
        'is_deleted': False,
        'board': board_create.data['id']
    }

    assert board_create.status_code == 201
    assert board_detail_response.status_code == 200
    assert create_category.status_code == 201
    assert category_response.status_code == 200
    assert update_category_response.status_code == 200
    assert expected_response == update_category_response.data
