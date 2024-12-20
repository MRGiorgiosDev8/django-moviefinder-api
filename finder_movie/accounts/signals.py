"""
Сигналы для приложения accounts.

Этот модуль содержит сигналы, которые автоматически создают и сохраняют профиль пользователя при создании или обновлении объекта CustomUser.

Сигналы:
    create_user_profile: Создает профиль пользователя при создании нового объекта CustomUser.
    save_user_profile: Сохраняет профиль пользователя при сохранении объекта CustomUser.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создает профиль пользователя при создании нового объекта CustomUser.

    Аргументы:
        sender (Model): Модель, отправившая сигнал.
        instance (CustomUser): Экземпляр модели CustomUser.
        created (bool): Флаг, указывающий, был ли создан новый объект.
        **kwargs: Дополнительные аргументы.
    """
    if created:
        UserProfile.objects.create(user=instance)
        print(f"Profile created for {instance.username}")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняет профиль пользователя при сохранении объекта CustomUser.

    Аргументы:
        sender (Model): Модель, отправившая сигнал.
        instance (CustomUser): Экземпляр модели CustomUser.
        **kwargs: Дополнительные аргументы.
    """
    if instance.profile:
        instance.profile.save()