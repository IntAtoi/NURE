from collections import Counter

def word_count(text):
    words = text.lower().split()
    word_freq = Counter(words)
    return word_freq

def update_inventory(inventory, product, quantity):
    inventory[product] = inventory.get(product, 0) + quantity
    if inventory[product] <= 0:
        del inventory[product]
    return inventory

def calculate_revenue(sales):
    revenue = {}
    for sale in sales:
        product, quantity, price = sale["продукт"], sale["кількість"], sale["ціна"]
        revenue[product] = revenue.get(product, 0) + quantity * price
    return revenue

def add_task(tasks, name, status="очікує"):
    tasks[name] = status

def remove_task(tasks, name):
    if name in tasks:
        del tasks[name]

def update_task_status(tasks, name, status):
    if name in tasks:
        tasks[name] = status

inventory = {
    "яблука": 10,
    "банани": 3,
    "апельсини": 7,
    "груші": 2
}

update_inventory(inventory, "банани", -2)
update_inventory(inventory, "апельсини", 5)
update_inventory(inventory, "груші", -2)

low_stock = [product for product, count in inventory.items() if count < 5]

sales = [
    {"продукт": "яблука", "кількість": 50, "ціна": 20},
    {"продукт": "банани", "кількість": 30, "ціна": 15},
    {"продукт": "апельсини", "кількість": 10, "ціна": 25},
    {"продукт": "груші", "кількість": 5, "ціна": 30}
]

revenue = calculate_revenue(sales)

high_revenue_products = [product for product, total in revenue.items() if total > 1000]

tasks = {
    "Завдання 1": "очікує",
    "Завдання 2": "в процесі",
    "Завдання 3": "виконано"
}

add_task(tasks, "Завдання 4")
update_task_status(tasks, "Завдання 1", "в процесі")
remove_task(tasks, "Завдання 3")

pending_tasks = [task for task, status in tasks.items() if status == "очікує"]

print("Оновлений склад:", inventory)
print("Продукти з кількістю менше 5:", low_stock)
print("Дохід від продажів:", revenue)
print("Продукти, що принесли дохід більше 1000:", high_revenue_products)
print("Список задач:", tasks)
print("Задачі, що очікують виконання:", pending_tasks)
