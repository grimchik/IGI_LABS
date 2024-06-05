def input_float():
    """
        Функция запрашивает у пользователя ввод числа с плавающей запятой (float)
        и обрабатывает исключения, если введенное значение не является числом с плавающей запятой .
        """
    value = 0
    while(True):
        try:
            value = float(input())
            break
        except ValueError:
            print("Incorrect input, repeat please: ")
    return value
def input_int():
    """
    Функция запрашивает у пользователя ввод целые числа (int)
    и обрабатывает исключения, если введенное значение не является целым числом.
    """
    value = 0
    while(True):
        try:
            value = int(input())
            break
        except ValueError:
            print("Incorrect input, repeat please: ")
    return value