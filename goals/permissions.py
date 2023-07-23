from typing import Any
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.request import Request

from goals.models import Goal, Category, Comment, Board, BoardParticipant

'''В коде мы:
Определили метод has_object_permission, который должен вернуть True
, если доступ у пользователя есть, и False — если нет.
Если пользователь не авторизован, всегда возвращаем False.
Если метод запроса входит в SAFE_METHODS (которые не изменяют данные, например GET), 
то тогда просто проверяем, 
что существует участник у данной доски.
Если метод не входит (это значит, что мы пытаемся изменить или удалить доску), 
то обязательно проверяем, 
что наш текущий пользователь является создателем доски.'''


class BoardPermission (IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Board) -> bool:
        _filters: dict[str, Any] = {'user': request.user, 'board': obj}
        if request.method not in SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermission(IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Category) -> bool:
        _filters: dict[str, Any] = {'user': request.user, 'board': obj.board}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermission(IsAuthenticated):

    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Goal) -> bool:
        _filters: dict[str, Any] = {'user': request.user, 'board': obj.category.board}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCommentPermission(IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Comment) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user
