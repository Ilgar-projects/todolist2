from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, generics
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import Category, Goal, Comment, Board, BoardParticipant
from goals.permissions import BoardPermission, GoalCategoryPermission, GoalPermission, GoalCommentPermission
from goals.serializers import CategoryCreateSerializer, CategorySerializer, GoalSerializer, \
    CommentSerializer, BoardSerializer, BoardWithParticipantsSerializer, GoalWithUserSerializer, CommentCreateSerializer

'''
Если указываешь свойство queryset,  либо определяешь методы get_object/get_queryset,  
то модель у класса вьюхи указывать не нужно - она не будет использоваться
'''


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            board = serializer.save()
            user = self.request.user
            # Проверяем, существует ли уже запись BoardParticipant с указанными значениями user и board
            board_participant_exists = BoardParticipant.objects.filter(user=user, board=board).exists()
            if not board_participant_exists:
                BoardParticipant.objects.create(user=user, board=board)


class BoardListView(generics.ListAPIView):
    permissions = [BoardPermission]
    serializer_class = BoardSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user).exclude(is_deleted=True)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardWithParticipantsSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants__user').exclude(is_deleted=True)

    def perform_destroy(self, instance: Board) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class CategoryCreateView(CreateAPIView):
    model = Category

    # создавать категории можно только авторизованным пользователям.
    permission_classes = [GoalCategoryPermission]
    serializer_class = CategoryCreateSerializer


class CategoryListView(ListAPIView):
    # разрешен доступ только для аутентифицированных пользователей
    permission_classes = [GoalCategoryPermission]
    serializer_class = CategorySerializer
    # позволяет ограничить количество объектов на странице с помощью параметров `limit` и `offset`.
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ]
    # `filterset_fields` - определяет поля, по которым можно сортировать результаты запроса.
    ordering_fields = ["title", "created"]
    ordering = ["title"]  # сортировка по дефолту
    search_fields = ["title"]

    # данный метод возвращает только те объекты модели GoalCategory,
    # которые принадлежат текущему пользователю и не являются удаленными.
    def get_queryset(self):
        return Category.objects.filter(board__participants__user=self.request.user).exclude(is_deleted=True)


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    '''
    GET /goals/goal_category/<pk> — просмотр категории.
    PUT /goals/goal_category/<pk> — обновление категории.
    DELETE /goals/goal_category/<pk> — удаление категории.
    Обратите внимание на параметр <pk>. Он необходим DRF для поиска объекта,
    который мы собираемся просматривать/редактировать/удалять.
    '''

    serializer_class = CategorySerializer
    permission_classes = [GoalCategoryPermission]
    queryset = Category.objects.exclude(is_deleted=True)

    # Чтобы категория не удалялась, при вызове delete,
    # мы определим метод perform_destroy у вью
    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.goal_set.update(status=Goal.Status.archived)


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [GoalPermission]
    serializer_class = GoalSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [GoalPermission]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = GoalDateFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False,
        ).exclude(status=Goal.Status.archived)


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    '''
    GET /goals/goal/<pk> — просмотр категории.
    PUT /goals/goal/<pk> — обновление категории.
    DELETE /goals/goal/<pk> — удаление категории.
    Обратите внимание на параметр <pk>. Он необходим DRF для поиска объекта,
    который мы собираемся просматривать/редактировать/удалять.
    '''

    serializer_class = GoalWithUserSerializer
    permission_classes = [GoalPermission]
    queryset = Goal.objects.exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [GoalCommentPermission]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [GoalCommentPermission]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["goal"]

    # ordering = ["-created"]

    def get_queryset(self):
        return Comment.objects.filter(goal__category__board__participants__user=self.request.user)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    '''
    GET /goals/goal_comment/<pk> — просмотр категории.
    PUT /goals/goal_comment/<pk> — обновление категории.
    DELETE /goals/goal_comment/<pk> — удаление категории.
    Обратите внимание на параметр <pk>. Он необходим DRF для поиска объекта,
    который мы собираемся просматривать/редактировать/удалять.
    '''

    serializer_class = CommentSerializer
    permission_classes = [GoalCommentPermission]
    queryset = Comment.objects.select_related('user')

    def get_queryset(self):
        return Comment.objects.select_related('user').filter(
            goal__category__board__participants__user=self.request.user)
