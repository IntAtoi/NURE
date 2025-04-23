import re
import hashlib

# Завдання 1
def analyze_log_file(log_file_path):
    response_codes = {}
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.search(r'"\s(\d{3})\s', line)
                if match:
                    code = match.group(1)
                    response_codes[code] = response_codes.get(code, 0) + 1
    except FileNotFoundError:
        print(f"Файл не знайдено: {log_file_path}")
    except IOError as e:
        print(f"Помилка при читанні файлу: {e}")
    return response_codes

# Завдання 2
def generate_file_hashes(file_paths):
    hashes = {}
    for path in file_paths:
        try:
            with open(path, 'rb') as file:
                file_data = file.read()
                file_hash = hashlib.sha256(file_data).hexdigest()
                hashes[path] = file_hash
        except FileNotFoundError:
            print(f"Файл не знайдено: {path}")
        except IOError as e:
            print(f"Помилка при читанні файлу {path}: {e}")
    return hashes

# Завдання 3
def filter_ips(input_file_path, output_file_path, allowed_ips):
    ip_counts = {}

    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                match = re.match(r'^(\d{1,3}(?:\.\d{1,3}){3})', line)
                if match:
                    ip = match.group(1)
                    if ip in allowed_ips:
                        ip_counts[ip] = ip_counts.get(ip, 0) + 1
    except FileNotFoundError:
        print(f"Вхідний файл не знайдено: {input_file_path}")
        return
    except IOError as e:
        print(f"Помилка при читанні вхідного файлу: {e}")
        return

    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for ip, count in ip_counts.items():
                outfile.write(f"{ip} - {count}\n")
    except IOError as e:
        print(f"Помилка при записі до файлу: {e}")

if __name__ == "__main__":
    # Завдання 1
    log_path = r"E:\mgnat\desktop\IDE\pycharm\PycharmProjects\lb2\apache_logs.txt"
    results = analyze_log_file(log_path)
    print("Коди відповідей:")
    for code, count in results.items():
        print(f"{code}: {count}")

    # Завдання 2
    files_to_hash = [
        r"E:\mgnat\desktop\IDE\pycharm\PycharmProjects\lb2\apache_logs.txt",
    ]
    hashes = generate_file_hashes(files_to_hash)
    print("\nSHA-256 хеші файлів:")
    for path, hash_val in hashes.items():
        print(f"{path}: {hash_val}")

    # Завдання 3
    allowed_ips = ['50.16.19.13', '46.105.14.53', '208.115.111.72', '220.181.108.153', '100.43.83.137']
    output_file = r"E:\mgnat\desktop\IDE\pycharm\PycharmProjects\lb2\filtered_ips.txt"
    filter_ips(log_path, output_file, allowed_ips)
    print(f"\nРезультати фільтрації IP збережено до {output_file}")
