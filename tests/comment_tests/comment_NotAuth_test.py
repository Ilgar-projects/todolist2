import pytest


@pytest.mark.django_db
def test_unauthorized_user_comment(client, create_goal):
    create_comment = client.post('/goals/goal_comment/create',
                                 {'text': 'new comment',
                                  'goal': create_goal.data['id']},
                                 content_type='application/json')
    client.logout()

    comment_list_result = client.get('/goals/goal_comment/list')
    comment_detail_response = client.get(f'/goals/goal_comment/{int(create_comment.data["id"])}')
    comment_delete_response = client.delete(f'/goals/goal_comment/{int(create_comment.data["id"])}')
    update_comment_response = client.patch(f'/goals/goal_comment/{int(create_comment.data["id"])}',
                                           data={'title': 'updated comment'},
                                           content_type='application/json')

    assert create_comment.status_code == 201
    assert comment_delete_response.status_code == 403
    assert comment_detail_response.status_code == 403
    assert update_comment_response.status_code == 403
    assert comment_list_result.status_code == 403
