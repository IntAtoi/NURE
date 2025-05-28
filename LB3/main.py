import sqlite3

def add_user():
    login = input("Введіть логін: ")
    password = input("Введіть пароль: ")
    full_name = input("Введіть повне ім'я: ")

    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)", (login, password, full_name))

    connection.commit()
    connection.close()

    print(f"Користувач {full_name} доданий")

def change_password():
    login = input("Введіть логін: ")

    while True:
        current_password = input("Введіть поточний пароль: ")

        connection = sqlite3.connect('user_database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT password FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()

        if result is None:
            print("Користувача не знайдено.")
            connection.close()
            return
        if result[0] == current_password:
            new_password = input("Введіть новий пароль: ")
            cursor.execute("UPDATE users SET password = ? WHERE login = ?", (new_password, login))
            connection.commit()
            print("Пароль змінено")
            return
        else:
            print("Невірний логін або пароль")


    connection.close()


connection = sqlite3.connect('user_database.db')
cursor = connection.cursor()

cursor.execute('''
        create table if not exists users(
        id integer primary key,
        login text not null unique,
        password text not null,
        full_name text not null)''')

connection.commit()
connection.close()

while True:
    print("1. Додати нового користувача")
    print("2. Оновити пароль")

    choice = input()

    if choice == '1':
        add_user()
    elif choice == '2':
        change_password()
    else:
        print("Невірно")
