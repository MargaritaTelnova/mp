import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


class TestRedirects:
    """Тесты редиректов"""

    def test_login_redirect_after_registration(self, client, user_data):
        """Тест редиректа после регистрации"""
        url = reverse('register')
        response = client.post(url, user_data)

        # Проверяем редирект на профиль
        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': 'newuser'})

    def test_logout_redirect(self, authenticated_client):
        """Тест редиректа после выхода"""
        url = reverse('logout')
        response = authenticated_client.post(url)

        assert response.status_code == 302
        assert response.url == reverse('home')

    def test_login_redirect_next_param(self, client, user):
        """Тест редиректа с параметром next"""
        login_url = reverse('login') + '?next=' + reverse('profile', kwargs={'username': 'testuser'})
        response = client.post(login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })

        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': 'testuser'})

    def test_access_denied_redirect(self, authenticated_client, user2):
        """Тест редиректа при отказе в доступе"""
        url = reverse('profile', kwargs={'username': user2.username})
        response = authenticated_client.get(url)

        assert response.status_code == 302
        assert response.url == reverse('users_list')

    def test_anonymous_redirect_to_login(self, client, user):
        """Тест редиректа анонима на страницу входа"""
        protected_urls = [
            reverse('users_list'),
            reverse('profile', kwargs={'username': user.username}),
            reverse('edit_profile'),
        ]

        for url in protected_urls:
            response = client.get(url)
            assert response.status_code == 302
            assert reverse('login') in response.url

    def test_friend_action_redirects(self, authenticated_client, user2):
        """Тест редиректов при действиях с друзьями"""
        # Добавление друга
        add_url = reverse('add_friend', kwargs={'username': user2.username})
        response = authenticated_client.get(add_url)
        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': user2.username})

        # Удаление друга
        remove_url = reverse('remove_friend', kwargs={'username': user2.username})
        response = authenticated_client.get(remove_url)
        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': user2.username})

    def test_edit_profile_redirect(self, authenticated_client, user):
        """Тест редиректа после редактирования профиля"""
        url = reverse('edit_profile')
        response = authenticated_client.post(url, {
            'first_name': 'New',
            'last_name': 'Name'
        })

        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': user.username})