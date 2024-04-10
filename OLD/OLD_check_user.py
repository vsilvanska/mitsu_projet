import sqlite3
import hashlib

# Підключення до бази даних SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

def register_user(username, email, password):
    # Хешування паролю перед збереженням
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        # Додавання нового користувача до бази даних
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        print("Користувач успішно зареєстрований!")
    except sqlite3.IntegrityError:
        print("Користувач з такою електронною адресою вже існує.")

def check_user(email, password):
    # Хешування введеного паролю для порівняння з базою даних
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Пошук користувача з введеними електронною адресою та паролем
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hashed_password))
    user = cursor.fetchone()

    if user:
        print("Ви успішно увійшли до системи!")
    else:
        print("Неправильна електронна адреса або пароль.")

# Приклад реєстрації нового користувача
register_user("user123", "user123@example.com", "password123")

# Приклад перевірки існуючого користувача
check_user("user123@example.com", "password123")

# Закриття з'єднання з базою даних
conn.close()