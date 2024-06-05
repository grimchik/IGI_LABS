import numpy as np

class Task5:
    """
    Класс Task5 предназначен для выполнения задачи 5.
    """
    def __init__(self, n, m, min_value, max_value):
        """
        Конструктор класса Task5.

        Args:
        - n (int): Количество строк матрицы.
        - m (int): Количество столбцов матрицы.
        - min_value (int): Минимальное значение для генерации случайных элементов матрицы.
        - max_value (int): Максимальное значение для генерации случайных элементов матрицы.

        Returns:
        - None
        """
        self.n = n
        self.m = m
        self.min_value = min_value
        self.max_value = max_value

    def generate_matrix(self):
        """
        Метод generate_matrix() генерирует матрицу размера n x m с случайными значениями.

        Returns:
        - numpy.ndarray: Сгенерированная матрица.
        """
        return np.random.randint(self.min_value, self.max_value, size=(self.n, self.m))

    def filter_negative_odd_elements(self, matrix):
        """
        Метод filter_negative_odd_elements(matrix) фильтрует отрицательные нечетные элементы матрицы.

        Args:
        - matrix (numpy.ndarray): Входная матрица.

        Returns:
        - numpy.ndarray: Отфильтрованные отрицательные нечетные элементы матрицы.
        """
        return matrix[(matrix < 0) & (matrix % 2 != 0)]

    def calculate_sum_of_abs_negative_odd_elements(self, filtered_elements):
        """
        Метод calculate_sum_of_abs_negative_odd_elements(filtered_elements) вычисляет сумму модулей
        отрицательных нечетных элементов матрицы.

        Args:
        - filtered_elements (numpy.ndarray): Отфильтрованные отрицательные нечетные элементы матрицы.

        Returns:
        - int: Сумма модулей отрицательных нечетных элементов матрицы.
        """
        return np.sum(np.abs(filtered_elements))

    def calculate_std_deviation(self, filtered_elements):
        """
        Метод calculate_std_deviation(filtered_elements) вычисляет стандартное отклонение отрицательных нечетных
        элементов матрицы.

        Args:
        - filtered_elements (numpy.ndarray): Отфильтрованные отрицательные нечетные элементы матрицы.

        Returns:
        - tuple: Кортеж, содержащий стандартное отклонение, вычисленное с использованием функции np.std() и
        стандартное отклонение, вычисленное по формуле.
        """
        std_dev_function = np.std(filtered_elements)
        mean = np.mean(filtered_elements)
        variance = np.mean((filtered_elements - mean) ** 2)
        std_dev_formula = np.sqrt(variance)

        return std_dev_function, std_dev_formula

def task5(n, m, min_value, max_value):
    """
    Функция task5(n, m, min_value, max_value) выполняет задачу 5.

    Args:
    - n (int): Количество строк матрицы.
    - m (int): Количество столбцов матрицы.
    - min_value (int): Минимальное значение для генерации случайных элементов матрицы.
    - max_value (int): Максимальное значение для генерации случайных элементов матрицы.

    Returns:
    - None
    """
    task = Task5(n, m, min_value, max_value)
    matrix = task.generate_matrix()
    filtered_elements = task.filter_negative_odd_elements(matrix)
    sum_of_abs_negative_odd_elements = task.calculate_sum_of_abs_negative_odd_elements(filtered_elements)
    std_deviation_function, std_deviation_formula = task.calculate_std_deviation(filtered_elements)

    print("Матрица A:")
    print(matrix)
    print("\nОтфильтрованные отрицательные нечетные элементы матрицы A:")
    print(filtered_elements)
    print("\nСумма модулей отрицательных нечетных элементов матрицы A:", sum_of_abs_negative_odd_elements)
    print("Стандартное отклонение (стандартная функция):", round(std_deviation_function, 2))
    print("Стандартное отклонение (по формуле):", round(std_deviation_formula, 2))