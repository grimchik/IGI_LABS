import math
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import stats
from SupportClasses.Correctinput import CorrectInput

class SequenceAnalyzer:
    """
    Класс для анализа последовательностей чисел и выполнения статистического анализа.
    """
    def __init__(self, sequence):
        """
        Инициализирует объект SequenceAnalyzer с заданной последовательностью.

        Args:
        - sequence (list): Входная последовательность для анализа.
        """
        self.sequence = sequence

    @staticmethod
    def factorial(x):
        """
        Статический метод для вычисления факториала числа x.

        Args:
        - x (int): Число, для которого вычисляется факториал.

        Returns:
        - int: Значение факториала числа x.
        """
        if x == 1:
            return 1
        else:
            return x * SequenceAnalyzer.factorial(x - 1)

    @staticmethod
    def calculate_sin_x(x, eps, sin_res, seq):
        """
        Статический метод для вычисления синуса числа x с заданной точностью eps с использованием ряда Тейлора.
        Записывает промежуточные значения в последовательность seq.

        Args:
        - x (float): Число, для которого вычисляется синус.
        - eps (float): Точность вычисления.
        - sin_res (float): Значение синуса числа x (для сравнения).
        - seq (list): Пустой список для записи промежуточных значений.

        Returns:
        - tuple: Кортеж, содержащий результат вычисления синуса и количество итераций.
        """
        iteration = 0
        result = 0.0
        while abs(sin_res - result) > eps and iteration <= 500:
            value = pow(-1, iteration) * ((pow(x, 2 * iteration + 1)) / SequenceAnalyzer.factorial(2 * iteration + 1))
            seq.append(value)
            result += value
            iteration += 1

        return result, iteration

    @staticmethod
    def mean(seq):
        """
        Статический метод для вычисления среднего значения (среднего арифметического) для заданной последовательности.

        Args:
        - seq (list): Последовательность чисел.

        Returns:
        - float: Среднее значение последовательности.
        """
        return np.mean(seq)

    @staticmethod
    def median(seq):
        """
        Статический метод для вычисления медианы для заданной последовательности.

        Args:
        - seq (list): Последовательность чисел.

        Returns:
        - float: Медиана последовательности.
        """
        return np.median(seq)

    @staticmethod
    def mode(seq):
        """
        Статический метод для вычисления моды для заданной последовательности.

        Args:
        - seq (list): Последовательность чисел.

        Returns:
        - scipy.stats.ModeResult: Объект, содержащий моду и количество встречаемости моды.
        """
        return scipy.stats.mode(seq)

    @staticmethod
    def variance(seq):
        """
        Статический метод для вычисления дисперсии для заданной последовательности.

        Args:
        - seq (list): Последовательность чисел.

        Returns:
        - float: Дисперсия последовательности.
        """
        return np.var(seq)

    @staticmethod
    def std_deviation(seq):
        """
        Статический метод для вычисления стандартного отклонения для заданной последовательности.

        Args:
        - seq (list): Последовательность чисел.

        Returns:
        - float: Стандартное отклонение последовательности.
        """
        return np.std(seq)

def Task3():
    """
    Выполняет анализ синуса числа x, используя ряд Тейлора, и проводит статистический анализ полученной последовательности.
    Затем визуализирует результаты сравнения полученной функции с математической функцией синуса.
    """
    print("Input X : ")
    x = CorrectInput.input_float()
    print("Input EPS : ")
    sequence = list()
    eps = CorrectInput.input_float()
    sin_res = math.sin(x)
    result, iterations = SequenceAnalyzer.calculate_sin_x(x, eps, sin_res, sequence)
    print("x | n | F(x) | Math F(x) | eps")
    print(f"{x} | {iterations} | {result} | {sin_res} | {eps}")
    mean = SequenceAnalyzer.mean(sequence)
    median = SequenceAnalyzer.median(sequence)
    mode = SequenceAnalyzer.mode(sequence)
    variance = SequenceAnalyzer.variance(sequence)
    std_deviation = SequenceAnalyzer.std_deviation(sequence)
    print(f"Mean: {mean}")
    print(f"Median: {median}")
    print(f"Mode: {mode}")
    print(f"Variance: {variance}")
    print(f"Standard Deviation: {std_deviation}")
    x_values = np.linspace(-2 * np.pi, 2 * np.pi, 400)
    y_sequence = [SequenceAnalyzer.calculate_sin_x(val, eps, math.sin(val), sequence)[0] for val in x_values]
    y_math = [math.sin(val) for val in x_values]
    plt.plot(x_values, y_sequence, label='F(x) from series', color='blue')
    plt.plot(x_values, y_math, label='Math F(x)', color='red')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.title('Comparison of F(x) from series and Math F(x)')
    plt.legend()
    plt.grid(True)
    plt.savefig('drow.png')
    plt.show()
