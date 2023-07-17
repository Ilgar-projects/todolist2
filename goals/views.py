from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import Category, Goal, Comment
from goals.serializers import CategoryCreateSerializer, CategorySerializer, GoalCreateSerializer, GoalSerializer, CommentCreateSerializer, CommentSerializer


class CategoryCreateView(CreateAPIView):
    model = Category

    # создавать категории можно только авторизованным пользователям.
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryCreateSerializer


class CategoryListView(ListAPIView):
    model = Category

    # разрешен доступ только для аутентифицированных пользователей
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = CategorySerializer
    # позволяет ограничить количество объектов на странице с помощью параметров `limit` и `offset`.
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # `filterset_fields` - определяет поля, по которым можно сортировать результаты запроса.
    ordering_fields = ["title", "created"]
    ordering = ["title"]  # сортировка по дефолту
    search_fields = ["title"]

    # данный метод возвращает только те объекты модели GoalCategory,
    # которые принадлежат текущему пользователю и не являются удаленными.
    def get_queryset(self):
        return Category.objects.select_related('user').filter(user=self.request.user).exclude(is_deleted=True)


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    '''
    GET /goals/goal_category/<pk> — просмотр категории.
    PUT /goals/goal_category/<pk> — обновление категории.
    DELETE /goals/goal_category/<pk> — удаление категории.
    Обратите внимание на параметр <pk>. Он необходим DRF для поиска объекта,
    который мы собираемся просматривать/редактировать/удалять.
    '''

    model = Category
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    # данный метод вернет только `GoalCategory` записи, которые принадлежат текущему
    # пользователю и не были помечены как удаленные.
    def get_queryset(self):
        return Category.objects.select_related('user').exclude(is_deleted=True)

    # Чтобы категория не удалялась, при вызове delete,
    # мы определим метод perform_destroy у вью
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = GoalDateFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
        )


class GoalDetailView(RetrieveUpdateDestroyAPIView):
    '''
    GET /goals/goal/<pk> — просмотр категории.
    PUT /goals/goal/<pk> — обновление категории.
    DELETE /goals/goal/<pk> — удаление категории.
    Обратите внимание на параметр <pk>. Он необходим DRF для поиска объекта,
    который мы собираемся просматривать/редактировать/удалять.
    '''

    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    # данный метод вернет только записи, которые принадлежат текущему
    # пользователю и не были помечены как удаленные.
    def get_queryset(self):
        return Goal.objects.select_related('user').filter(category__is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["goal"]
    ordering = ["-created"]

    def get_queryset(self):
        return Comment.objects.select_related('user').filter(user=self.request.user)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    '''
    GET /goals/goal_comment/<pk> — просмотр категории.
    PUT /goals/goal_comment/<pk> — обновление категории.
    DELETE /goals/goal_comment/<pk> — удаление категории.
    Обратите внимание на параметр <pk>. Он необходим DRF для поиска объекта,
    который мы собираемся просматривать/редактировать/удалять.
    '''

    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.select_related('user')

