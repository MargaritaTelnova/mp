print("1. Декоратор логирования: Создать декоратор logger(func)")
print("=" * 50)

def logger(func):
    def wrapper(*args, **kwargs):
        # Перед вызовом функции
        print(f"Вызов функции {func.__name__} с аргументами {args} и {kwargs}")
        
        # Выполнение функции
        result = func(*args, **kwargs)
        
        # После выполнения функции
        print(f"Функция {func.__name__} вернула {result}")
        return result
    return wrapper

print("Применение декоратора к функциям:")
print("=" * 50)

@logger
def add(a, b):
    return a + b

@logger
def divide(a, b):
    if b == 0:
        return "Ошибка: деление на ноль"
    return a / b

@logger
def greet(name):
    return f"Привет, {name}!"

# Тестирование функций с декоратором
print("Тестирование функции add:")
result1 = add(1, 2)
print()

print("Тестирование функции divide:")
result2 = divide(6, 2)
print()

print("Тестирование функции divide с делением на ноль:")
result3 = divide(5, 0)
print()

print("Тестирование функции greet:")
result4 = greet("Рита")
print()

print("=" * 50)
print("2. Декоратор доступа: Создать декоратор require_role(allowed_roles)")
print("=" * 50)

def require_role(allowed_roles):
    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if user.get('role') in allowed_roles:
                return func(user, *args, **kwargs)
            else:
                print(f"Доступ запрещён пользователю {user['name']}")
                return None
        return wrapper
    return decorator

print("Пример использования декоратора require_role:")
print("=" * 50)

@require_role(['admin'])
def delete_database(user):
    print(f"База данных удалена пользователем {user['name']}")
    return "Операция выполнена успешно"

@require_role(['admin', 'manager'])
def edit_settings(user):
    print(f"Настройки изменены пользователем {user['name']}")
    return "Настройки обновлены"

@require_role(['user', 'admin', 'manager'])
def view_data(user):
    print(f"Данные просмотрены пользователем {user['name']}")
    return "Данные загружены"

print("Создание пользователей с разными ролями:")
print("=" * 50)

# Создание пользователей
users = [
    {'name': 'Маргарита', 'role': 'admin'},
    {'name': 'Юлия', 'role': 'manager'},
    {'name': 'Роман', 'role': 'user'},
    {'name': 'Татьяна', 'role': 'guest'}
]

print("Тестирование доступа для разных пользователей:")
print("=" * 50)

# Тестирование функции delete_database для разных пользователей
print("Функция delete_database (требует роль 'admin'):")
for user in users:
    print(f"Пользователь: {user['name']}, роль: {user['role']}")
    result = delete_database(user)
    if result:
        print(f"Результат: {result}")
    print("-" * 30)

print()

print("Функция edit_settings (требует роли 'admin' или 'manager'):")
for user in users:
    print(f"Пользователь: {user['name']}, роль: {user['role']}")
    result = edit_settings(user)
    if result:
        print(f"Результат: {result}")
    print("-" * 30)

print()

print("Функция view_data (требует роли 'user', 'admin' или 'manager'):")
for user in users:
    print(f"Пользователь: {user['name']}, роль: {user['role']}")
    result = view_data(user)
    if result:
        print(f"Результат: {result}")
    print("-" * 30)

print("=" * 50)
print("Дополнительное тестирование:")
print("=" * 50)

# Дополнительное тестирование с разными аргументами
print("Тестирование функций с дополнительными аргументами:")

@require_role(['admin'])
def create_user(admin_user, username, email):
    print(f"Пользователь {username} создан администратором {admin_user['name']}")
    return f"Создан пользователь: {username} ({email})"

admin_user = {'name': 'Маргарита', 'role': 'admin'}
regular_user = {'name': 'Роман', 'role': 'user'}

print("Создание пользователя администратором:")
result = create_user(admin_user, "new_user", "new@example.com")
print(f"Результат: {result}")
print()

print("Попытка создания пользователя обычным пользователем:")
result = create_user(regular_user, "another_user", "another@example.com")
print(f"Результат: {result}")