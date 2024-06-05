from SupportFunctions.CorrectInput import input_int
def print_decorator(func):
    """
        Декоратор для вывода имени функции и ее результатов до и после вызова.
        Параметры: Функция, которая будет обернута декоратором.
        Возвращает: Результат выполнения функции func.
    """
    def wrapper(*args, **kwargs):
        print("Running function:", func.__name__)
        result = func(*args, **kwargs)
        print("Result:", result)
        return result
    return wrapper
@print_decorator
def avg_value():
    """
    Функция для подсчета среднего арифметического. Запрашиваются на ввод целые числа и вычисляется их среднее арифметическое, для прекращения ввода необходимо ввести 0.
    Параметры: нет
    Возвращает: Среднее арифметическое
    """
    print("Enter an integer, to stop entering enter 0")
    count = 0
    sum = 0
    res = 0.0
    inp = 1
    while (inp != 0):
        print("Input value: ")
        inp = input_int()
        if(inp ==0): break
        count += 1
        sum += inp
        res = sum / count
    return res
def task2():
    """
        Функция для выполнения задания 2. Выводит на экран результат выполнения функции avg_value().
        Параметры:Нет.
        Возвращает:Ничего.
        """
    print(avg_value())