from pytest_factoryboy import register

from tests.factories import BoardFactory, CategoryFactory, UserFactory

pytest_plugins = 'tests.fixtures'

register(BoardFactory)
register(CategoryFactory)
register(UserFactory)
