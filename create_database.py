from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# Підключення до бази даних SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Створення таблиці користувачів, якщо вона ще не існує
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)''')
conn.commit()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    # Хешування паролю перед збереженням
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        # Додавання нового користувача до бази даних
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        return jsonify({'message': 'Реєстрація пройшла успішно'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Користувач з такою електронною адресою вже існує'}), 400

if __name__ == '__main__':
    app.run(debug=True)