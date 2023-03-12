import sqlite3

conn = sqlite3.connect('todo.db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE todo_items
(id INTEGER PRIMARY KEY AUTOINCREMENT,
description TEXT,
is_done INTEGER)
''')
conn.commit()
