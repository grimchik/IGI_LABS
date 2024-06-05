from SupportFunctions.GenerateList import input_list
from SupportFunctions.GenerateList import generete_random_list
from SupportFunctions.GenerateList import print_list
def find_max_abs_index(lst):
    """
        Функция для нахождения индекса максимального по модулю элемента в списке.
        Параметры: Список элементов.
        Возвращает: Индекс максимального по модулю элемента в списке.
    """
    max_abs_value = max(lst, key=abs)
    return lst.index(max_abs_value)
def sum_after_first_positive(lst):
    """
        Функция для вычисления суммы элементов списка, расположенных после первого положительного элемента.
        Если первый положительный элемент не найден, возвращает 0.
        Параметры: Список элементов.
        Возвращает: Сумму элементов списка, расположенных после первого положительного элемента.
        """
    index_first_positive = next((i for i, x in enumerate(lst) if x > 0), None)
    if index_first_positive is not None:
        return sum(lst[index_first_positive + 1:])
    else:
        return 0
def task5():
    """
        Функция для выполнения задания 5.
        Запрашивается ввод пользователем списка и генерация случайного списка.
        Для каждого списка находится номер максимального по модулю элемента и сумма элементов,
        расположенных после первого положительного элемента. Результаты выводятся на экран.
        Параметры: нет
        Возвращает: Ничего.
    """
    elements = input_list()
    elements2 = list(generete_random_list())
    print_list(elements)
    print_list(elements2)
    max_abs_index = find_max_abs_index(elements)
    max_abs_index2 = find_max_abs_index(elements2)
    print("Номер максимального по модулю элемента списка:", max_abs_index)
    print("Номер максимального по модулю элемента случайно сгенерированного списка:", max_abs_index2+1)
    sum_after_positive = sum_after_first_positive(elements)
    sum_after_positive2 = sum_after_first_positive(elements2)
    print("Сумма элементов списка, расположенных после первого положительного элемента:", sum_after_positive)
    print("Сумма элементов случайно сгенерированного списка, расположенных после первого положительного элемента:", sum_after_positive2)