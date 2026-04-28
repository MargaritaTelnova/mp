import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


class TestProfileAccess:
    """Тесты доступа к профилю"""

    def test_own_profile_access(self, authenticated_client, user):
        """Тест доступа к своему профилю"""
        url = reverse('profile', kwargs={'username': user.username})
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.context['profile_user'] == user
        assert response.context['is_own_profile'] is True

    def test_friend_profile_access(self, authenticated_client, user, user2):
        """Тест доступа к профилю друга"""
        # Добавляем в друзья
        user.friends.add(user2)

        url = reverse('profile', kwargs={'username': user2.username})
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.context['is_friend'] is True

    def test_stranger_profile_access_denied(self, authenticated_client, user2):
        """Тест отказа в доступе к профилю незнакомца"""
        url = reverse('profile', kwargs={'username': user2.username})
        response = authenticated_client.get(url)

        # Должен быть редирект на список пользователей
        assert response.status_code == 302
        assert response.url == reverse('users_list')

    def test_anonymous_profile_access(self, client, user):
        """Тест доступа анонима к профилю"""
        url = reverse('profile', kwargs={'username': user.username})
        response = client.get(url)

        # Аноним должен быть перенаправлен на страницу входа
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test_nonexistent_profile(self, authenticated_client):
        """Тест доступа к несуществующему профилю"""
        url = reverse('profile', kwargs={'username': 'nonexistent'})
        response = authenticated_client.get(url)
        assert response.status_code == 404


class TestUsersList:
    """Тесты списка пользователей"""

    def test_users_list_authenticated(self, authenticated_client, user, user2):
        """Тест доступа аутентифицированного к списку пользователей"""
        url = reverse('users_list')
        response = authenticated_client.get(url)

        assert response.status_code == 200
        # Текущий пользователь не должен быть в списке
        assert user not in response.context['users']
        assert user2 in response.context['users']

    def test_users_list_anonymous(self, client):
        """Тест доступа анонима к списку пользователей"""
        url = reverse('users_list')
        response = client.get(url)

        # Аноним должен быть перенаправлен на страницу входа
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))


class TestEditProfile:
    """Тесты редактирования профиля"""

    def test_edit_profile_page_access(self, authenticated_client, user):
        """Тест доступа к странице редактирования"""
        url = reverse('edit_profile')
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_edit_profile_anonymous(self, client):
        """Тест доступа анонима к редактированию"""
        url = reverse('edit_profile')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test_successful_profile_update(self, authenticated_client, user):
        """Тест успешного обновления профиля"""
        url = reverse('edit_profile')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '+1234567890',
            'bio': 'This is my bio',
            'birth_date': '1990-01-01'
        }
        response = authenticated_client.post(url, data)

        # Проверяем редирект
        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': user.username})

        # Проверяем обновление данных
        user.refresh_from_db()
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'
        assert user.phone == '+1234567890'
        assert user.bio == 'This is my bio'