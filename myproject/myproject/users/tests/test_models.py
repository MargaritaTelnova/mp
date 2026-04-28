import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from users.models import CustomUser

pytestmark = pytest.mark.django_db


class TestUserModel:
    """Тесты модели пользователя"""

    def test_create_user(self, user):
        """Тест создания обычного пользователя"""
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self, admin_user):
        """Тест создания суперпользователя"""
        assert admin_user.is_superuser is True
        assert admin_user.is_staff is True

    def test_user_str_method(self, user):
        """Тест строкового представления пользователя"""
        assert str(user) == 'testuser'

    def test_get_full_name(self, user):
        """Тест метода get_full_name"""
        assert user.get_full_name() == 'Test User'

        user.first_name = ''
        user.save()
        assert user.get_full_name() == 'testuser'

    def test_unique_email_constraint(self, db, user):
        """Тест уникальности email"""
        with pytest.raises(Exception):
            CustomUser.objects.create_user(
                username='testuser2',
                email='test@example.com',  # Существующий email
                password='testpass123'
            )

    def test_phone_field_validation(self, db):
        """Тест валидации телефона"""
        user = CustomUser.objects.create_user(
            username='phoneuser',
            email='phone@example.com',
            password='testpass123'
        )

        # Валидный телефон
        user.phone = '+1234567890'
        user.full_clean()  # Не должно быть исключения

        # Невалидный телефон (слишком длинный)
        user.phone = '+12345678901234567890'
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_friends_relationship(self, user, user2):
        """Тест добавления в друзья"""
        assert user.friends.count() == 0
        user.friends.add(user2)
        assert user.friends.count() == 1
        assert user2 in user.friends.all()

        # Проверка симметричности
        assert user in user2.friends.all()

    def test_remove_friend(self, user, user2):
        """Тест удаления из друзей"""
        user.friends.add(user2)
        assert user in user2.friends.all()

        user.friends.remove(user2)
        assert user.friends.count() == 0
        assert user2.friends.count() == 0


class TestUserModelParametrized:
    """Параметризованные тесты модели"""

    @pytest.mark.parametrize("username,email,phone", [
        ("user1", "user1@test.com", "+1234567890"),
        ("user2", "user2@test.com", "+9876543210"),
        ("user3", "user3@test.com", None),
    ])
    def test_create_multiple_users(self, db, username, email, phone):
        """Параметризованный тест создания разных пользователей"""
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password='testpass123',
            phone=phone
        )
        assert user.username == username
        assert user.email == email
        assert user.phone == phone