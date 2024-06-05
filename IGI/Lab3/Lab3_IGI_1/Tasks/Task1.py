import math
from SupportFunctions.CorrectInput import input_float
def factorial (x):
    """
    Функция для рекурсивного вычисления факториала числа.
    Параметры: основание факториала
    Возвращает: значение факториала
    """
    if x==1:
        return 1
    else:
        return x*factorial(x-1)

def sin_x(x,eps,sin_res):
    """
        Функция считает сумму ряда для синуса.
        Параметры: значение X, точность и значение math.sin(x)
        Возвращает: Вычисленную сумму ряда и количество просуммированных членов ряда
    """
    iteration = 0
    result = 0.0
    while abs(sin_res - result) > eps and iteration <=500:
        result += pow(-1,iteration)*((pow(x,2*iteration+1))/factorial(2*iteration+1))
        iteration += 1
    return result,iteration
def task1():
    """
    Функция для выполнения 1 задания. Запрашивается на ввод икс и точность.
    Вычисляется значение синуса и вызывает функцию для подсчета суммы ряда для синуса.
    Результаты выводится на экран.
    Параметры: нет
    Возвращает: Ничего
    """
    print("Input X : ")
    x = input_float()
    print("Input EPS : ")
    eps = input_float()
    sin_res = math.sin(x)
    result, iterations = sin_x(x, eps, sin_res)
    print("x | n | F(x) | Math F(x) | eps")
    print(f"{x} | {iterations} | {result} | {sin_res} | {eps}")
