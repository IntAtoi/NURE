import hashlib

users = {
    "ivan123": {
        "password": hashlib.md5("ivanPassword".encode()).hexdigest(),
        "full_name": "Іван Іванович Іванов"
    },
    "maria456": {
        "password": hashlib.md5("mariaPassword".encode()).hexdigest(),
        "full_name": "Марія Петрівна Петрова"
    }
}

def check_password(login, password):
    if login in users:
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if users[login]["password"] == hashed_password:
            print(f"Привіт, {users[login]['full_name']}.")
        else:
            print("Невірний пароль")
    else:
        print("Невірній логін")

login_input = input("Введіть ім'я користувача: ")
password_input = input("Введіть пароль: ")

check_password(login_input, password_input)
