import sqlite3
import time

import FinPyQueries

class DataBase:
    '''Класс для работы с БД'''
    def __init__(self):
        super(DataBase, self).__init__()
        self.__connection = sqlite3.connect('main_db_test.db')
        self.__cursor = self.__connection.cursor()

    def create_db(self):
        '''Метод для начального создания БД'''
        list_of_queries = (FinPyQueries.accounts_table_query, FinPyQueries.incomes_table_query,
                           FinPyQueries.outcomes_table_query, FinPyQueries.income_categories_table_query,
                           FinPyQueries.outcome_categories_table_query,)

        for query in list_of_queries:
            self.send_change_query(query=query)

        return True

    def close_connection(self):
        '''Метод закрытия соединения с БД'''
        self.__connection.close()

        return True

    def send_change_query(self, query, *args):
        '''Метод для отправки запросов на изменение БД'''
        try:
            self.__cursor.execute(query, args)  # Отправка запроса с помощью cursor
            self.__connection.commit()  # Подтверждение изменений
        except:
            print("Ошибка исполнения запроса на изменение.")
            return False
        return True

    def send_read_query(self, query, *args):
        '''Метод для отправки запросов на чтение информации из БД'''
        try:
            result = self.__cursor.execute(query, args)  # Отправка запроса с помощью cursor
            result = result.fetchall()  # Получение данных
        except:
            print("Ошибка исполнения запроса на чтение.")
            return False
        return result


class Account:
    '''Класс Acount нужен для создания объектов счетов'''
    def __init__(self, db, account_name, amount=0.00):
        self.account_name = account_name
        self.amount = amount
        self.__db = db
        self.__db.send_change_query(FinPyQueries.add_account_query, self.account_name, self.amount)

    def update_account(self, new_account_name=None, new_amount=None):
        '''Метод для изменения названия счёта'''
        if not new_account_name:
            new_account_name = self.account_name
        if not new_amount:
            new_amount = self.amount
        self.__db.send_change_query(FinPyQueries.update_account_query, new_account_name, new_amount, self.account_name)
        self.account_name = new_account_name
        self.amount = new_amount
        return True

    def delete_account(self):
        self.__db.send_change_query(FinPyQueries.delete_account_query, self.account_name)
        return True

    def add_transaction(self, transaction_type, income_amount, income_category, income_date):
        pass


class Accounts:
    '''Класс для работы со всеми счетами'''
    def __init__(self, db):
        self.__db = db

    def get_list_accounts(self):
        '''Метод для получения списка счетов'''
        accounts = self.__db.send_read_query(query=FinPyQueries.get_accounts_query)
        return accounts

    def get_account_amounts(self):
        '''Метод для получения списка счетов, отсортированных по суммам на них'''
        accounts = self.__db.send_read_query(query=FinPyQueries.get_account_amounts_query)
        return accounts

class Categories:

    def __init__(self, db):
        self.__db = db

    def add_category(self, transaction_type, category_name):
        '''Метод для добавления категории'''
        if transaction_type == 'income':
            self.__db.send_change_query(FinPyQueries.add_income_category_query, category_name)
        elif transaction_type == 'outcome':
            self.__db.send_change_query(FinPyQueries.add_outcome_category_query, category_name)
        else:
            raise ValueError(f"Неверный тип транзакции!")

        return True

    def update_category(self, transaction_type, new_category_name, old_category_name):
        '''Метод для добавления категории'''
        if transaction_type == 'income':
            self.__db.send_change_query(FinPyQueries.update_income_category_query, new_category_name, old_category_name)
        elif transaction_type == 'outcome':
            self.__db.send_change_query(FinPyQueries.update_outcome_category_query, new_category_name, old_category_name)
        else:
            raise ValueError(f"Неверный тип транзакции!")

        return True

    def delete_category(self, transaction_type, category_name):
        '''Метод для удаления категории'''
        if transaction_type == 'income':
            self.__db.send_change_query(FinPyQueries.delete_income_category_query, category_name)
        elif transaction_type == 'outcome':
            self.__db.send_change_query(FinPyQueries.delete_outcome_category_query, category_name)
        else:
            raise ValueError(f"Неверный тип транзакции!")

        return True

    def get_list_category(self, transaction_type):
        '''Метод для получения списка категорий'''
        categories = None

        if transaction_type == 'income':
            categories = self.__db.send_read_query(query=FinPyQueries.get_income_categories)
        elif transaction_type == 'outcome':
            categories = self.__db.send_read_query(query=FinPyQueries.get_outcome_categories)
        else:
            raise ValueError(f"Неверный тип транзакции!")

        return categories


class Transactions:

    def __init__(self, db):
        self.__db = db

    def add_income_transaction(self, transaction_type, amount, category, date, account_name):
        if transaction_type == 'income':
            self.__db.send_change_query(FinPyQueries.add_income_transaction_query, amount, category, date, account_name)
        elif transaction_type == 'outcomes':
            self.__db.send_change_query(FinPyQueries.add_outcome_transaction_query, amount, category, date, account_name)
        else:
            raise ValueError(f"Неверный тип транзакции!")

        return True

    def get_list_transactions(self, transaction_type):
        transactions_list = None
        if transaction_type == 'income':
            transactions_list = self.__db.send_read_query(FinPyQueries.get_list_income_transactions_query)
        elif transaction_type == 'outcomes':
            transactions_list = self.__db.send_read_query(FinPyQueries.get_list_outcome_transactions_query)
        else:
            raise ValueError(f"Неверный тип транзакции!")

        return transactions_list


