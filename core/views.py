from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status, exceptions, permissions
from rest_framework.response import Response
from core.models import User
from core.serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # если пользователь не авторизован-выводим ошибку авторизации
        if not (user := authenticate(**serializer.validated_data)):
            raise exceptions.AuthenticationFailed

        login(request=request, user=user)

        return Response(ProfileSerializer(user).data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    # PUT изменение отдельных полей
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def perform_destroy(self, instance: User) -> None:
        logout(self.request)


class UpdatePasswordView(generics.GenericAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response(serializer.data)
