import django_filters
from django.db import models
from django_filters import rest_framework
from goals.models import Goal


class GoalDateFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {
            "due_date": ["lte", "gte"],
            "category": ["in"],
            "status": ["in"],
            "priority": ["in"],
        }
    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }