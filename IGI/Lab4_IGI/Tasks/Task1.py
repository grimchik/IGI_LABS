import csv
import pickle
from SupportClasses.Correctinput import CorrectInput

class Team:
    """
    Класс, представляющий команду.

    Атрибуты:
        name (str): Название команды.
        points (int): Количество очков у команды.
    """
    def __init__(self, name, points):
        self.name = name
        self.points = points

    @property
    def name(self):
        """Возвращает название команды."""
        return self._name

    @name.setter
    def name(self, value):
        """Устанавливает название команды."""
        self._name = value

    @property
    def points(self):
        """Возвращает количество очков."""
        return self._points

    @points.setter
    def points(self, value):
        """Устанавливает количество очков."""
        self._points = value

    def __del__(self):
        print("Команда удалена!")

class CompetitionTable:
    """
    Класс, представляющий таблицу соревнований.

    Атрибуты:
        teams (list): Список команд в таблице.
    """
    def __init__(self):
        self.teams = []

    def add_team(self, team):
        """Добавляет команду в таблицу."""
        self.teams.append(team)

    def print_all_teams(self):
        """Выводит информацию о всех командах в таблице."""
        for team in self.teams:
            print("Команда:", team.name, "| Очки:", team.points)

    def find_winner(self):
        """Находит победителя соревнования."""
        if not self.teams:
            return None
        winner = max(self.teams, key=lambda x: x.points)
        return winner

    def sort_by_points(self):
        """Сортирует команды по количеству очков."""
        self.teams.sort(key=lambda x: x.points, reverse=True)

    def find_team_by_name(self, name):
        """
        Находит команду по её названию.

        Args:
            name (str): Название команды.

        Returns:
            Team: Объект команды, если найден, в противном случае - None.
        """
        for team in self.teams:
            if team.name == name:
                return team
        return None

class SerializeStrategy:
    """Абстрактный класс стратегии сериализации."""
    def print_serializer(self):
        """Выводит информацию о сериализаторе."""
        print("Сериализатор")

    def serialize(self, filename, data):
        """Абстрактный метод сериализации."""
        pass

class CSVSerialize(SerializeStrategy):
    """Класс для сериализации данных в формат CSV."""
    def serialize(self, filename, data):
        """
        Сериализует данные в формате CSV и записывает в файл.

        Args:
            filename (str): Имя файла для записи данных.
            data (list): Список объектов команд для сериализации.
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Название Команды", "Очки"])
            for team in data:
                writer.writerow([team.name, team.points])

class PickleSerialize(SerializeStrategy):
    """Класс для сериализации данных с использованием модуля pickle."""
    def serialize(self, filename, data):
        """
        Сериализует данные с использованием pickle и записывает в файл.

        Args:
            filename (str): Имя файла для записи данных.
            data (list): Список объектов команд для сериализации.
        """
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

def Task1():
    """
    Выполняет задачу по созданию и управлению соревновательной таблицей.

    Создаёт несколько команд, добавляет их в таблицу, сортирует по очкам,
    находит победителя и выполняет сериализацию таблицы в форматы CSV и pickle.
    """
    teams_dict = {
        "TeamA": Team("TeamA", 0),
        "TeamB": Team("TeamB", 2)
    }
    competition_table = CompetitionTable()
    print("Введите количество команд: ")
    num_teams = CorrectInput.input_int()
    for i in range(num_teams):
        name = input("Введите название команды: ")
        print("Введите количество очков: ")
        points = CorrectInput.input_int()
        team = Team(name, points)
        teams_dict[name] = team

    for team in teams_dict.values():
        competition_table.add_team(team)

    competition_table.sort_by_points()
    competition_table.print_all_teams()
    winner = competition_table.find_winner()
    print("Победитель: ", winner.name, "| Очки: ", winner.points)
    find_team = competition_table.find_team_by_name("TeamA")
    if find_team:
        print("Название:", find_team.name, "| Очки:", find_team.points)

    csv_serializer = CSVSerialize()
    csv_serializer.serialize("teams_csv.csv", competition_table.teams)

    pickle_serializer = PickleSerialize()
    pickle_serializer.serialize("teams_pickle.pkl", competition_table.teams)
