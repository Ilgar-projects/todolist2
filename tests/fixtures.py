import pytest


@pytest.fixture
def create_login_user(client):
    user_data = {
        'username': 'test',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@test.ru',
        'password': '1q2w3eR$',
        'password_repeat': '1q2w3eR$'
    }
    create_user_response = client.post('/core/signup', data=user_data, content_type='application/json')
    login_user_response = client.post(
        '/core/login',
        {
            'username': user_data['username'],
            'password': user_data['password']
        },
        content_type='application/json'
    )

    return create_user_response, login_user_response


@pytest.fixture
def create_another_user(client):
    user_data = {
        'username': 'test2',
        'first_name': 'Test',
        'last_name': 'test',
        'email': 'test@test.ru',
        'password': 'test12234567',
        'password_repeat': 'test12234567'
    }

    create_user_response = client.post(
        '/core/signup',
        data=user_data,
        content_type='application/json')

    return create_user_response


@pytest.fixture
def create_board(client, create_login_user):
    create_board_response = client.post(
        '/goals_tests/board/create',
        data={'title': 'test_board'},
        content_type='application/json'
    )
    return create_board_response


@pytest.fixture
def create_category(client, create_board):
    create_category = client.post(
        '/goals_tests/goal_category/create',
        {
            'title': 'test_category',
            'board': create_board.data['id']
        },
        format='application/json'
    )
    return create_category


@pytest.fixture
def create_goal(client, create_category):
    create_goal = client.post(
        '/goals_tests/goal/create',
        {
            'title': 'test_goal',
            'category': create_category.data['id']
        },
        content_type='application/json'
    )

    return create_goal
