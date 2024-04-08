from flask import Flask, render_template, request, redirect, url_for
from flask import session
import csv

app = Flask(__name__)
app.secret_key = b'bahe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'


@app.route('/', methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        session['nom'] = request.form['nom']
        session['prenom'] = request.form['prenom']
        session['datedenaissance'] = request.form['datedenaissance']
        session['nomecole'] = request.form['nomecole']
        session['villeecole'] = request.form['villeecole']
        session['annee'] = request.form['annee']
        session['classe'] = request.form['classe']
        session['option'] = request.form['option']

        new_id = None

        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            if len(data) == 0:
                new_id = 1
            elif len(data) > 0:
                new_id = int(data[-1]['id']) + 1

        with open("data.csv", "a", encoding="utf-8", newline="") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=';')
            line = [new_id, session['nom'], session['prenom'], session['datedenaissance'], session['nomecole'],
                    session['villeecole'], session['annee'], session['classe'], session['option']]
            writer.writerow(line)

        return redirect('/submitted')


@app.route('/submitted')
def submitted():
    return render_template('submitted.html',
                           nom=session['nom'],
                           prenom=session['prenom'],
                           redirect=url_for('index'),
                           delay=5000,
                           )


@app.route('/tableau')
def tableau():
    with open("data.csv", "r", encoding="utf-8") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))
    return render_template('tableau.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)