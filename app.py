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

@app.route("/events", methods=['GET', 'POST'])
def events():
    if request.method == 'GET':
        return render_template("events.html")
    elif request.method == 'POST':
        session['title'] = request.form['title']
        session['description'] = request.form['description']
        session['date'] = request.form['date']
        session['time'] = request.form['time']

        with open("data1.csv", "a", encoding="utf-8", newline="") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [session['title'], session['description'], session['date'], session['time']]
            writer.writerow(line)

        return redirect('/events')
        
if __name__ == '__main__':
    app.run(debug=True)
