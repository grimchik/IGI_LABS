from Tasks.Task1 import task1
from Tasks.Task2 import task2
from Tasks.Task3 import task3
from Tasks.Task4 import task4
from Tasks.Task5 import task5
from SupportFunctions.CorrectInput import input_int
#Author : Voitko Aleksandr
#Variant : 6
#Date 31.03.2024
#Description : This program is the implementation of 3 laboratory
#Lab Number 3
#Version : 1.0
if __name__ == "__main__":
    while True:
        print("Input number of task, if you want to exit input 0: ")
        choose = input_int()
        match choose:
            case 1:
                task1()
            case 2:
                task2()
            case 3:
                task3()
            case 4:
                task4()
            case 5:
                task5()
            case 0:
                break
            case _:
                print("Incorrect input")