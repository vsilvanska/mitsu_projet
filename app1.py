from flask import Flask, render_template, request, redirect, url_for
from flask import session
import csv

app = Flask(__name__)
app.secret_key = b'bafe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET'])
@app.route("/index", methods=['GET'])
def index():  
    return render_template('index1.html')


@app.route("/table", methods=['GET'])
def table():    
    with open("data1.csv", "r", encoding="utf-8") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))      
    return render_template('table.html', data=data)


@app.route("/encode", methods=['GET', 'POST'])
def encode():
    if request.method == 'GET':
        return render_template('encode.html')

    elif request.method == 'POST':
        session['title'] = request.form['title']
        session['date'] = request.form['date']
        session['time'] = request.form['time']        
        new_id = None

        with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            if len(data) == 0:
                new_id = 1
            elif len(data) > 0:
                new_id = int(data[-1]['id']) + 1

        with open("data1.csv", "a", encoding="utf-8", newline="") as fichier_csv:                      
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [new_id, session['title'], session['date'], session['time']]
            writer.writerow(line)
        
        return redirect('/submitted')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html',
                           title=session['title'],
                           date=session['date'],
                           redirect=url_for('table'),
                           delay=5000,
                           )

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        line = []
        with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

            # Rechercher une ligne par son ID et modifier son contenu
            for line in data:
                if line['id'] == id:
                    title = line[title]
                    date =  line[date]
                    time = line['time']

        return render_template('edit.html',
                                title = title,
                                date = date,
                                time = time
                                )
     
    elif request.method == 'POST':
        session['title'] = request.form['title']
        session['date'] = request.form['date']
        session['time'] = request.form['time']
        data = []

        with open("data1.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

        # Rechercher une ligne par son ID et modifier son contenu
        for line in data:
            if line['id'] == id:
                line[title] = session['title']
                line[date] = session['date']
                line['time'] = session['time']

        # Réécrire le fichier CSV avec les modifications
        with open('data1.csv', mode='w', newline='') as file:
            fieldnames = ['id', 'title', 'date', 'time']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
        
        return redirect('/submitted')
     

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
        fieldnames = ['id', 'title', 'date', 'time']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)

    return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)
