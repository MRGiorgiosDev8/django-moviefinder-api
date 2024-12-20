from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'avatar']

    def create(self, validated_data):
        """
        Создаёт и возвращает новый экземпляр CustomUser, используя проверенные данные.

        Аргументы:
            validated_data (dict): Проверенные данные для создания нового пользователя.

        Возвращает:
            CustomUser: Созданный экземпляр пользователя.
        """
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Обновляет и возвращает существующий экземпляр CustomUser, используя проверенные данные.

        Аргументы:
            instance (CustomUser): Существующий экземпляр пользователя для обновления.
            validated_data (dict): Проверенные данные для обновления пользователя.

        Возвращает:
            CustomUser: Обновлённый экземпляр пользователя.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance