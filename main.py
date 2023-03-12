import sqlite3


class TodoItem:
    def __init__(self, text):
        self.text = text
        self.is_done = False

    def check(self):
        self.is_done = True

    def uncheck(self):
        self.is_done = False


class Todo:
    def __init__(self):
        self.todo_items = []

    def add_todo(self, todo_item):
        self.todo_items.append(todo_item)

    def list_items(self):
        for i, item in enumerate(self.todo_items):
            print(f"{i}: {item.text} ({'done' if item.is_done else 'not done'})")

    def find(self, word):
        found_items = []
        for i, item in enumerate(self.todo_items):
            if word in item.text:
                found_items.append((i, item))
        return found_items

    def save_to_db(self, conn):
        with conn:
            cur = conn.cursor()

            for item in self.todo_items:
                cur.execute("INSERT INTO todo_items (text, is_done) VALUES (?, ?)", (item.text, item.is_done))

    def load_from_db(self, conn):
        with conn:
            cur = conn.cursor()


            rows = cur.fetchall()
            for row in rows:
                item = TodoItem(row[1])
                item.is_done = bool(row[2])


if __name__ == '__main__':
    menu = {
        '1': 'add_todo',
        '2': 'list_items',
        '3': 'find',
        '4': 'save_to_db',
        '5': 'load_from_db',
        '6': 'exit'
    }
    todo = Todo()

    import pickle

    db = {"todo_items": []}
    with open("todoo.db", "wb") as f:
        pickle.dump(db, f)

        conn = sqlite3.connect('todoo.db')

    while True:
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Показать список")
        print("3. Найти")
        print("4. Сохранить в ДБ")
        print("5. Загрузить из ДБ")
        print("6. Выйти")

        choice = input("Выберите пункт от 1 до 6: ")
        if choice == '6':
            break
        method_name = menu.get(choice)
        if method_name:
            method = getattr(todo, method_name)
            if method_name == 'add_todo':
                text = input("Введите Предмет: ")
                item = TodoItem(text)
                method(item)
            elif method_name == 'load_from_db':
                method(conn)
                print("Todo Items loaded from DB.")
            elif method_name == 'find':
                word = input("Введите слово, которое хотите найти: ")
                found_items = method(word)
                if found_items:
                    for i, item in found_items:
                        print(f"{i}: {item.text}")

                else:
                    print("Нет таких предметов.")
            elif method_name == 'save_to_db':
                method(conn)
                print("Предметы были сохранены в БД.")

                conn.close()





