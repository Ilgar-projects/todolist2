from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from rest_framework import serializers

from core.models import User
from core.serializers import ProfileSerializer
from goals.models import Category, Goal, Comment, Board, BoardParticipant


class BoardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class ParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=BoardParticipant.editable_roles)
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board",)


class BoardWithParticipantsSerializer(BoardSerializer):
    participants = ParticipantSerializer(many=True)

    def update(self, instance: Board, validated_data: dict):
        request_user: User = self.context['request'].user

        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=request_user).delete()
            participants = [
                BoardParticipant(user=participant['user'], role=participant['role'], board=instance)
                for participant in validated_data.get('participants', [])]
            BoardParticipant.objects.bulk_create(participants, ignore_conflicts=True)
            if title := validated_data.get('title'):
                instance.title = title
            instance.save()
        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class CategoryCreateSerializer(serializers.ModelSerializer):
    """ Чтобы значение user автоматически подставлялось при создании категории,
      мы можем переопределить поле user, если пробросим через
      default=serializers.CurrentUserDefault()
      значение текущего пользователя. Таким образом, при создании категории в поле user
      будет проставлен тот пользователь, от чьего имени создавалась категория.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_board(self, board: Board) -> Board:
        if board.is_deleted:
            raise ValidationError('Board not exists')
        if not BoardParticipant.objects.filter(
                board_id=board.id,
                user_id=self.context['request'].user.id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer], ).exists():
            raise PermissionDenied

        return board

    class Meta:
        model = Category

        # read_only — их нельзя изменять.
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


# Новый сериализатор потребовался для того, чтобы убрать логику
# с подстановкой текущего пользователя в поле user
class CategorySerializer(CategoryCreateSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # В сериализаторе создания цели нужно проверять не цель, а категорию,
    # поэтому метод должен называться def validate_category
    def validate_category(self, category):
        if category.is_deleted:
            raise ValidationError('Category not exists')
        if not BoardParticipant.objects.filter(
                board_id=category.board_id,
                user_id=self.context['request'].user.id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer], ).exists():
            raise PermissionDenied

        return category

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalWithUserSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # при создании комментария нужно проверять цель,
    # для которой коммент создается def validate_goal(self, goal)
    # причем проверка цели не на is_deleted, а на статус archived-это исправить в будущем
    def validate_goal(self, goal):
        if goal.status == Goal.Status.archived:
            raise ValidationError('Goal not exists')
        if not BoardParticipant.objects.filter(
            board_id=goal.category.board_id,
            user_id=self.context['request'].user.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists():
            raise PermissionDenied

        return goal

    class Meta:
        model = Comment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    # поле с названием цели будет показано, и чтобы его нельзя было редактировать
    # прописываем это поле только для чтения
    goals = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
