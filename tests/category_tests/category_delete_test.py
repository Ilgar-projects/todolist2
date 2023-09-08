import pytest


@pytest.mark.django_db
def test_category_delete(client, create_login_user):
    board_create = client.post('/goals/board/create', {'title': 'test board'}, content_type='application/json')

    board_detail_response = client.get(f'/goals/board/{int(board_create.data["id"])}')

    create_category = client.post('/goals/goal_category/create',
                                  {'title': 'test category 1',
                                   'board': {int(board_create.data['id'])}},
                                  format='json')

    category_response = client.get(f'/goals/goal_category/{int(create_category.data["id"])}')

    delete_category_response = client.delete(f'/goals/goal_category/{int(create_category.data["id"])}')
    check_category_response = client.get(f'/goals/goal_category/{int(create_category.data["id"])}')

    assert board_create.status_code == 201
    assert board_detail_response.status_code == 200
    assert create_category.status_code == 201
    assert category_response.status_code == 200
    assert delete_category_response.status_code == 204
    assert check_category_response.status_code == 404
