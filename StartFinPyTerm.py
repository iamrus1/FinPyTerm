import string
import datetime

from FinPyClasses import DataBase, Account, Accounts, Categories, Transactions


def cycle_question_with_args(question_func):
    def wrapper(message, answer_options):
        while True:
            answer = question_func(message=message, answer_options=answer_options)
            if answer == False:
                continue
            elif answer == 'ex':
                return 'ex'
            else:
                return answer
    return wrapper


def cycle_question(question_func):
    def wrapper():
        while True:
            answer = question_func()
            if answer == False:
                continue
            elif answer == 'ex':
                return 'ex'
            else:
                return answer
    return wrapper


@cycle_question
def input_amount():
    '''Функция ввода суммы'''
    amount = input("Введите сумму: ")

    answer = validate_amount(amount)
    if answer == 'ex':  # Если сумму прошла проверку, то верни её
        return 'ex'
    elif answer == False:
        return False

    return float(answer)


@cycle_question
def input_category():
    '''Функция ввода категории'''
    category = input("Введите категорию: ")

    answer = validate_category(category)
    if answer == 'ex':
        return 'ex'
    elif answer == False:
        return False

    category = category.lower().strip()

    return category.title()


@cycle_question
def input_date():
    '''Функция ввода даты'''
    transaction_date = f"{datetime.date.today()}".split('-')
    transaction_date.reverse()
    transaction_date = '.'.join(transaction_date)
    confirm_date = input(f"Нажмите ENTER, если хотите оставить текущую дату. Иначе введите любой символ.\nВаш ответ: ")

    if confirm_date == '':
        return transaction_date
    elif confirm_date.lower().strip() == 'ex':
        return 'ex'
    else:
        transaction_date = input("Введите дату в формате dd.mm.yyyy.\nВаш ответ: ")

    answer = validate_date(transaction_date)
    if answer == 'ex':
        return 'ex'
    elif answer == False:
        return False

    return transaction_date


def validate_action_message(answer, answer_options):
    '''Функция валидации управляющего сообщения'''
    if answer in answer_options:
        return True
    elif answer.lower().strip() == 'ex':
        return 'ex'
    else:
        print("\n--------------------------------\nВведено некорректное значение.\n--------------------------------\n")
        return False


def validate_amount(amount):
    '''Функция валидации введённой суммы. Валидация происходит по типу введённой суммы, по положительности числа,
    по величине, по нулям'''
    if amount.lower().strip() == 'ex':
        return 'ex'
    try:
        amount = float(amount)  # Проверка на вещественное число
    except ValueError:
        print("Сумма должна быть целым или дробным числом с разделителем в виде точки.\n")
        return False

    if amount > 0:  # Проверка на положительное число
        if str(amount)[0] == '0' and str(amount)[1] != '.':  # Проверка на корректность положительного числа
            print("\n--------------------------------\nВведено некорректное значение.\n--------------------------------\n")
            return False
        if amount > 99999999 or amount < 0.01:  # Проверка на величину числа
            print("\n--------------------------------\nВведено некорректное значение.\n--------------------------------\n")
            return False
        if '.' in str(amount):
            amount_parts = str(amount).split('.')
            if len(amount_parts[0]) > 8 or len(amount_parts[1]) > 2:  # Проверка на значения до и после разделителя
                print("\n--------------------------------\nВведено некорректное значение.\n--------------------------------\n")
                return False
    else:
        print("Сумма должна быть больше нуля.\n")
        return False

    return True


def validate_category(category):
    '''Функция валидации категории'''
    if category.lower().strip() == 'ex':
        return 'ex'

    char_set = set(['!', '@', '"', "'", '#', '`', '#', '№', '$', '%', '^', '&', '?',
                   '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', ':', ';',
                   '<', '>', '\\', '/', '|', '~', '.', ',', ' ', '0', '1', '2', '3', '4',
                    '5', '6', '7', '8', '9'])
    if char_set & set(category):  # Проверка на наличие недопустимых символов
        print("\n---------------------------------------------\nКатегория может состоять только из букв\n---------------------------------------------\n")
        return False
    elif len(category) == 0 or len(category) > 20:  # Проверка на длину
        print("\n------------------------------\nНедопустимая длина категории\n------------------------------\n")
        return False

    return True


def validate_date(transaction_date):
    '''Функция валидации даты'''
    acceptable_chars = [str(i) for i in range(0, 10)] + ['.']
    if transaction_date.lower().strip() == 'ex':
        return 'ex'
    if len(set(transaction_date) - set(acceptable_chars)) != 0:
        print("\n------------------------------\nНедопустимые символы в дате.\n------------------------------\n")
        return False
    try:
        datetime.datetime.strptime(transaction_date, "%d.%m.%Y")
    except ValueError:
        print("\n------------------------------\nНеверный формат даты. Дата должна иметь вид dd.mm.yyyy.\n------------------------------\n")
        return False
    try:
        d, m, y = transaction_date.split('.')
        datetime.datetime(int(y), int(m), int(d))
    except ValueError:
        print("\n------------------------------\nВведена несуществующая дата.\n------------------------------\n")
        return False

    return True


@cycle_question
def add_income_term():
    print('\n-------------Добавление дохода-------------')
    amount = input_amount()
    if amount != 'ex':
        category = input_category()
        if category != 'ex':
            transaction_date = input_date()
            if transaction_date != 'ex':
                print(f"{amount} | {category} | {transaction_date}")
                return True
            else:
                return 'ex'
        else:
            return 'ex'
    else:
        return 'ex'

    return False


def start_app():
    '''Главная функция,  которая запускается в самом начале'''
    db = DataBase()  # Подключение к БД
    db.create_db()  # Создание БД
    accounts = Accounts(db=db)
    transactions = Transactions(db)

    numbers_of_functions = {'1': add_income_term}
    choose_action_message = "Выберите действие, которое хотите выполнить:\n" \
                    "1. Добавить доход\n" \
                    "Введите EX для выхода\n" \
                    "Ваш ответ: "

    while True:
        action_number = input(choose_action_message)

        answer = validate_action_message(action_number, numbers_of_functions.keys())
        if answer == 'ex':
            return True
        elif answer == True:
            result = numbers_of_functions[action_number]()
            if result == 'ex':
                return True
        else:
            continue
        answer_continue = input("Нажмите 1 для продолжения или любую клавишу для завершения.\n")
        if answer_continue != '1':
            break

    return True



if __name__ == "__main__":
    print("Здравствуйте!\nЯ Finpy - программа для учета Ваших финансов. Давайте начнём.\n")
    start_app()
    print("\n------------\nДо свидания!\n------------\n")
