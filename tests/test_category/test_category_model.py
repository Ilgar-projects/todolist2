import pytest
from datetime import datetime
from core.models import User
from goals.models import Category, Board


@pytest.mark.django_db
def test_category_model():
    board = Board(title="Test Board")
    board.save()

    user = User.objects.create(username="test_user")

    category = Category(board=board, title="Test Category", user=user)
    category.save()

    assert isinstance(category.created, datetime)
    assert isinstance(category.updated, datetime)
    assert category.board == board
    assert category.title == "Test Category"
    assert category.user == user
    assert category.is_deleted is False
