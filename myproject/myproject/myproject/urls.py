from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Аутентификация
    path('auth/password_reset/',
         auth_views.PasswordResetView.as_view(
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
         ),
         name='password_reset'),

    path('auth/', include('django.contrib.auth.urls')),

    # Регистрация
    path('register/', views.register, name='register'),

    # Соцсеть
    path('', views.home, name='home'),
    path('users/', views.users_list, name='users_list'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/add/', views.add_friend, name='add_friend'),
    path('profile/<str:username>/remove/', views.remove_friend, name='remove_friend'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)