import os

# Файл для хранения данных
DATA_FILE = 'finance_data.txt'

def load_entries():
    """ Загрузка записей из файла. """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        data = file.read().split('\n\n')
        return [dict((kv.split(':') for kv in entry.split('\n'))) for entry in data if entry.strip()]

def save_entries(entries):
    """ Сохранение записей в файл. """
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        for entry in entries:
            for key, value in entry.items():
                file.write(f"{key}:{value}\n")
            file.write("\n")

def display_entries(entries):
    """ Отображение всех записей и расчет баланса. """
    total_income = 0
    total_expense = 0
    for entry in entries:
        print(f"Дата: {entry['Дата']}, Категория: {entry['Категория']}, Сумма: {entry['Сумма']}, Описание: {entry.get('Описание', '')}")
        if entry['Категория'] == 'Доход':
            total_income += int(entry['Сумма'])
        else:
            total_expense += int(entry['Сумма'])
    print(f"\nОбщий баланс: {total_income - total_expense}")
    print(f"Всего доходов: {total_income}, Всего расходов: {total_expense}")

def add_entry():
    """ Добавление новой записи. """
    date = input("Введите дату (YYYY-MM-DD): ")
    category = input("Введите категорию (Доход/Расход): ")
    amount = input("Введите сумму: ")
    description = input("Введите описание: ")
    entry = {
        'Дата': date,
        'Категория': category,
        'Сумма': amount,
        'Описание': description
    }
    entries = load_entries()
    entries.append(entry)
    save_entries(entries)
    print("Запись добавлена успешно.")

def edit_entry(entries):
    """ Редактирование существующей записи. """
    date = input("Введите дату записи для редактирования (YYYY-MM-DD): ")
    for i, entry in enumerate(entries):
        if entry['Дата'] == date:
            print(f"Редактирование записи: {entry}")
            entry['Категория'] = input(f"Введите новую категорию (Доход/Расход) [{entry['Категория']}]: ") or entry['Категория']
            entry['Сумма'] = input(f"Введите новую сумму [{entry['Сумма']}]: ") or entry['Сумма']
            entry['Описание'] = input(f"Введите новое описание [{entry['Описание']}]: ") or entry['Описание']
            save_entries(entries)
            print("Запись обновлена успешно.")
            return
    print("Запись не найдена.")

def search_entries(entries):
    """ Поиск записей по критериям. """
    print("Выберите критерий поиска:")
    print("1 - По категории")
    print("2 - По дате")
    print("3 - По сумме")
    criteria = input("Введите номер критерия поиска: ")

    if criteria == "1":
        search_category = input("Введите категорию для поиска (Доход/Расход): ")
        matched_entries = [e for e in entries if e['Категория'] == search_category]
    elif criteria == "2":
        search_date = input("Введите дату для поиска (YYYY-MM-DD): ")
        matched_entries = [e for e in entries if e['Дата'] == search_date]
    elif criteria == "3":
        search_amount = input("Введите сумму для поиска: ")
        matched_entries = [e for e in entries if e['Сумма'] == search_amount]
    else:
        print("Неверный критерий поиска.")
        return

    if matched_entries:
        display_entries(matched_entries)
    else:
        print("Записи не найдены.")

def main():
    """ Главный цикл программы. """
    actions = {
        '1': display_entries,
        '2': add_entry,
        '3': edit_entry,
        '4': search_entries
    }
    
    while True:
        print("\n1 - Показать все записи")
        print("2 - Добавить запись")
        print("3 - Редактировать запись")
        print("4 - Поиск по записям")
        print("q - Выход")
        
        choice = input("Выберите действие: ").strip()
        if choice == 'q':
            break
        elif choice in actions:
            if choice == '2':  # Добавление записи не требует передачи существующих записей.
                actions[choice]()
            else:
                entries = load_entries()
                actions[choice](entries)
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()