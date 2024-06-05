import random
from .CorrectInput import input_int
from .CorrectInput import input_float
def input_list():
    """
        Функция для ввода списка с помощью пользовательского ввода. Запрашивается размер списка,
        после чего запрашивается ввод элементов для каждого индекса. Пользователь вводит вещественные числа.
        Параметры: нет
        Возвращает: Список вещественных чисел.
        """
    while True:
        try:
            print("Entry list size")
            size = input_int()
            if size <= 0:
                print("The list size must be greater than zero")
                continue
            break
        except ValueError:
            print()
    lst = []

    for i in range (size):
        while True:
            try:
                print("Input element in list:")
                elem = input_float()
                lst.append(elem)
                break
            except ValueError:
                print()
    return lst

def print_list(lst):
    """
        Функция для вывода списка на экран.
        Параметры:
        - lst: Список элементов.
        Возвращает: Ничего.
        """
    print("Список:", lst)
def generete_random_list():
    """
        Функция для генерации случайного списка.
        Генерируется случайный размер списка от 5 до 12 элементов, и для каждого элемента
        генерируется случайное вещественное число в диапазоне от -10 до 10.
        Параметры: нет
        Возвращает: Список вещественных чисел.
        """
    while True:
        try:
            print("Entry list size")
            size = input_int()
            if size <= 0:
                print("The list size must be greater than zero")
                continue
            break
        except ValueError:
            print()

    for i in range(size):
        yield random.uniform(-10,10)