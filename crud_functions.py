import sqlite3

def initiate_db():                                     # Функция для создания таблицы Products в файле not_telegram.db
    connection = sqlite3.connect("not_telegram.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEDGER PRIMARY KEY, 
    title TEXT NOT NULL,
    description TEXT,
    price INTEDGER NOT NULL
    )
    """)

    # Цикл для заполнения таблицы Products

    for i in range(1, 5):
        cursor.execute("INSERT INTO Products (id, title, description, price) VALUES(?, ?, ?, ?)",
                       (i, f"Product: {i}", f"Описание: {i}", f"Цена: {i * 100}"))
    connection.commit()  # Сохраняем состояние
    # connection.close()  # В одной функции два раза закрывать таблицу нельзя

    # Создание таблицы Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY, 
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,                
    balance INT NOT NULL
    )
    """)                 # Здесь записываем INT, т.к. INTEGER -> INT
    connection.commit()  # Сохраняем состояние
    connection.close()

def add_user(username, email, age):  # Функция для добавления пользователей в таблицу Users в файле crud_functions
    connection = sqlite3.connect("not_telegram.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                       (f"{username}", f"{email}", f"{age}", f"1000"))
    connection.commit()  # Сохраняем состояние
    connection.close()   # Закрываем подключение


def is_included(username):  # Функция для проверки есть пользователь в базе или нет
    connection = sqlite3.connect("not_telegram.db")
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM Users WHERE username = ?", (username,))
    connection.commit()  # Сохраняем состояние
    check_user = cursor.fetchone()
    connection.close()  # Закрываем подключение
    if check_user is None:
        return False
    else:
        return True

def get_all_products(id):
    connection = sqlite3.connect("not_telegram.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products WHERE id = ?", (id,))
    connection.commit()  # Сохраняем состояние
    prod = cursor.fetchall() # Сохраняем записи в переменной prod
    id, title, description, price = prod[0]
    return f"Название: {title} | Описание: {description} | Цена: {price}"
    connection.close()


# initiate_db()  # Запускать функцию initiate_db для создания (если ее нет) и заполнение таблицы Products.
# Далее закомментировать вызов функции initiate_db()





