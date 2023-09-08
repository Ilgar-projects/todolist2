import pytest


@pytest.mark.django_db
def test_unauthorized_user_goal(client, create_category):
    create_goal = client.post('/goals/goal/create',
                              {'title': 'new goal',
                               'category': create_category.data['id']},
                              content_type='application/json')

    client.logout()

    goal_list_result = client.get('/goals/goal/list')
    goal_detail_response = client.get(f'/goals/goal/{int(create_goal.data["id"])}')
    goal_delete_response = client.delete(f'/goals/goal/{int(create_goal.data["id"])}')
    update_goal_response = client.patch(f'/goals/goal/{int(create_goal.data["id"])}',
                                        data={'title': 'updated goal'},
                                        content_type='application/json')

    assert create_goal.status_code == 201
    assert goal_delete_response.status_code == 403
    assert goal_detail_response.status_code == 403
    assert update_goal_response.status_code == 403
    assert goal_list_result.status_code == 403
