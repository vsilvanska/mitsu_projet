from flask import Flask, render_template, request, redirect, url_for, session
import logging
import csv
from email_validator import validate_email, EmailNotValidError

def verif_email(email):
    try:
        v = validate_email(email)
        print("True")
    except EmailNotValidError as e:
        print(str(e))

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.secret_key = b'bahe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET'])
@app.route("/index1", methods=['GET'])
def index():    
    with open("data1.csv", "r", encoding="utf-8") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))      
    return render_template('index1.html', data=data)


@app.route("/encode", methods=['GET', 'POST'])
def encode():
    if request.method == 'GET':
        return render_template('encode.html')

    elif request.method == 'POST':
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']        
        new_id = None

        with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            if len(data) == 0:
                new_id = 1
            elif len(data) > 0:
                new_id = int(data[-1]['id']) + 1

        with open("data1.csv", "a", encoding="utf-8", newline="") as fichier_csv:                      
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [new_id, session['first_name'], session['last_name'], session['email']]
            writer.writerow(line)
        
        return redirect('/submitted')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html',
                           first_name=session['first_name'],
                           last_name=session['last_name'],
                           redirect=url_for('table'),
                           delay=5000,
                           )

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        line = []
        with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

            for line in data:
                if line['id'] == id:
                    prenom = line['prenom']
                    nom =  line['nom']
                    email = line['email']

        return render_template('edit.html',
                                prenom = prenom,
                                nom = nom,
                                email = email
                                )
     
    elif request.method == 'POST':
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        data = []

        with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

        for line in data:
            if line['id'] == id:
                line['prenom'] = session['first_name']
                line['nom'] = session['last_name']
                line['email'] = session['email']

        with open('data1.csv', mode='w', newline='') as file:
            fieldnames = ['id', 'prenom', 'nom', 'email']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
        
        return redirect('/submitted')
     

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    data = []

    with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))

    for line in data:
        if line['id'] == id:
            data.remove(line)

    with open('data1.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'prenom', 'nom', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)

    return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)