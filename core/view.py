from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # поиск по полям 'first_name', 'last_name', 'username'
    search_fields = ['first_name', 'last_name', 'username']
