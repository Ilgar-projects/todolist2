import pytest


@pytest.mark.django_db
def test_goals_list(client, create_category):
    create_goal_1 = client.post('/goals/goal/create',
                                {'title': 'new goal 1', 'category': create_category.data['id']},
                                content_type='application/json')

    create_goal_2 = client.post('/goals/goal/create',
                                {'title': 'new goal 2', 'category': create_category.data['id']},
                                content_type='application/json')

    goal_list_response = client.get('/goals/goal/list')

    expected_response = [
        {
            'id': create_goal_1.data['id'],
            'category': create_category.data['id'],
            'created': create_goal_1.data['created'],
            'updated': create_goal_1.data['updated'],
            'title': 'new goal 1',
            'description': None,
            'status': create_goal_1.data['status'],
            'priority': create_goal_1.data['priority'],
            'due_date': create_goal_1.data['due_date'],
            'user': goal_list_response.data[0]['user'],
        },
        {
            'id': create_goal_2.data['id'],
            'category': create_category.data['id'],
            'created': create_goal_2.data['created'],
            'updated': create_goal_2.data['updated'],
            'title': 'new goal 2',
            'description': None,
            'status': create_goal_2.data['status'],
            'priority': create_goal_2.data['priority'],
            'due_date': create_goal_2.data['due_date'],
            'user': goal_list_response.data[1]['user']
        }
    ]

    assert create_goal_1.status_code == 201
    assert create_goal_2.status_code == 201
    assert goal_list_response.status_code == 200
    assert goal_list_response.data == expected_response
