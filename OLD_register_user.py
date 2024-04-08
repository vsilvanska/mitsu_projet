import sqlite3

# Підключення до бази даних SQLite (створюється, якщо не існує)
conn = sqlite3.connect('users.db')

# Створення курсора для виконання SQL-запитів
cursor = conn.cursor()

# Створення таблиці користувачів
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)''')

# Збереження змін до бази даних
conn.commit()

# Закриття з'єднання з базою даних
conn.close()