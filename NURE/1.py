from collections import Counter
def word_count(text):
    words = text.lower().split()
    word_freq = Counter(words)
    return word_freq

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
word_freq = word_count(text)
frequent_words = [word for word, count in word_freq.items() if count > 3]
print("Словник частоти слів:", word_freq)
print("Слова, що зустрічаються більше 3 разів:", frequent_words)
