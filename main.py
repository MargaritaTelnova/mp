# # Циклы
# # 1. Вывести на экран таблицу умножения от 1 до 9 с помощью вложенных циклов. Приветствуется красивый вывод с использованием табуляции.
# print("Таблица умножения от 1 до 9:")
# for i in range(1, 10):
#     for j in range(1, 10):
#         print(f"{i * j:3}", end=" ")
#     print()

# # 2. Посчитать сумму всех нечётных чисел от 1 до 100.
# a = 0
# for i in range (0, 101):
#     if i % 2 != 0:
#         a += i
# print('Сумма нечётных чисел от 1 до 100:', a)

# # 3. Запросить у пользователя число n и вывести все его делители.
# n = int(input("Введите число: "))
# print(f"Делители числа {n}:", end=" ")

# for i in range(1, n + 1):
#     if n % i == 0:
#         print(i, end=" ")
# print()

# # 4. Найти факториал числа, введённого пользователем, с помощью цикла.
# j = 1
# n = int(input('Введите число n: '))
# for i in range (1, n+1):
#     j *= i
# print(f"Факториал числа {n}:", j)

# # 5. Сгенерировать последовательность Фибоначчи длиной n и вывести её.
# n = int(input("Введите длину последовательности Фибоначчи: "))
#
# if n <= 0:
#     print("Длина должна быть положительным числом!")
# elif n == 1:
#     print("0")
# elif n == 2:
#     print("0 1")
# else:
#     a, b = 0, 1
#     print(a, b, end=" ")
#
#     for i in range(2, n):
#         c = a + b
#         print(c, end=" ")
#         a, b = b, c










# # Списки
# # 0. Для следующих заданий подготовьте цикл из случайных чисел, как в примере:
# import random
# numbers = [random.randint(-50, 50) for _ in range(10)]


# # 1. Создать список из 10 чисел и вывести только чётные элементы.
# even = [x for x in numbers if x % 2 == 0]
# print(even)


# # 2. Найти максимальное и минимальное число в списке.
# print(f"Мин: {min(numbers)}, Макс: {max(numbers)}")


# # 3. Запросить у пользователя 5 чисел, сохранить в список (используйте .append()), отсортировать его и вывести.
# numbers = []
# for i in range(5):
#     numbers.append(float(input(f"Введите число {i+1}: ")))
#
# numbers.sort()
# print("Отсортированный список:", numbers)


# # 4. Удалить из списка все дубликаты (без использования множеств).
# def remove_duplicates(lst):
#     """Удаляет дубликаты из списка"""
#     result = []
#     for item in lst:
#         if item not in result:
#             result.append(item)
#     return result
#
# numbers = [1, 2, 2, 3, 4, 4, 5, 1, 6, 2]
# unique_numbers = remove_duplicates(numbers)
# print("Исходный список:", numbers)
# print("Без дубликатов:", unique_numbers)
#
#
# # 5. Поменять местами первый и последний элемент списка.
# def swap_first_last(lst):
#     if len(lst) >= 2:
#         lst[0], lst[-1] = lst[-1], lst[0]
#     return lst
#
# numbers = [1, 2, 3, 4, 5]
# print("Исходный список:", numbers)
# swap_first_last(numbers)
# print("После обмена:", numbers)









# # Словари
# # 1. Создать словарь с именами студентов и их оценками, вывести средний балл.
# students = {"Олеся": 100, "Мария": 50, "Иван": 100, "Анна":100, "Олег": 100}
# average = sum(students.values()) / len(students)
# result = f"Оценки: {students}\nСредний балл: {average:.2f}"
# print(result)
#
#
# # 2. Подсчитать количество каждой буквы в строке (словарь: буква → количество). Пользователь сначала с помощью input() вводит строку, затем вы
# # создаете необходимый словарь.
# text = input("Введите строку: ")
#
# letter_count = {}
#
# for char in text:
#     if char.isalpha():
#         char_lower = char.lower()
#         if char_lower in letter_count:
#             letter_count[char_lower] += 1
#         else:
#             letter_count[char_lower] = 1
#
# print("\nКоличество каждой буквы в строке:")
# for letter, count in sorted(letter_count.items()):
#     print(f"'{letter}': {count}")


# # 3. Создать словарь, где ключи – это числа от 1 до 10, а значения – их квадраты.
# a = {}
#
# for i in range(1, 11):
#     a[i] = i ** 2
#
# print("Словарь квадратов:", a)


# # 4. Составить словарь из двух списков: список ключей и список значений.
# keys = ['имя', 'возраст', 'город', 'страна']
# values = ['Оля', '20', 'Ростов', 'Россия']
#
# result_dict = {}
# for i in range(len(keys)):
#     result_dict[keys[i]] = values[i]
#
# print("Словарь из двух списков:")
# print(result_dict)









# # Множества
# # 1. Создать два множества и вывести их пересечение и объединение.
# set1 = {1, 2, 3, 4, 5}
# set2 = {4, 5, 6, 7, 8}
#
# intersection = set1 & set2
# print("Пересечение:", intersection)
#
# union = set1 | set2
# print("Объединение:", union)
#
#
# # 2. Найти все уникальные слова в тексте, введённом пользователем.
# text = input("Введите текст: ")
#
# words = text.split()
# unique_words = set(words)
#
# print(f"Уникальные слова: {unique_words}")


# # 3. Даны два списка. Найти общие элементы с помощью множеств.
# list1 = [1, 2, 3, 4, 5, 6]
# list2 = [4, 5, 6, 7, 8, 9]
#
# set1 = set(list1)
# set2 = set(list2)
# common_elements = set1 & set2
#
# print("Общие элементы:", common_elements)


# # 4. Проверить, является ли одно множество подмножеством другого.
# setA = {1, 2, 3}
# setB = {1, 2, 3, 4, 5}
#
# is_subset = setA <= setB
#
# print(f"A ⊆ B: {is_subset}")


# # 5. Удалить из множества все элементы, которые меньше заданного числа.
# numbers = {1, 5, 3, 8, 2, 9, 4, 7}
# threshold = 5
#
# filtered_set = {x for x in numbers if x >= threshold}
#
# print(f"Результат: {filtered_set}")








# # Комбинированные задания
# # 1. Сгенерировать список из 20 случайных чисел и вывести только уникальные значения.
# import random
# numbers = [random.randint(1, 50) for _ in range(20)]
# unique_numbers = set(numbers)
#
# print(sorted(unique_numbers))


# # 2. Создать словарь, где ключи – это элементы списка, а значения – количество их повторений.
# items = ['дом', 'ключ', 'дом', 'мама', 'мама', 'ключ', 'мост']
#
# count_dict = {}
#
# for item in items:
#     if item in count_dict:
#         count_dict[item] += 1
#     else:
#         count_dict[item] = 1
#
# print("Словарь частот:")
# for item, count in count_dict.items():
#     print(f"  {item}: {count}")


# # 3. Дан список слов. Создать множество из слов, длина которых больше 5 символов.
# words = ['мама', 'яблоко', 'собака', 'крановщик', 'мозг', 'привет']
#
# long_words = {word for word in words if len(word) > 5}
#
# print("Слова длиной > 5 символов:", long_words)


# # 4. Ввести предложение. Сохранить в словарь количество вхождений каждого слова.
# sentence = input("Введите предложение: ")
# words = sentence.split()
#
# word_count = {}
# for word in words:
#     if word in word_count:
#         word_count[word] += 1
#     else:
#         word_count[word] = 1
#
# for word, count in word_count.items():
#     print(f"'{word}' - {count}")


# # 5. Создать список чисел, преобразовать его в множество и обратно в список (убрав дубликаты).
# numbers = [1, 2, 2, 3, 4, 4, 5, 1, 6, 2]
#
# unique_set = set(numbers)
#
# unique_list = list(unique_set)
#
# print("Множество:", unique_set)
# print("Список без дубликатов:", unique_list)


# # 6. Дан словарь "товар – цена". Найти самый дорогой товар.
# products = {'яблоки': 100,'бананы': 80,'апельсины': 120,'груши': 90,'манго': 200}
#
# most_expensive = max(products, key=products.get)
# max_price = products[most_expensive]
#
# print(f"Самый дорогой товар: '{most_expensive}' - {max_price} руб.")


# # 7. Дан список имён. Определить, какие из имён встречаются более одного раза. Какое имя встречается чаще всего.
# names = ['Анна', 'Иван', 'Мария', 'Петр', 'Анна', 'Иван', 'Ольга', 'Иван', 'Мария']
#
# name_count = {}
# for name in names:
#     name_count[name] = name_count.get(name, 0) + 1
#
# print("\nИмена, которые встречаются более одного раза:")
# for name, count in name_count.items():
#     if count > 1:
#         print(f"  {name}: {count} раз(а)")
#
# most_common_name = max(name_count, key=name_count.get)
# most_common_count = name_count[most_common_name]
# print(f"\nСамое частое имя: '{most_common_name}' - {most_common_count} раз(а)")


# # 8. Запросить у пользователя строку и составить словарь: символ → индекс его первого вхождения.
# text = input("Введите строку: ")
#
# char_dict = {}
#
# for index, char in enumerate(text):
#     if char not in char_dict:
#         char_dict[char] = index
#
# print("Словарь (символ → индекс первого вхождения):")
# for char, index in char_dict.items():
#     print(f"  '{char}': {index}")