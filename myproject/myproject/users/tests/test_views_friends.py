import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


class TestFriendActions:
    """Тесты действий с друзьями"""

    def test_add_friend(self, authenticated_client, user, user2):
        """Тест добавления в друзья"""
        url = reverse('add_friend', kwargs={'username': user2.username})
        response = authenticated_client.get(url)

        # Проверяем редирект
        assert response.status_code == 302
        assert response.url == reverse('profile', kwargs={'username': user2.username})

        # Проверяем, что пользователи стали друзьями
        assert user2 in user.friends.all()
        assert user in user2.friends.all()

    def test_add_self_as_friend(self, authenticated_client, user):
        """Тест добавления самого себя в друзья"""
        url = reverse('add_friend', kwargs={'username': user.username})
        response = authenticated_client.get(url)

        assert response.status_code == 302
        # Сам себя добавить нельзя
        assert user not in user.friends.all()

    def test_add_existing_friend(self, authenticated_client, user, user2):
        """Тест добавления уже существующего друга"""
        # Сначала добавляем в друзья
        user.friends.add(user2)

        url = reverse('add_friend', kwargs={'username': user2.username})
        response = authenticated_client.get(url)

        assert response.status_code == 302
        # Друг уже есть, счетчик не должен измениться
        assert user.friends.count() == 1

    def test_remove_friend(self, authenticated_client, user, user2):
        """Тест удаления из друзей"""
        # Сначала добавляем в друзья
        user.friends.add(user2)
        assert user2 in user.friends.all()

        url = reverse('remove_friend', kwargs={'username': user2.username})
        response = authenticated_client.get(url)

        assert response.status_code == 302
        assert user2 not in user.friends.all()
        assert user not in user2.friends.all()

    def test_remove_nonexistent_friend(self, authenticated_client, user, user2):
        """Тест удаления несуществующего друга"""
        url = reverse('remove_friend', kwargs={'username': user2.username})
        response = authenticated_client.get(url)

        assert response.status_code == 302
        # Ничего не должно измениться
        assert user.friends.count() == 0

    def test_friend_actions_anonymous(self, client, user2):
        """Тест действий с друзьями от анонима"""
        add_url = reverse('add_friend', kwargs={'username': user2.username})
        response = client.get(add_url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

        remove_url = reverse('remove_friend', kwargs={'username': user2.username})
        response = client.get(remove_url)
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))


class TestFriendsList:
    """Тесты списка друзей"""

    def test_friends_count_in_profile(self, authenticated_client, user, user2):
        """Тест отображения количества друзей в профиле"""
        user.friends.add(user2)

        url = reverse('profile', kwargs={'username': user.username})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert response.context['profile_user'].friends.count() == 1

    def test_multiple_friends(self, authenticated_client, user, db):
        """Тест с множеством друзей"""
        # Создаем несколько друзей
        friends = []
        for i in range(3):
            friend = User.objects.create_user(
                username=f'friend{i}',
                email=f'friend{i}@example.com',
                password='testpass123'
            )
            user.friends.add(friend)
            friends.append(friend)

        url = reverse('profile', kwargs={'username': user.username})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert response.context['profile_user'].friends.count() == 3

        for friend in friends:
            assert friend in response.context['profile_user'].friends.all()