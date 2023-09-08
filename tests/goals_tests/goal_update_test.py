import pytest


@pytest.mark.django_db
def test_update_goal(client, create_category):
    create_goal = client.post('/goals/goal/create',
                              {'title': 'new goal', 'category': create_category.data['id']},
                              content_type='application/json')

    goal_response = client.get(f'/goals/goal/{create_goal.data["id"]}')

    goal_update_response = client.patch(f'/goals/goal/{create_goal.data["id"]}',
                                        {'title': 'new goal 2',
                                         'description': 'updated description'},
                                        content_type='application/json')

    expected_response = {
        'id': create_goal.data['id'],
        'category': create_category.data['id'],
        'created': create_goal.data['created'],
        'updated': goal_update_response.data['updated'],
        'title': 'new goal 2',
        'description': 'updated description',
        'status': create_goal.data['status'],
        'priority': create_goal.data['priority'],
        'due_date': create_goal.data['due_date'],
        'user': goal_response.data['user']
    }

    assert create_goal.status_code == 201
    assert goal_response.status_code == 200
    assert goal_update_response.data == expected_response