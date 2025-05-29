import hashlib
from datetime import datetime

class BaseUser:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self._password_hash = self._encrypt_password(password)
        self.is_active = is_active

    def _encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_password(self, password):
        return self._password_hash == self._encrypt_password(password)

    def __str__(self):
        return f"{self.__class__.__name__}({self.username})"


class AdminUser(BaseUser):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password)
        self.permissions = permissions or []

    def grant_permission(self, permission):
        self.permissions.append(permission)


class StandardUser(BaseUser):
    def __init__(self, username, password, last_login=None):
        super().__init__(username, password)
        self.last_login = last_login

    def refresh_last_login(self):
        self.last_login = datetime.now()


class TemporaryUser(BaseUser):
    def __init__(self, username="guest", password="guest"):
        super().__init__(username, password, is_active=False)
        self.access_level = "restricted"


class UserAuthSystem:
    def __init__(self):
        self.registry = {}

    def register_user(self, user):
        self.registry[user.username] = user

    def authenticate_user(self, username, password):
        user = self.registry.get(username)
        if user and user.is_active and user.validate_password(password):
            return user
        return None


def display_menu():
    auth_system = UserAuthSystem()

    admin = AdminUser("admin", "admin", ["manage_users", "view_logs"])
    user1 = StandardUser("user", "user")
    guest = TemporaryUser()

    auth_system.register_user(admin)
    auth_system.register_user(user1)
    auth_system.register_user(guest)

    while True:
        print("1. Вхід")
        print("2. Вихід")
        choice = input()

        if choice == "1":
            username = input("Ім'я користувача: ")
            password = input("Пароль: ")
            user = auth_system.authenticate_user(username, password)

            if user:
                print(f"Привіт, {user.username}")
                if isinstance(user, AdminUser):
                    print(f"Роль: Адміністратор | Дозволи: {', '.join(user.permissions)}")
                elif isinstance(user, StandardUser):
                    user.refresh_last_login()
                    print(f"Роль: Користувач | Останній вхід: {user.last_login}")
                elif isinstance(user, TemporaryUser):
                    print(f"Роль: Гість | Рівень доступу: {user.access_level}")
            else:
                print("Невірне ім'я користувача або пароль")
        elif choice == "2":
            break
        else:
            print("Невірний вибір")


if __name__ == "__main__":
    display_menu()