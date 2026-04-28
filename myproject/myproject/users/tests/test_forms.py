import pytest
from users.forms import CustomUserCreationForm
from users.models import CustomUser

pytestmark = pytest.mark.django_db


class TestRegistrationForm:
    """Тесты формы регистрации"""

    def test_valid_form(self, user_data):
        """Тест валидной формы"""
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid()

    def test_invalid_email(self, user_data):
        """Тест невалидного email"""
        user_data['email'] = 'invalid-email'
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_duplicate_email(self, user, user_data):
        """Тест дублирования email"""
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid()
        form.save()

        # Пытаемся создать еще одного с тем же email
        form2 = CustomUserCreationForm(data=user_data)
        assert not form2.is_valid()
        assert 'email' in form2.errors

    def test_password_mismatch(self, user_data):
        """Тест несовпадения паролей"""
        user_data['password2'] = 'different123'
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert 'password2' in form.errors

    def test_weak_password(self, user_data):
        """Тест слабого пароля"""
        user_data['password1'] = '123'
        user_data['password2'] = '123'
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()

    def test_missing_required_fields(self):
        """Тест отсутствия обязательных полей"""
        form = CustomUserCreationForm(data={})
        assert not form.is_valid()
        assert 'username' in form.errors
        assert 'email' in form.errors
        assert 'password1' in form.errors

    @pytest.mark.parametrize("field,value", [
        ('username', 'testuser123'),
        ('email', 'test@example.com'),
        ('first_name', 'John'),
        ('last_name', 'Doe'),
    ])
    def test_required_fields(self, user_data, field, value):
        """Параметризованный тест обязательных полей"""
        user_data[field] = value
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid()