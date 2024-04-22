from flask import Flask, render_template, request, redirect, url_for
from flask import session
import logging
import csv
import jinja2
from email_validator import validate_email, EmailNotValidError

def verif_email(email):
	try:
	# validate and get info
		v = validate_email(email)
		# replace with normalized form
		print("True")
	except EmailNotValidError as e:
		# email is not valid, exception message is human-readable
		print(str(e))

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.secret_key = b'bahe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    with open("data.csv", "r", encoding="utf-8") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))      
    return render_template('index.html', data=data)

@app.route("/base")
def home():
    return render_template("base.html", title="Mitsuruki")


@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')
    
    elif request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['password'] = request.form['password']


        new_id = None

        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            if len(data) == 0:
                 new_id = 1
            elif len(data) > 0:
                new_id = int(data[-1]['id']) + 1  

        with open("data.csv", "a", encoding="utf-8", newline="") as fichier_csv:                      
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [new_id, session['name'], session['email'], session['password']]
            writer.writerow(line)
    
        return redirect('/profile')

@app.route('/profile')
def submitted():
    return render_template('profile.html',
                           name=session['name'],
                           email=session['email'],
                           prenom=session['password'],
                           )

if __name__ == '__main__':
	app.run(debug=True)