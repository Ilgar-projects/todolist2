from django.urls import path

from goals import views

urlpatterns = [
    # Categories
    path('goal_category/create', views.CategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', views.CategoryListView.as_view(), name='categories-list'),
    path('goal_category/<int:pk>', views.CategoryDetailView.as_view(), name='category-details'),
    # Goals
    path('goal/create', views.GoalCreateView.as_view(), name='create-goal'),
    path('goal/list', views.GoalListView.as_view(), name='goal-list'),
    path('goal/<int:pk>', views.GoalDetailView.as_view(), name='goal-details'),
    # Comments
    path('goal_comment/create', views.CommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', views.CommentListView.as_view(), name='comment-list'),
    path('goal_comment/<int:pk>', views.CommentDetailView.as_view(), name='comment-details')
]
