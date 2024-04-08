import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask import session
import fn as fnht

# Створення підключення до бази даних

conn = sqlite3.connect('mydatabase.db')

# Створення курсору для виконання SQL-запитів

cursor = conn.cursor()

# Виконання SQL-запиту

cursor.execute('SELECT * FROM People')

# Отримання результатів запиту

results = cursor.fetchall()

# Закриття підключення

conn.close()

