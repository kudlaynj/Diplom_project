import sqlite3

connection = sqlite3.connect("data_base.db")
cursor = connection.cursor()

img_ = {"calcium": 'c:\\Users\\Admin\\PycharmProjects\\module_13\\kalcij_evalar.png',
        'dihydroquercetin': 'c:\\Users\\Admin\\PycharmProjects\\module_13\\dgkv.png',
        'magnesium': 'c:\\Users\\Admin\\PycharmProjects\\module_13\\evalar-magnij.png',
        'multiflora': 'c:\\Users\\Admin\\PycharmProjects\\module_13\\multiflora-evalar.png'}


def initiate_db():
    cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL,
name_img TEXT NOT NULL
    )
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users(
            userid INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
            )
            """)


initiate_db()


def is_included(username):
    check_user = cursor.execute("SELECT username FROM Users WHERE username = ?", (username,))
    if check_user.fetchone():
        return True
    else:
        return False


def add_user(username, email, age, balance):
    balance = 1000
    cursor.execute('''
        INSERT INTO Users (username, email, age, balance)
        VALUES (?, ?, ?, ?)
    ''', (username, email, age, balance))
    connection.commit()



def get_all_products():
    cursor.execute(" SELECT * FROM Products ")
    check_product = cursor.fetchall()
    return check_product


# for i, j, k in zip(range(1, 5), img_, img_.values()):
#    initiate_db()
#    cursor.execute("INSERT OR IGNORE INTO Products(id, title, description, price, name_img) VALUES (?, ?, ?, ?, ?)",
#                   (f'{i}', f'Product{i}', f'{j}', f'{i * 100}', f'{k}'))
#    print(f"Название: Product{i} | Описание: {j} | Цена: {i * 100} | img_ {k}")
#    connection.commit()

connection.commit()
