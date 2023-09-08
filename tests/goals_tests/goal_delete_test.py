import pytest


@pytest.mark.django_db
def test_delete_goal(client, create_category):
    create_goal = client.post('/goals/goal/create',
                              {'title': 'new goal', 'category': create_category.data['id']},
                              content_type='application/json')

    goal_response = client.get(f'/goals/goal/{create_goal.data["id"]}')

    goal_delete_response = client.delete(f'/goals/goal/{create_goal.data["id"]}',
                                         content_type='application/json')

    check_delete_response = client.get(f'/goals/goal/{create_goal.data["id"]}')

    assert create_goal.status_code == 201
    assert goal_response.status_code == 200
    assert goal_response.data['title'] == 'new goal'
    assert goal_delete_response.status_code == 204
    assert check_delete_response.status_code == 404