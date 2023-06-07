from rest_framework import serializers

from core.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
