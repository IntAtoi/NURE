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
print("Оновлений склад:", inventory)
print("Продукти з кількістю менше 5:", low_stock)
