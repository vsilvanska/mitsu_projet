from flask import Flask, render_template, request, redirect, url_for
from flask import session
import csv

app = Flask(__name__)
app.secret_key = b'bahe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    with open("data.csv", "r", encoding="utf-8") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))      
    return render_template('index.html', data=data)


@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')
    
    elif request.method == 'POST':
        session['name'] = request.form['name']
        session['mot'] = request.form['mot']


        new_id = None

        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            if len(data) == 0:
                 new_id = 1
            elif len(data) > 0:
                new_id = int(data[-1]['id']) + 1  

        with open("data.csv", "a", encoding="utf-8", newline="") as fichier_csv:                      
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [new_id, session['name'], session['mot']]
            writer.writerow(line)
    
        return redirect('/profile')

@app.route('/profile')
def submitted():
    return render_template('profile.html',
                           name=session['name'],
                           prenom=session['mot'],
                           )

if __name__ == '__main__':
	app.run(debug=True)