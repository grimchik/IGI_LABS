from SupportClasses import Correctinput
from Tasks.Task1 import Task1
from Tasks.Task2 import Task2
from Tasks.Task3 import Task3
from Tasks.Task4 import Task4
from Tasks.Task5 import task5
from SupportClasses.Correctinput import CorrectInput
#Author : Voitko Aleksandr
#Variant : 6
#Date 13.04.2024
#Description : This program is the implementation of 4 laboratory
#Lab Number 4
#Version : 1.0
if __name__ == "__main__":
    while True:
        print("Input number of task, if you want to exit input 0: ")
        choose = CorrectInput.input_int()
        match choose:
            case 1:
                Task1()
            case 2:
                Task2()
            case 3:
                Task3()
            case 4:
                Task4()
            case 5:
                task5(5, 5, -100, 100)
            case 0:
                break
            case _:
                print("Incorrect input")