from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializerCreate(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя, включающий только email и password.
    """

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        """
        Метод для создания нового пользователя с хэшированным паролем.
        """
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределенный сериализатор для получения JWT-токена, включающий в себя email пользователя.
    """

    @classmethod
    def get_token(cls, user):
        """
        Получение JWT-токена с дополнительными полями username и email.
        """
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        return token
