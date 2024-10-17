# Создание таблиц
accounts_table_query = '''
        CREATE TABLE IF NOT EXISTS accounts(
        account_name VARCHAR20 PRIMARY KEY NOT NULL,
        amount REAL NOT NULL)
        '''
incomes_table_query = '''
        CREATE TABLE IF NOT EXISTS incomes(
        income_id INTEGER PRIMARY KEY AUTOINCREMENT,
        income_amount REAL NOT NULL,
        income_category VARCHAR(20),
        income_date DATE NOT NULL,
        account_name VARCHAR20, 
        FOREIGN KEY(account_name) REFERENCES accounts(account_name))
        '''
outcomes_table_query = '''
        CREATE TABLE IF NOT EXISTS outcomes(
        outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
        outcome_amount REAL NOT NULL,
        outcome_category VARCHAR(20),
        outcome_date DATE NOT NULL,
        account_name VARCHAR20,
        FOREIGN KEY(account_name) REFERENCES accounts(account_name))
        '''
income_categories_table_query = '''
        CREATE TABLE IF NOT EXISTS income_categories(income_category VARCHAR(20) NOT NULL PRIMARY KEY)
        '''
outcome_categories_table_query = '''
        CREATE TABLE IF NOT EXISTS outcome_categories(outcome_category VARCHAR(20) NOT NULL PRIMARY KEY)
        '''

# Вставки категорий
add_income_category_query = '''INSERT or IGNORE INTO income_categories (income_category) VALUES (?)'''
add_outcome_category_query = '''INSERT or IGNORE INTO outcome_categories (outcome_category) VALUES (?)'''

# Вставки счетов
add_account_query = '''INSERT or IGNORE INTO accounts (account_name, amount) VALUES (?, ?)'''

# Вставки транзакций доходов
add_income_transaction_query = '''
        INSERT or IGNORE INTO incomes (income_amount, income_category, income_date, account_name)
        VALUES (?,?,?,?)
        '''

# Вставки транзакция расходов
add_outcome_transaction_query = '''
        INSERT or IGNORE INTO outcomes (outcome_amount, outcome_category, outcome_date, account_name) 
        VALUES (?,?,?,?)
        '''

# Изменения категорий
update_income_category_query = '''UPDATE or IGNORE income_categories SET income_category = (?) WHERE income_category = (?)'''
update_outcome_category_query = '''UPDATE or IGNORE outcome_categories SET outcome_category = (?) WHERE outcome_category = (?)'''

# Изменения счетов
update_account_query = '''UPDATE or IGNORE accounts SET account_name = (?), amount = (?) WHERE account_name = (?)'''

# Удаления категорий
delete_income_category_query = '''DELETE FROM income_categories WHERE income_category = (?)'''
delete_outcome_category_query = '''DELETE FROM outcome_categories WHERE outcome_category = (?)'''

# Удаление счетов
delete_account_query = '''DELETE FROM accounts WHERE account_name = (?)'''

# Выборки категорий
get_income_categories = '''SELECT * FROM income_categories'''
get_outcome_categories = '''SELECT * FROM outcome_categories'''

# Выборка счетов
get_accounts_query = '''SELECT account_name FROM accounts'''
get_account_amounts_query = '''SELECT * FROM accounts ORDER BY amount DESC'''

# Выборки транзакций
get_list_income_transactions_query = '''SELECT * FROM incomes'''
get_list_outcome_transactions_query = '''SELECT * FROM outcomes'''

# Изменения транзакций
# Удаления транзакций
# Выборки транзакций