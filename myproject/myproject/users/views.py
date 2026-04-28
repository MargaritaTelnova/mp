from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import CustomUser


def register(request):
    """
    Регистрация с автоматическим входом
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически логиним пользователя после регистрации
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация успешно завершена.')
            return redirect('profile', username=user.username)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def home(request):
    """
    Главная страница
    """
    return render(request, 'home.html')


# ... предыдущие импорты и функции ...

@login_required
def profile_view(request, username):
    """
    Просмотр профиля пользователя
    - Свою страницу можно смотреть всегда
    - Страницу друга можно смотреть
    - Страницу чужого нельзя смотреть
    """
    viewed_user = get_object_or_404(CustomUser, username=username)
    current_user = request.user

    # Проверяем права доступа
    can_view = False

    if current_user == viewed_user:
        # Свою страницу всегда можно смотреть
        can_view = True
    elif viewed_user in current_user.friends.all():
        # Страницу друга можно смотреть
        can_view = True
    else:
        # Чужую страницу нельзя
        can_view = False

    if not can_view:
        messages.error(request, 'У вас нет доступа к этой странице. Добавьте пользователя в друзья.')
        return redirect('users_list')

    # Проверяем, являются ли они друзьями (для отображения кнопки)
    is_friend = viewed_user in current_user.friends.all()

    context = {
        'profile_user': viewed_user,
        'is_own_profile': current_user == viewed_user,
        'is_friend': is_friend,
    }
    return render(request, 'users/profile.html', context)


@login_required
def users_list(request):
    """
    Список всех пользователей (только для аутентифицированных)
    """
    # Исключаем текущего пользователя из списка
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'users/users_list.html', {'users': users})


@login_required
def add_friend(request, username):
    """
    Добавление пользователя в друзья
    """
    friend = get_object_or_404(CustomUser, username=username)
    current_user = request.user

    if current_user == friend:
        messages.error(request, 'Нельзя добавить самого себя в друзья')
    elif friend in current_user.friends.all():
        messages.warning(request, f'{friend.username} уже у вас в друзьях')
    else:
        current_user.friends.add(friend)
        messages.success(request, f'{friend.username} добавлен в друзья!')

    return redirect('profile', username=username)


@login_required
def remove_friend(request, username):
    """
    Удаление пользователя из друзей
    """
    friend = get_object_or_404(CustomUser, username=username)
    current_user = request.user

    if friend in current_user.friends.all():
        current_user.friends.remove(friend)
        messages.success(request, f'{friend.username} удален из друзей')
    else:
        messages.warning(request, f'{friend.username} не у вас в друзьях')

    return redirect('profile', username=username)


@login_required
def edit_profile(request):
    """
    Редактирование своего профиля
    """
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.bio = request.POST.get('bio')
        user.birth_date = request.POST.get('birth_date') or None

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile', username=user.username)

    return render(request, 'users/edit_profile.html', {'user': request.user})