from abc import ABC, abstractmethod
import math
import turtle
from PIL import Image
from PIL import EpsImagePlugin

class DrawableMixin:
    """
    Миксин для отрисовки фигур.
    """
    def draw(side_length, acute_angle, color, text):
        """
        Отрисовка фигуры.

        Args:
        - side_length (float): Длина стороны фигуры.
        - acute_angle (float): Острый угол фигуры в градусах.
        - color (str): Цвет фигуры.
        - text (str): Текст подписи фигуры.

        Returns:
        - None
        """
        pass

class Color:
    """
    Класс для представления цвета.
    """
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

class GeometricFigure(ABC):
    """
    Абстрактный базовый класс для геометрических фигур.
    """
    def __init__(self, length):
       self.length = length

    @abstractmethod
    def calculate_area(self):
        """
        Абстрактный метод для вычисления площади фигуры.

        Returns:
        - float: Площадь фигуры.
        """
        pass

class Circle(GeometricFigure):
    """
    Класс для представления круга.
    """
    figure_name = "Круг"

    def __init__(self, radius):
        super().__init__(radius)

    def calculate_area(self):
        """
        Метод для вычисления площади круга.

        Returns:
        - float: Площадь круга.
        """
        return math.pi * self.length ** 2

class Rhombus(GeometricFigure, DrawableMixin):
    """
    Класс для представления ромба.
    """
    figure_name = "Ромб"

    def __init__(self, side_length, acute_angle, color):
        super().__init__(side_length)
        self.acute_angle = math.radians(acute_angle)
        self.color = Color(color)

    def draw(side_length, acute_angle, color, text):
        """
        Метод для отрисовки ромба.

        Args:
        - side_length (float): Длина стороны ромба.
        - acute_angle (float): Острый угол ромба в градусах.
        - color (str): Цвет ромба.
        - text (str): Текст подписи ромба.

        Returns:
        - None
        """
        turtle.color(color)
        turtle.begin_fill()
        for _ in range(2):
            turtle.forward(side_length)
            turtle.left(180 - acute_angle)
            turtle.forward(side_length)
            turtle.left(180 - (180 - acute_angle))
        turtle.end_fill()
        turtle.penup()
        turtle.goto(-50, -150)
        turtle.write(text, font=("Arial", 16, "normal"))
        turtle.hideturtle()
        ts = turtle.getscreen()
        ts.getcanvas().postscript(file="Tasks/Romb.eps")
        EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs10.03.0\bin\gswin64c.exe'
        eps_image = Image.open("Tasks/Romb.eps")
        eps_image.load(scale=10)
        eps_image.save("Tasks/Romb.png")

    def validate_input(side_length, acute_angle):
        """
        Метод для проверки корректности ввода.

        Args:
        - side_length (float): Длина стороны ромба.
        - acute_angle (float): Острый угол ромба в градусах.

        Returns:
        - bool: Результат валидации.
        """
        if side_length <= 0:
            print("Ошибка: длина стороны должна быть больше нуля.")
            return False
        if not (0 < acute_angle <= 90):
            print("Ошибка: острый угол должен находиться в диапазоне от 0 до 90 градусов.")
            return False
        return True

    def calculate_area(self):
        """
        Метод для вычисления площади ромба.

        Returns:
        - float: Площадь ромба.
        """
        return self.side_length ** 2 * math.sin(self.acute_angle)

def Task4():
    """
    Функция для выполнения задания 4.
    """
    side_length = float(input("Введите длину стороны ромба: "))
    acute_angle = float(input("Введите острый угол ромба в градусах: "))
    color = input("Введите цвет ромба: ")

    if not Rhombus.validate_input(side_length, acute_angle):
        return

    rhombus = Rhombus(side_length, acute_angle, color)
    text = input("Введите подпись: ")
    Rhombus.draw(side_length, acute_angle, color, text)
    turtle.done()