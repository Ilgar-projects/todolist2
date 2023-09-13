import pytest

from goals.models import Board


@pytest.mark.django_db
def test_board_model():
    board = Board(title="Test Board")
    assert board.title == "Test Board"
    assert board.is_deleted is False
