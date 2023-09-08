import pytest


@pytest.mark.django_db
def test_delete_comment(client, create_goal):
    create_comment = client.post('/goals/goal_comment/create',
                                 {'text': 'new comment',
                                  'goal': create_goal.data['id']},
                                 content_type='application/json')

    comment_response = client.get(f'/goals/goal_comment/{create_comment.data["id"]}')

    comment_delete_response = client.delete(f'/goals/goal_comment/{create_comment.data["id"]}')

    check_delete_response = client.get(f'/goals/goal_comment/{create_comment.data["id"]}')

    assert create_comment.status_code == 201
    assert comment_response.status_code == 200
    assert comment_delete_response.status_code == 204
    assert check_delete_response.status_code == 404
