def lst_words():
    """
    Есть заданная строка.
    Строка разбивается на слова с помощью пробелов.
    Удаляются запятые из строки.
    Параметры: нет
    Возвращает: список слов из введенной строки
    """
    str_input = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her"
    str_cleaned = str_input.replace(",", "")
    words = str_cleaned.split()
    return words
def task_a():
    """
    Функция для выполнения задания А. Подсчитывает количество слов в списке, заканчивающихся на гласную букву.
    Параметры:Нет
    Возвращает: Ничего.
    """
    vowels = 'aeiouAEIOU'
    words = lst_words()
    count = 0
    for i in words:
        if i[-1] in vowels:
            count += 1
    print(f"Number of words ending with a vowel: {count}")
    print("________________________")
def task_b():
    """
    Функция для выполнения задания B. Выводит слова из списка, длина которых равна средней длине слов в списке.
    Параметры:Нет
    Возвращает:Ничего
    """
    words = lst_words()
    count = 0
    for i in words:
        count += len(i)
    length = round(count/len(words))
    print(f"Print all words with length:{length} if present:")
    #length = 9
    count2 = 0
    for i in words:
        if len(i) == length:
            print(i)
            count2 +=1
    if count2 == 0:
        print(f"There are no words of length {length} characters in the line")
    print("________________________")
def task_c():
    """
    Функция для выполнения задания C. Выводит каждое пятое слово из списка.
    Параметры:Нет
    Возвращает:Ничего
    """
    print("Print every 5th word in string:")
    words = lst_words()
    count = 0
    for i in words:
        if (count+1) % 5 == 0 :
            print(i)
        count+=1
    print("________________________")
def task4():
    """
    Функция для выполнения 4 задания.
    Вызывается функция для выполнения задания А, задания Б, задания С
    Параметры: нет
    Возвращает: Ничего
    """
    task_a()
    task_b()
    task_c()