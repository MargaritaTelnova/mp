import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.forms import CustomUserCreationForm

User = get_user_model()
pytestmark = pytest.mark.django_db


class TestErrors:
    """Тесты обработки ошибок"""

    def test_404_for_nonexistent_profile(self, authenticated_client):
        """Тест 404 для несуществующего профиля"""
        url = reverse('profile', kwargs={'username': 'nonexistent123'})
        response = authenticated_client.get(url)
        assert response.status_code == 404

    def test_validation_error_for_duplicate_email(self, user, user_data):
        """Тест ошибки валидации дубликата email"""
        user_data['email'] = user.email
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_form_error_for_weak_password(self, user_data):
        """Тест ошибки формы для слабого пароля"""
        user_data['password1'] = '123'
        user_data['password2'] = '123'
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert 'password2' in form.errors

    def test_login_error_message(self, client, user):
        """Тест сообщения об ошибке при входе"""
        url = reverse('login')
        response = client.post(url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })

        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_missing_required_registration_fields(self):
        """Тест отсутствия обязательных полей при регистрации"""
        form = CustomUserCreationForm(data={})
        assert not form.is_valid()
        required_fields = ['username', 'email', 'password1', 'password2']
        for field in required_fields:
            assert field in form.errors