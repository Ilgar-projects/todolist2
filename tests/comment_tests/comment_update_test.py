import pytest


@pytest.mark.django_db
def test_update_comment(client, create_goal):
    create_comment = client.post('/goals/goal_comment/create',
                                 {'text': 'new comment',
                                  'goal': create_goal.data['id']},
                                 content_type='application/json')

    comment_response = client.get(f'/goals/goal_comment/{create_comment.data["id"]}')

    comment_update_response = client.patch(f'/goals/goal_comment/{create_comment.data["id"]}',
                                           {'text': 'new comment updated'},
                                           content_type='application/json')

    expected_response = {
        'id': create_comment.data['id'],
        'user': comment_response.data['user'],
        'created': create_comment.data['created'],
        'updated': comment_update_response.data['updated'],
        'text': 'new comment updated',
        'goal': create_goal.data['id']
    }

    assert create_comment.status_code == 201
    assert comment_response.status_code == 200
    assert comment_update_response.status_code == 200
    assert comment_update_response.data == expected_response
