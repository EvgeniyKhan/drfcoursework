from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import MyTokenObtainPairSerializer, UserSerializer, UserSerializerCreate


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Представление для получения JWT-токена.
    """
    serializer_class = MyTokenObtainPairSerializer


class UserListAPIView(ListAPIView):
    """
    Представление для получения списка пользователей.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    """
    Представление для создания нового пользователя.
    """
    serializer_class = UserSerializerCreate
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления пользователя по идентификатору.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
