from django.contrib import admin

from goals.models import Category, Goal, Comment


class CategoryAdmin(admin.ModelAdmin):
    '''
    - list_display определяет, какие поля будут отображаться в списке объектов
    модели GoalCategory. В данном случае, отображаются поля "title", "user", "created" и "updated".
    - search_fields определяет, по каким полям будет выполняться поиск объектов модели
    GoalCategory в административной панели. В данном случае, поиск будет выполняться
    по полям "title" и "user".
    '''

    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(Category, CategoryAdmin)


class GoalAdmin(admin.ModelAdmin):
    ...
    # list_display = ("title", "user", "created", "updated")
    # search_fields = ("title", "user")


admin.site.register(Goal, GoalAdmin)


class CommentAdmin(admin.ModelAdmin):
    ...
    # list_display = ("title", "user", "created", "updated")
    # search_fields = ("title", "user")


admin.site.register(Comment, CommentAdmin)
