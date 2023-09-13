import pytest

from core.models import User
from core.serializers import ProfileSerializer
from goals.models import Board, Category
from goals.serializers import CategorySerializer


@pytest.mark.django_db
def test_category_serializer():
    user = User.objects.create(username="test_user")

    board = Board.objects.create(title="Test Board", is_deleted=False)

    category = Category.objects.create(board=board, user=user, title="Test Category")

    serializer = CategorySerializer(category)

    assert serializer.data['user'] == ProfileSerializer(user).data
    assert serializer.data['board'] == board.id
    assert serializer.data['title'] == "Test Category"
