import sqlite3

# Створення підключення до бази даних

conn = sqlite3.connect('mydatabase.db')

# Створення курсору для виконання SQL-запитів

cursor = conn.cursor()

# Виконання SQL-запиту

cursor.execute('SELECT * FROM Users')

# Отримання результатів запиту

results = cursor.fetchall()

# Закриття підключення

conn.close()

