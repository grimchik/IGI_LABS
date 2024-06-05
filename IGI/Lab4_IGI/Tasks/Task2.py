import re
import zipfile
class TextAnalyzer:
    """
    Класс для анализа текстовых данных.

    Attributes:
        input_file (str): Путь к входному файлу с текстом.
        output_file (str): Путь к выходному файлу с результатами анализа.
        zip_file (str): Путь к файлу zip, в который упаковываются результаты.
        text (str): Текст для анализа.
        num_sentences (int): Количество предложений в тексте.
        num_declarative (int): Количество повествовательных предложений.
        num_interrogative (int): Количество вопросительных предложений.
        num_imperative (int): Количество побудительных предложений.
        avg_sentence_length (float): Средняя длина предложения.
        avg_word_length (float): Средняя длина слова.
        num_smileys (int): Количество смайликов в тексте.
        capitalized_words_with_numbers (list): Слова с заглавной буквы и цифрами.
        html_colors (list): Шестнадцатеричные идентификаторы цвета в HTML.
        num_min_length_words (int): Количество слов минимальной длины.
        words_followed_by_period (list): Слова, за которыми следует точка.
        longest_word_ending_with_r (str): Самое длинное слово, заканчивающееся на "r".
    """
    def __init__(self, input_file='Tasks/input.txt', output_file='Tasks/output.txt', zip_file='Tasks/result.zip'):
        self.input_file = input_file
        self.output_file = output_file
        self.zip_file = zip_file

    def read_text(self):
        """Чтение текста из входного файла."""
        with open(self.input_file, 'r', encoding='utf-8') as file:
            self.text = file.read()

    def analyze_text(self):
        """Анализ текста и вычисление различных параметров."""
        self.num_sentences = len(re.findall(r'[.!?]', self.text))
        self.num_declarative = len(re.findall(r'\b[A-Za-z]+[.]', self.text))
        self.num_interrogative = len(re.findall(r'\b[A-Za-z]+[?]', self.text))
        self.num_imperative = len(re.findall(r'\b[A-Za-z]+[!]', self.text))

        sentences = re.split(r'[.!?]', self.text)
        self.avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / self.num_sentences

        words = re.findall(r'\b[A-Za-z]+\b', self.text)
        self.avg_word_length = sum(len(word) for word in words) / len(words)

        self.num_smileys = len(re.findall(r'[;:]-*[\(\[\)\]]+', self.text))

        self.capitalized_words_with_numbers = re.findall(r'\b[A-Z][a-z]*[0-9]+[a-z]\b', self.text)

        self.html_colors = re.findall(r'#[0-9A-Fa-f]{6}\b', self.text)

        min_word_length = min(len(word) for word in words)
        self.num_min_length_words = len([word for word in words if len(word) == min_word_length])

        self.words_followed_by_period = re.findall(r'\b[A-Za-z]+[.]', self.text)

        self.longest_word_ending_with_r = max(re.findall(r'\b[A-Za-z]*r\b', self.text), key=len)

    def output_results(self, min_word_length):
        """
        Запись результатов анализа в выходной файл.

        Args:
            min_word_length (int): Минимальная длина слова.
        """
        with open(self.output_file, 'w', encoding='utf-8') as file:
            file.write(f'Количество предложений: {self.num_sentences}\n')
            file.write(f'Количество предложений разных типов:\n')
            file.write(f'    Повествовательные: {self.num_declarative}\n')
            file.write(f'    Вопросительные: {self.num_interrogative}\n')
            file.write(f'    Побудительные: {self.num_imperative}\n')
            file.write(f'Средняя длина предложения: {self.avg_sentence_length}\n')
            file.write(f'Средняя длина слова: {self.avg_word_length}\n')
            file.write(f'Количество смайликов: {self.num_smileys}\n')
            file.write('Слова, начинающиеся с заглавной буквы и содержащие цифры:\n')
            for word in self.capitalized_words_with_numbers:
                file.write(f'    {word}\n')
            file.write('Шестнадцатеричные идентификаторы цвета в HTML:\n')
            for color in self.html_colors:
                file.write(f'    {color}\n')
            file.write(f'Количество слов минимальной длины: {self.num_min_length_words}\n')
            file.write('Слова, за которыми следует точка:\n')
            for word in self.words_followed_by_period:
                file.write(f'    {word}\n')
            file.write(f'Самое длинное слово, заканчивающееся на "r": {self.longest_word_ending_with_r}\n')

    def zip_results(self):
        """Упаковка выходного файла с результатами в zip-архив."""
        with zipfile.ZipFile(self.zip_file, 'w') as zip_file:
            zip_file.write(self.output_file)

    def run(self):
        """Запуск процесса анализа текста."""
        self.read_text()
        self.analyze_text()
        self.output_results(self.num_min_length_words)
        self.zip_results()

    def print_results(self):
        """Вывод результатов анализа на экран."""
        with open(self.output_file, 'r', encoding='utf-8') as file:
            print(file.read())

def Task2():
    """Выполнение задачи анализа текста и вывод результатов."""
    analyzer = TextAnalyzer()
    analyzer.run()
    analyzer.print_results()
