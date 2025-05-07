import hashlib
from datetime import datetime

class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == self._hash_password(password)


class Administrator(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password)
        self.permissions = permissions or []

    def add_permission(self, permission):
        self.permissions.append(permission)

    def __str__(self):
        return f"Administrator({self.username})"


class RegularUser(User):
    def __init__(self, username, password, last_login=None):
        super().__init__(username, password)
        self.last_login = last_login

    def update_last_login(self):
        self.last_login = datetime.now()

    def __str__(self):
        return f"RegularUser({self.username})"


class GuestUser(User):
    def __init__(self, username="guest", password="guest"):
        super().__init__(username, password, is_active=False)
        self.access_level = "limited"

    def __str__(self):
        return f"GuestUser({self.username})"

class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.is_active and user.verify_password(password):
            return user
        return None

def main_menu():
    ac = AccessControl()

    admin = Administrator("admin", "admin", ["manage_users", "view_logs"])
    user1 = RegularUser("user", "qwerty1234")
    guest = GuestUser()

    ac.add_user(admin)
    ac.add_user(user1)
    ac.add_user(guest)

    while True:
        print("\n--- Меню входу ---")
        print("1. Увійти")
        print("2. Вийти")
        choice = input("Ваш вибір: ")

        if choice == "1":
            username = input("Ім'я користувача: ")
            password = input("Пароль: ")
            user = ac.authenticate_user(username, password)

            if user:
                print(f"Вхід успішний, {user.username}")
                if isinstance(user, Administrator):
                    print(f"Роль: Адміністратор | Дозволи: {', '.join(user.permissions)}")
                elif isinstance(user, RegularUser):
                    user.update_last_login()
                    print(f"Роль: Користувач | Останній вхід: {user.last_login}")
                elif isinstance(user, GuestUser):
                    print(f"Роль: Гість | Рівень доступу: {user.access_level}")
            else:
                print("Невірне ім'я користувача або пароль.")
        elif choice == "2":
            break
        else:
            print("Невірний вибір.")

if __name__ == "__main__":
    main_menu()
