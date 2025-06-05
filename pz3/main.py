import sqlite3
from datetime import datetime
import random

connection = sqlite3.connect('security_events.db')
cursor = connection.cursor()

def log_event(source_name, type_name, message, ip=None, user=None):
    cursor.execute("SELECT id FROM EventSources WHERE name = ?", (source_name,))
    source = cursor.fetchone()
    cursor.execute("SELECT id FROM EventTypes WHERE type_name = ?", (type_name,))
    event_type = cursor.fetchone()
    if source and event_type:
        cursor.execute('''
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now(), source[0], event_type[0], message, ip, user))
        connection.commit()

def add_source(name, location, source_type):
    try:
        cursor.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)", (name, location, source_type))
        connection.commit()
    except sqlite3.IntegrityError:
        print("Джерело вже існує.")

def add_type(type_name, severity):
    try:
        cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", (type_name, severity))
        connection.commit()
    except sqlite3.IntegrityError:
        print("Тип вже існує.")

def populate_event_types():
    defaults = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical"),
    ]
    for item in defaults:
        try:
            cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", item)
        except sqlite3.IntegrityError:
            continue
    connection.commit()

def initialize_schema():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EventSources (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            location TEXT,
            type TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EventTypes (
            id INTEGER PRIMARY KEY,
            type_name TEXT UNIQUE,
            severity TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SecurityEvents (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source_id INTEGER,
            event_type_id INTEGER,
            message TEXT,
            ip_address TEXT,
            username TEXT,
            FOREIGN KEY (source_id) REFERENCES EventSources(id),
            FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
        )
    ''')
    connection.commit()

def recent_failures():
    cursor.execute('''
        SELECT * FROM SecurityEvents
        WHERE event_type_id = (SELECT id FROM EventTypes WHERE type_name = 'Login Failed')
        AND timestamp >= datetime('now', '-1 day')
    ''')
    return cursor.fetchall()

def multiple_failures():
    cursor.execute('''
        SELECT ip_address, COUNT(*), MIN(timestamp), MAX(timestamp)
        FROM SecurityEvents
        WHERE event_type_id = (SELECT id FROM EventTypes WHERE type_name = 'Login Failed')
        AND ip_address IS NOT NULL
        GROUP BY ip_address, strftime('%Y-%m-%d %H', timestamp)
        HAVING COUNT(*) > 5
    ''')
    return cursor.fetchall()

def critical_weekly():
    cursor.execute('''
        SELECT EventSources.name, COUNT(*)
        FROM SecurityEvents
        JOIN EventTypes ON SecurityEvents.event_type_id = EventTypes.id
        JOIN EventSources ON SecurityEvents.source_id = EventSources.id
        WHERE EventTypes.severity = 'Critical'
        AND timestamp >= datetime('now', '-7 days')
        GROUP BY EventSources.name
    ''')
    return cursor.fetchall()

def find_by_keyword(word):
    cursor.execute('''
        SELECT * FROM SecurityEvents
        WHERE message LIKE ?
    ''', (f'%{word}%',))
    return cursor.fetchall()

def seed_test_data():
    devices = [
        ("Firewall_A", "192.0.2.1", "Firewall"),
        ("Web_Server_Logs", "203.0.113.5", "Web Server"),
        ("IDS_Sensor_B", "198.51.100.12", "IDS"),
    ]
    for device in devices:
        add_source(*device)

    for i in range(12):
        log_event(
            source_name=random.choice(["Firewall_A", "Web_Server_Logs", "IDS_Sensor_B"]),
            type_name=random.choice(["Login Success", "Login Failed", "Port Scan Detected", "Malware Alert"]),
            message=f"Log event {i+1}",
            ip=random.choice(["192.0.2.10", "203.0.113.25", "198.51.100.55", None]),
            user=random.choice(["admin", "user", None])
        )

def main_menu():
    while True:
        print("1. Додати нове джерело подій")
        print("2. Додати новий тип подій")
        print("3. Додати нову подію безпеки")
        print("4. Показати події 'Login Failed' (останні 24 год)")
        print("5. Показати підозрілі IP")
        print("6. Показати критичні події (за 7 днів)")
        print("7. Пошук подій за ключовим словом")

        match input("Оберіть опцію: "):
            case '1':
                n = input("Назва джерела: ")
                l = input("IP або місце: ")
                t = input("Тип: ")
                add_source(n, l, t)

            case '2':
                n = input("Назва типу: ")
                print("Оберіть рівень серйозності: ")
                print("1. Informational\n2. Warning\n3. Critical")
                severity_choice = input()
                severity_map = {'1': 'Informational', '2': 'Warning', '3': 'Critical'}
                s = severity_map.get(severity_choice, 'Informational')
                add_type(n, s)

            case '3':
                s = input("Джерело: ")
                t = input("Тип події: ")
                m = input("Повідомлення: ")
                ip = input("IP: ") or None
                u = input("Користувач: ") or None
                log_event(s, t, m, ip, u)

            case '4':
                for row in recent_failures():
                    print(row)

            case '5':
                for row in multiple_failures():
                    print(row)

            case '6':
                for row in critical_weekly():
                    print(row)

            case '7':
                k = input("Ключове слово: ")
                for row in find_by_keyword(k):
                    print(row)

            case _:
                print("Невірнo")

if __name__ == "__main__":
    initialize_schema()
    populate_event_types()
    seed_test_data()
    main_menu()
    connection.commit()
    connection.close()
