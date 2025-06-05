import hashlib
from datetime import datetime

class UserBase:
    def __init__(self, name, secret, active=True):
        self.name = name
        self._hash = self._make_hash(secret)
        self.active = active

    def _make_hash(self, secret):
        return hashlib.sha256(secret.encode()).hexdigest()

    def check_credentials(self, secret):
        return self._hash == self._make_hash(secret)

    def __str__(self):
        return f"{type(self).__name__}({self.name})"


class Admin(UserBase):
    def __init__(self, name, secret, roles=None):
        super().__init__(name, secret)
        self.roles = roles or []

    def add_role(self, role):
        self.roles.append(role)


class RegularUser(UserBase):
    def __init__(self, name, secret, last_seen=None):
        super().__init__(name, secret)
        self.last_seen = last_seen

    def update_login_time(self):
        self.last_seen = datetime.now()


class Guest(UserBase):
    def __init__(self, name="guest", secret="guest"):
        super().__init__(name, secret, active=False)
        self.level = "limited"


class AuthSystem:
    def __init__(self):
        self.users = {}

    def add(self, profile):
        self.users[profile.name] = profile

    def verify(self, name, secret):
        profile = self.users.get(name)
        if profile and profile.active and profile.check_credentials(secret):
            return profile
        return None


def auth_interface():
    system = AuthSystem()

    system.add(Admin("admin", "admin", ["manage", "logs"]))
    system.add(RegularUser("user", "user"))
    system.add(Guest())

    while True:
        print("1. Авторизація")
        print("2. Вихід")
        match input():
            case "1":
                u = input("Користувач: ")
                p = input("Пароль: ")
                entity = system.verify(u, p)
                if entity:
                    print(f"Привіт, {entity.name}")
                    match entity:
                        case Admin():
                            print("Права:", ', '.join(entity.roles))
                        case RegularUser():
                            entity.update_login_time()
                            print("Останній вхід:", entity.last_seen)
                        case Guest():
                            print("Режим доступу:", entity.level)
                else:
                    print("Дані некоректні")
            case "2":
                break
            case _:
                print("Помилка вибору")


if __name__ == "__main__":
    auth_interface()
