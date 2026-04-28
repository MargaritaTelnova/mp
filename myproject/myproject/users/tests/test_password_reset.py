import pytest
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


class TestPasswordReset:
    """Тесты восстановления пароля"""

    def test_password_reset_form_page(self, client):
        """Тест доступности страницы восстановления пароля"""
        url = reverse('password_reset')
        response = client.get(url)
        assert response.status_code == 200

    def test_password_reset_request(self, client, user):
        """Тест запроса на восстановление пароля"""
        url = reverse('password_reset')
        response = client.post(url, {'email': user.email})

        assert response.status_code == 302
        assert response.url == reverse('password_reset_done')
        assert len(mail.outbox) == 1
        assert user.email in mail.outbox[0].to

    def test_password_reset_invalid_email(self, client):
        """Тест запроса с несуществующим email"""
        url = reverse('password_reset')
        response = client.post(url, {'email': 'nonexistent@example.com'})

        assert response.status_code == 302
        assert response.url == reverse('password_reset_done')