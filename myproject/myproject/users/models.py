from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с email и телефоном
    """
    # Email уже есть в AbstractUser, но сделаем его обязательным
    email = models.EmailField(unique=True, verbose_name='Email')

    # Телефон с валидацией
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )

    # Дополнительные поля для профиля
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

    # Поле для друзей (ManyToMany с самим собой)
    friends = models.ManyToManyField(
        'self',
        symmetrical=True,  # Если A друг B, то B друг A
        blank=True,
        verbose_name='Друзья'
    )

    def __str__(self):
        return self.username

    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']