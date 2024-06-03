from flask import Flask, render_template, request, redirect, url_for, session
import logging
import csv
from email_validator import validate_email, EmailNotValidError
import sqlite3
import os

def verif_email(email):
    try:
        v = validate_email(email)
        print("True")
    except EmailNotValidError as e:
        print(str(e))

def fn_get_db_name():
    file_path = os.path.realpath(__file__)
    work_dir = os.path.dirname(file_path)
    db_name = f'{work_dir}/data.db'
    return db_name

def fn_encode_event(db_name, event_list):
    sqliteConnection = None
    try:            
        with sqlite3.connect(db_name, timeout=10) as sqliteConnection:
            print(f"Connected to the database {db_name}")
            cursor = sqliteConnection.cursor()                                
            try:
                print(f"Commande SQL exécutée : INSERT INTO EVENTS (title_e, date_e, description_e) VALUES ('{event_list[0]}','{event_list[1]}','{event_list[2]}');")
                cursor.execute(f"INSERT INTO EVENTS (title_e, date_e, description_e) VALUES ('{event_list[0]}','{event_list[1]}','{event_list[2]}');")
                print("SQLite command executed successfully")
            except sqlite3.Error as error:
                print(f"Error while executing SQLite script: {error}")
            finally:
                cursor.close()
    except sqlite3.Error as error:
        print(f"Error while connecting to SQLite: {error}")
    except Exception as error:
        print(f"{error}")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def fn_read_db(db_name):
    sqliteConnection = None
    try:            
        with sqlite3.connect(db_name, timeout=10) as sqliteConnection:
            print(f"Connected to the database {db_name}")
            cursor = sqliteConnection.cursor()                                
            try:
                cursor.execute(f"SELECT * FROM EVENTS;")
                data = cursor.fetchall()
                print("SQLite script executed successfully")
                print(f'\nExecution du SELECT :')
                for line in data:
                    print(line)
                print()
                # Transformation des données d'une table SQL contenant (title, date, description_e) récupérée à l'aide de (SELECT * FROM EVENTS;) en liste de dictionnaire
                # Récupérez les noms des colonnes
                column_names = [description[0] for description in cursor.description]
                # Transformez les données en une liste de dictionnaires
                event_list = []
                for line in data:
                    event = dict(zip(column_names, line))
                    event_list.append(event)
            except sqlite3.Error as error:
                print(f"Error while executing SQLite script: {error}")
            finally:
                cursor.close()
    except sqlite3.Error as error:
        print(f"Error while connecting to SQLite: {error}")
    except Exception as error:
        print(f"{error}")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            return event_list
                    

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.secret_key = b'bahe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    with open("data1.csv", "r", encoding="utf-8") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))
    return render_template('index.html', data=data)

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')
    
    elif request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['password'] = request.form['password']

        new_id = None

        with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            if len(data) == 0:
                new_id = 1
            elif len(data) > 0:
                new_id = int(data[-1]['id']) + 1  

        with open("data1.csv", "a", encoding="utf-8", newline="") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [new_id, session['name'], session['email'], session['password']]
            writer.writerow(line)
    
        return redirect('/profile')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route("/events", methods=['GET'])
def events(): 
    db_name = fn_get_db_name()
    data = fn_read_db(db_name)
    return render_template('events.html', data=data)


@app.route("/encode", methods=['GET', 'POST'])
def encode():
    if request.method == 'GET':
        return render_template('encode.html')

    elif request.method == 'POST':
        session['title'] = request.form['title']
        session['date'] = request.form['date']
        session['desc'] = request.form['desc']
        event_list = [session['title'], session['date'], session['desc']]
        db_name = fn_get_db_name()
        fn_encode_event(db_name,event_list)
        
        return redirect('/events')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        line = []
        print(id)
        db_name = fn_get_db_name()
        data = fn_read_db(db_name)

        # Rechercher une ligne par son ID et modifier son contenu
        for line in data:
            print(line)
            if int(line['events_id']) == int(id):
                print(f"if ok")
                title = line['title_e']
                print(title)
                date =  line['date_e']
                print(date)
                desc = line['description_e']
                print(desc)

        return render_template('edit.html',
                                title = title,
                                date = date,
                                desc = desc
                                )
     
    elif request.method == 'POST':
        session['title'] = request.form['title']
        session['date'] = request.form['date']
        session['desc'] = request.form['desc']
        data = []

        with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

        # Rechercher une ligne par son ID et modifier son contenu
        for line in data:
            if line['id'] == id:
                line['title'] = session['title']
                line['date'] = session['date']
                line['desc'] = session['desc']

        # Réécrire le fichier CSV avec les modifications
        with open('data1.csv', mode='w', newline='') as file:
            fieldnames = ['id', 'title', 'date', 'desc']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
        
        return redirect('/events')
     

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    data = []

    with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))

    # Search for the dictionary that contains the line to be deleted
    for line in data:
        if line['id'] == id:
            # Remove the dictionary from the list
            data.remove(line)

    # Write the modified list of dictionaries to the CSV file
    with open('data1.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'title', 'date', 'desc']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)

    return redirect('/')

        
if __name__ == '__main__':
    app.run(debug=True)
