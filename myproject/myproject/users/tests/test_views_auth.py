import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


class TestRegistrationView:
    """Тесты регистрации"""

    def test_registration_page_status(self, client):
        """Тест доступности страницы регистрации"""
        url = reverse('register')
        response = client.get(url)
        assert response.status_code == 200

    def test_successful_registration(self, client, user_data):
        """Тест успешной регистрации"""
        url = reverse('register')
        response = client.post(url, user_data)

        # Проверяем создание пользователя
        assert User.objects.filter(username='newuser').exists()
        user = User.objects.get(username='newuser')
        assert user.email == 'newuser@example.com'
        assert user.first_name == 'New'

        # Проверяем редирект на профиль
        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': 'newuser'})

    def test_registration_auto_login(self, client, user_data):
        """Тест автоматического входа после регистрации"""
        url = reverse('register')
        response = client.post(url, user_data)

        # Проверяем, что пользователь авторизован
        response = client.get(reverse('home'))
        assert response.context['user'].is_authenticated

    def test_invalid_registration(self, client, invalid_user_data):
        """Тест невалидной регистрации"""
        url = reverse('register')
        response = client.post(url, invalid_user_data)

        # Проверяем, что пользователь не создан
        assert not User.objects.filter(username='newuser').exists()

        # Проверяем, что остались на странице регистрации
        assert response.status_code == 200

    def test_registration_duplicate_username(self, client, user, user_data):
        """Тест регистрации с существующим username"""
        user_data['username'] = 'testuser'
        url = reverse('register')
        response = client.post(url, user_data)

        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors


class TestLoginLogoutView:
    """Тесты входа и выхода"""

    def test_login_page_status(self, client):
        """Тест доступности страницы входа"""
        url = reverse('login')
        response = client.get(url)
        assert response.status_code == 200

    def test_successful_login(self, client, user):
        """Тест успешного входа"""
        url = reverse('login')
        response = client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        })

        # Проверяем редирект после входа
        assert response.status_code == 302
        assert response.url == reverse('home')

        # Проверяем, что пользователь авторизован
        response = client.get(reverse('home'))
        assert response.context['user'].is_authenticated

    def test_login_with_redirect_next(self, client, user):
        """Тест входа с редиректом на другую страницу"""
        url = reverse('login') + '?next=' + reverse('profile', kwargs={'username': 'testuser'})
        response = client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        })

        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': 'testuser'})

    def test_failed_login(self, client, user):
        """Тест неудачного входа"""
        url = reverse('login')
        response = client.post(url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })

        # Проверяем, что остались на странице входа
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

        # Проверяем, что пользователь не авторизован
        response = client.get(reverse('home'))
        assert not response.context['user'].is_authenticated

    def test_logout(self, authenticated_client):
        """Тест выхода из системы"""
        url = reverse('logout')
        response = authenticated_client.post(url)

        assert response.status_code == 302
        assert response.url == reverse('home')

        # Проверяем, что пользователь разлогинен
        response = authenticated_client.get(reverse('home'))
        assert not response.context['user'].is_authenticated

    @pytest.mark.parametrize("credentials,expected_status", [
        ({"username": "testuser", "password": "testpass123"}, 302),  # Успех
        ({"username": "testuser", "password": "wrong"}, 200),  # Неудача
        ({"username": "wrong", "password": "testpass123"}, 200),  # Неудача
        ({"username": "", "password": ""}, 200),  # Пустые поля
    ])
    def test_login_parametrized(self, client, user, credentials, expected_status):
        """Параметризованный тест входа"""
        url = reverse('login')
        response = client.post(url, credentials)
        assert response.status_code == expected_status