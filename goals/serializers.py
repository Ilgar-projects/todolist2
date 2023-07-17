from rest_framework import serializers
from rest_framework.exceptions import NotFound
from core.serializers import ProfileSerializer
from goals.models import Category, Goal, Comment


class CategoryCreateSerializer(serializers.ModelSerializer):
    ''' Чтобы значение user автоматически подставлялось при создании категории,
      мы можем переопределить поле user, если пробросим через
      default=serializers.CurrentUserDefault()
      значение текущего пользователя. Таким образом, при создании категории в поле user
      будет проставлен тот пользователь, от чьего имени создавалась категория.
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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

class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")



class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_comment(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value

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
