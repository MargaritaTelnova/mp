import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from users.models import CustomUser

User = get_user_model()

@pytest.fixture
def client():
    """Фикстура клиента"""
    return Client()

@pytest.fixture
def user(db):
    """Фикстура обычного пользователя"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        phone='+1234567890'
    )

@pytest.fixture
def user2(db):
    """Фикстура второго пользователя"""
    return User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123',
        first_name='Test2',
        last_name='User2'
    )

@pytest.fixture
def admin_user(db):
    """Фикстура администратора"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )

@pytest.fixture
def authenticated_client(client, user):
    """Фикстура авторизованного клиента"""
    client.login(username='testuser', password='testpass123')
    return client

@pytest.fixture
def friend_user(db, user, user2):
    """Фикстура пользователей, которые являются друзьями"""
    user.friends.add(user2)
    user2.friends.add(user)
    return user, user2

@pytest.fixture
def user_data():
    """Данные для регистрации"""
    return {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'phone': '+9876543210',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!'
    }

@pytest.fixture
def invalid_user_data():
    """Невалидные данные для регистрации"""
    return {
        'username': 'newuser',
        'email': 'invalid-email',
        'first_name': 'New',
        'last_name': 'User',
        'phone': 'invalid',
        'password1': '123',
        'password2': '456'
    }