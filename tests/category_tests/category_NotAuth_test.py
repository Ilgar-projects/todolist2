import pytest


@pytest.mark.django_db
def test_unauthorized_user_cat(client, create_category):
    client.logout()

    category_list_result = client.get('/goals/goal_category/list')
    category_detail_response = client.get(f'/goals/goal_category/{int(create_category.data["id"])}')
    category_delete_response = client.delete(f'/goals/goal_category/{int(create_category.data["id"])}')
    update_category_response = client.patch(f'/goals/goal_category/{int(create_category.data["id"])}',
                                            data={'title': 'updated category'},
                                            content_type='application/json')

    assert create_category.status_code == 201
    assert category_delete_response.status_code == 403
    assert category_detail_response.status_code == 403
    assert update_category_response.status_code == 403
    assert category_list_result.status_code == 403
