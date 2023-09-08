import logging

import factory
from factory import Faker
from pytest_factoryboy import register

from goals_tests.models import Board, GoalCategory

logger = logging.getLogger('faker')
logger.setLevel(logging.INFO)


@register
class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика по созданию экземпляра модели User"""
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = ''

    class Meta:
        model = 'core.User'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = Faker('sentence')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = Faker('sentence')
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)