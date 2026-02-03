import requests
import matplotlib.pyplot as plt

# 1. Получение данных по API
base_url = 'https://pokeapi.co/api/v2/'
limit = 10
url = f'{base_url}pokemon?limit={limit}'

# Получаем список покемонов
response = requests.get(url)
pokemon_list = response.json()['results']

# 2. Парсинг JSON
data = []

for pokemon in pokemon_list:
    # Получаем детальную информацию о покемоне
    pokemon_details = requests.get(pokemon['url']).json()

    # Получаем статистики покемона
    stats = {}
    for stat in pokemon_details['stats']:
        stats[stat['stat']['name']] = stat['base_stat']

    # Создаем словарь с данными
    pokemon_dict = {
        'id': pokemon_details['id'],
        'name': pokemon_details['name'],
        'height': pokemon_details['height'],
        'weight': pokemon_details['weight'],
        'hp': stats.get('hp', 0),
        'attack': stats.get('attack', 0),
        'defense': stats.get('defense', 0),
        # Дополнительные характеристики (по заданию)
        'speed': stats.get('speed', 0),
        'base_experience': pokemon_details.get('base_experience', 0)
    }

    data.append(pokemon_dict)

# 3. Визуализация
# Подготовка данных для графиков
names = [p['name'].capitalize() for p in data]
hp_values = [p['hp'] for p in data]
attack_values = [p['attack'] for p in data]
defense_values = [p['defense'] for p in data]
weights = [p['weight'] for p in data]
heights = [p['height'] for p in data]
speed_values = [p['speed'] for p in data]

# Создаем фигуру с несколькими графиками
plt.figure(figsize=(15, 10))

# График 1: Линейный график
plt.subplot(2, 3, 1)
plt.plot(names, hp_values, marker='o', color='red')
plt.title('Здоровье (HP) покемонов')
plt.xlabel('Покемоны')
plt.ylabel('HP')
plt.xticks(rotation=45)
plt.grid(True)

# График 2: Точечная диаграмма
plt.subplot(2, 3, 2)
plt.scatter(weights, heights, alpha=0.7, color='blue')
for i, pokemon in enumerate(data):
    plt.annotate(
        pokemon['name'].capitalize(),  # Имя покемона с заглавной буквы
        (weights[i], heights[i]),  # Координаты точки (x, y)
        xytext=(5, 5),  # Смещение текста от точки (в пикселях)
        textcoords='offset points',  # Система координат для смещения
        fontsize=6,  # Размер шрифта
        alpha=0.8  # Прозрачность текста
    )
plt.title('Вес vs Рост')
plt.xlabel('Вес')
plt.ylabel('Рост')
plt.grid(True)

# График 3: Столбчатая диаграмма
plt.subplot(2, 3, 3)
plt.bar(names, attack_values, color='green')
plt.title('Атака покемонов')
plt.xlabel('Покемоны')
plt.ylabel('Attack')
plt.xticks(rotation=45)

# График 4: Горизонтальная столбчатая диаграмма
plt.subplot(2, 3, 4)
plt.barh(names, defense_values, color='orange')
plt.title('Защита покемонов')
plt.xlabel('Defense')
plt.ylabel('Покемоны')

# График 5: Гистограмма
plt.subplot(2, 3, 5)
plt.hist(hp_values, bins=15, edgecolor='black', color='purple')
plt.title('Распределение здоровья')
plt.xlabel('Здоровье')
plt.ylabel('Покемоны')
plt.grid(True)

# График 6: Круговая диаграмма
plt.subplot(2, 3, 6)
plt.pie(attack_values, labels=names, autopct='%1.1f%%')
plt.title('Доля атаки каждого покемона')

plt.tight_layout()
plt.show()
print(data)