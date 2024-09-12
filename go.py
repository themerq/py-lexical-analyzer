import ply.lex as lex # Импорт модуля для лексического анализа
import tkinter as tk # Импорт модуля для создания графического интерфейса
from tkinter import scrolledtext # Импорт виджета для многострочного текста
import sys # Импорт модуля для работы с системными функциями
from decimal import Decimal # Импорт десятичного типа данных
from tkinter import messagebox # Импорт модуля для вывода диалоговых окон


# Определение токенов (лексем)
tokens = [
    'OPERATORS_RELATIONAL',
    'KLUCH',
    'INTEGER_BINARY',
    'INTEGER_OCTAL',
    'INTEGER_HEXADECIMAL',
    'REAL_NUMBER',
    'IDENTIFIER'
]

# Игнорирование комментариев внутри # ... #
def t_ignore_COMMENT(t):
    r'\%.*?\%'  # Регулярное выражение для комментариев внутри #
    pass  # Игнорируем комментарии внутри #

# Игнорирование пробелов и символов новой строки
t_ignore = ' \n'

# Словарь для соответствия ключевых слов и операторов токенам
tokens_dict = {
    'and': 'OPERATORS_RELATIONAL',
    'or': 'OPERATORS_RELATIONAL',
    'not': 'OPERATORS_RELATIONAL',
    ':=': 'OPERATORS_RELATIONAL',
    '<>': 'OPERATORS_RELATIONAL',
    '<': 'OPERATORS_RELATIONAL',
    '>': 'OPERATORS_RELATIONAL',
    '<=': 'OPERATORS_RELATIONAL',
    '+': 'OPERATORS_RELATIONAL',
    '>=': 'OPERATORS_RELATIONAL',
    '-': 'OPERATORS_RELATIONAL',
    '/': 'OPERATORS_RELATIONAL',
    '*': 'OPERATORS_RELATIONAL',
    '=': 'OPERATORS_RELATIONAL',
    ';': 'OPERATORS_RELATIONAL',
    '': 'OPERATORS_RELATIONAL',
    '(': 'OPERATORS_RELATIONAL',
    ')': 'OPERATORS_RELATIONAL',    
    '#': 'KLUCH',
    'readln': 'KLUCH',
    'writeln': 'KLUCH',
    'begin': 'KLUCH',
    'to': 'KLUCH',
    'if': 'KLUCH',
    'step': 'KLUCH',
    'next': 'KLUCH',
    '@': 'KLUCH',
    'for': 'KLUCH',
    '&': 'KLUCH',
    'else': 'KLUCH',
    'while': 'KLUCH',
    'end': 'KLUCH'
}
###################Буфер######################
## Переменная для хранения позиции окончания предыдущего токена
# Создаем пустой список для хранения токенов
token_list = [] #Буфер

prev_token_end = 0

# Переменная для хранения предыдущего токена
prev_token = None

# Функция для обработки токена
def process_token(t):
    global prev_token_end
    global prev_token

    # Проверяем, если предыдущий токен существует и заканчивается на той же позиции, где начинается текущий токен
    if prev_token is not None and prev_token_end == t.lexpos:
        error_message = f"Error: Некорректный токен '{prev_token.value}{t.value}'"
        messagebox.showerror("Ошибка", error_message)  # Показываем всплывающее окно с сообщением об ошибке
        sys.exit()  # Завершаем выполнение программы при обнаружении ошибки
    prev_token_end = t.lexpos + len(t.value)
    prev_token = t
    return t

# # Функция для разделителей
def t_OPERATORS_RELATIONAL(t):
    r'/|,|{|}|\=|\(|\)|and|or|not|:=|<>|<|>|<=|\|\||>=|-|\*|;'
    t.type = tokens_dict.get(t.value, 'OPERATORS_RELATIONAL')  # Проверяем словарь для зарезервированных слов
    return process_token(t)
# Функция для ключ слов
def t_KLUCH(t):
    r'readln|writeln|@|begin|&|to|if|step|next|end|for|else|while|\#|@|&'
    t = process_token(t)
    return t
# Функция для чисел в 16тиричной
def t_INTEGER_HEXADECIMAL(t):
    r'[A-Fa-f][0-9A-Fa-f]+[Hh]'
    return process_token(t)
# Функция для идентификаторов
def t_IDENTIFIER(t):
    r'[A-Za-z][A-Za-z0-9]*'
    t = process_token(t)
    return t

# Функция для двоички
def t_INTEGER_BINARY(t):
    r'[0-1]+[bB]'
    return process_token(t)
# Функция для восьмерич
def t_INTEGER_OCTAL(t):
    r'[0-7]+[Oo]'
    return process_token(t)
# Функция для действит чисел
def t_REAL_NUMBER(t):
    r'[-+]?\d+\.\d*([Ee][-+]?\d+)?|\d*\.?\d+([Ee][-+]?\d+)?[Dd]?'
    t = process_token(t)
    return t

# Обработчик ошибок
def t_error(t):
    if t.value:
        error_message = f"Error: Символ не соответствует формальному языку '{t.value[0]}'"
        messagebox.showerror("Ошибка", error_message)  # Показываем всплывающее окно с сообщением об ошибке
        sys.exit()  # Завершаем выполнение программы при обнаружении ошибки
    else:
        error_message = "Error: Illegal character at the end of input"
        messagebox.showerror("Ошибка", error_message)  # Показываем всплывающее окно с сообщением об ошибке

    # Если следующий токен - число или идентификатор, выдаем ошибку
    if lexer.lexdata[lexer.lexpos].isalnum():
        print("Error: Missing space between tokens")
        sys.exit()  # Завершаем выполнение программы при обнаружении ошибки

# Запускаем лексер
lexer = lex.lex()

KLUCH = ['readln', 'writeln', 'end', 'begin', '&', 'to', 'if', 'step', 'next', '@', 'for', 'else', 'while', 'input','#', '@', '&', ]
OPERATORS_RELATIONAL = [';', ',', '{', '}', '=', '(', ')', 'and', 'or', 'not', ':=', '<>', '<', '>', '<=', '||', '>=', '-', '/', '*']
identifier_table = {}  # Таблица идентификаторов
number_table = {} # Таблица чисел
result_list = [] # Таблица результат

# Функция для сброса значений
def reset_values():
    global token_list, identifier_table, number_table, result_list, number_table1

    # Очищаем списки
    token_list = []
    identifier_table = {}
    number_table = {}
    result_list = []
    number_table1 = {}

    # Очищаем поле вывода и ввода
    input_entry.delete(1.0, tk.END)
    result.delete(1.0, tk.END)
    table1.delete(1.0, tk.END)
    table3.delete(1.0, tk.END)
    table2.delete(1.0, tk.END)
    table4.delete(1.0, tk.END)

# Печатаем токены
def tokenize_input():
    input_string = input_entry.get("1.0", tk.END)  # Получаем введенный текст из поля ввода
    lexer.input(input_string)  # Подаем введенный текст лексическому анализатору

    # Очищаем поле вывода результата
    result.delete("1.0", tk.END)

    while True:
        tok = lexer.token()
        if not tok:
            break  # конец

        print(tok)
        token_list.append(tok)  # Добавляем токен в список
    print("Successfully tokenized.")
    # Выводим содержимое списка токенов
    print("Token list:")
    for token in token_list:
        print(token)
    new_token_list = [(token.type, token.value) for token in token_list if token.type in ['KLUCH', 'OPERATORS_RELATIONAL', 'IDENTIFIER', 'REAL_NUMBER','INTEGER_HEXADECIMAL','INTEGER_OCTAL','INTEGER_BINARY']]

    print(new_token_list)

    for item in new_token_list:
        if item[0] == 'KLUCH' and item[1] in KLUCH:
            table_number = 1  # Номер таблицы
            value_number = KLUCH.index(item[1]) + 1  # Номер значения в таблице
            result_list.append((table_number, value_number))
        elif item[0] == 'OPERATORS_RELATIONAL' and item[1] in OPERATORS_RELATIONAL:
            table_number = 2
            value_number = OPERATORS_RELATIONAL.index(item[1]) + 1
            result_list.append((table_number, value_number))
        elif item[0] == 'INTEGER_BINARY' or item[0] == 'INTEGER_OCTAL' or item[0] == 'INTEGER_HEXADECIMAL' or item[
            0] == 'REAL_NUMBER':
            number = item[1]
            if number in number_table:
                value_number = number_table[number]
            else:
                # Если число нет в таблице, добавляем его и присваиваем новый номер
                value_number = len(number_table) + 1
                number_table[number] = value_number
            table_number = 3
            result_list.append((table_number, value_number))

        elif item[0] == 'IDENTIFIER':
            identifier = item[1]
            if identifier in identifier_table:
                value_number = identifier_table[identifier]
            else:
                # Если идентификатора нет в таблице, добавляем его и присваиваем новый номер
                value_number = len(identifier_table) + 1
                identifier_table[identifier] = value_number
            table_number = 4
            result_list.append((table_number, value_number))

    print(number_table)
    print(result_list)

    number_table1 = {}  # Новая таблица чисел в двоичной системе

    for key, value in number_table.items():
        if 'e' in key.lower():
            mantissa, exponent = key.split('e')
            exponent = int(exponent)
            if exponent >= 0:
                binary_mantissa = ''.join(format(int(digit), '04b') for digit in mantissa.replace('.', ''))
                binary_number = f"0.{binary_mantissa}e+{exponent:08b}"
            else:
                binary_mantissa = ''.join(format(int(digit), '04b') for digit in mantissa.replace('.', ''))
                binary_exponent = bin(abs(exponent))[2:].zfill(8)
                binary_number = f"0.{binary_mantissa}e-{binary_exponent}"
        else:
            if key.endswith(('b', 'B')):
                binary_number = key[:-1]  # Число уже в двоичной системе
            elif key.endswith(('h', 'H')):
                binary_number = bin(int(key[:-1], 16))[2:].zfill(
                    8)  # Преобразуем в двоичную систему счисления и добавляем нули слева
            elif key.endswith(('o', 'O')):
                binary_number = bin(int(key[:-1], 8))[2:].zfill(
                    8)  # Преобразуем в двоичную систему счисления и добавляем нули слева
            elif key.endswith(('d', 'D')):
                binary_number = bin(int(Decimal(key[:-1])))[2:].zfill(
                    8)  # Преобразуем в двоичную систему счисления и добавляем нули слева (если число действительное)
            else:
                if '.' in key:
                    integer_part, decimal_part = key.split('.')
                    binary_integer = bin(int(integer_part))[2:].zfill(8) if integer_part else '0'
                    binary_decimal = ''.join(format(int(digit), '08b') for digit in decimal_part)
                    binary_number = f"{binary_integer}.{binary_decimal}"
                else:
                    binary_number = bin(int(key))[2:].zfill(8)

        number_table1[binary_number] = value  # Добавляем в новую таблицу

    print(number_table1)
################################ Ввод текста ####################
    # Преобразуем список в строку
    list_str = str(result_list)
    # Вставляем строку в виджет tk.Text
    result.insert(tk.END, list_str)

    #number_table11 = set(number_table1.keys()) на случай если нужно будет поменять вывод цифр
    list_str1 = str(number_table1)
    table1.insert(tk.END, list_str1)

    list_str2 = str(KLUCH)
    table2.insert(tk.END, list_str2)

    list_str3 = str(OPERATORS_RELATIONAL)
    table3.insert(tk.END, list_str3)

    list_str4 = str(identifier_table)
    table4.insert(tk.END, list_str4)

######################### Создаем графический интерфейс ###############################
root = tk.Tk()  # Создание основного окна приложения
root.title("Лексический анализатор by Голованов С.О. 01п")

# Поле ввода
input_label = tk.Label(root, text="Введите программу:")
input_label.pack()
input_entry = scrolledtext.ScrolledText(root, height=10, width=60)
input_entry.pack()

# Кнопка для токенизации введенного текста
tokenize_button = tk.Button(root, text="Запустить анализ", command=tokenize_input)
tokenize_button.pack()

# Поле вывода результата
result_label = tk.Label(root, text="Результат анализа:")
result_label.pack()
result = scrolledtext.ScrolledText(root, height=10, width=60)
result.pack()

# Поле вывода чисел
table1_label = tk.Label(root, text="Числа:")
table1_label.pack()
table1 = scrolledtext.ScrolledText(root, height=7, width=60)
table1.pack()

# Поле вывода ключей
table2_label = tk.Label(root, text="Ключ.слова:")
table2_label.pack()
table2 = scrolledtext.ScrolledText(root, height=7, width=60)
table2.pack()

# Поле вывода ключей
table3_label = tk.Label(root, text="Разделители:")
table3_label.pack()
table3 = scrolledtext.ScrolledText(root, height=7, width=60)
table3.pack()

# Поле вывода идентификаторов
table4_label = tk.Label(root, text="Идентификаторы:")
table4_label.pack()
table4 = scrolledtext.ScrolledText(root, height=7, width=60)
table4.pack()

# Создаем кнопку "Сброс"
reset_button = tk.Button(root, text="Сброс", command=reset_values)
reset_button.pack()

# Запускаем главный цикл приложения
root.mainloop() # Запуск цикла обработки событий для отображения окна и работы приложения