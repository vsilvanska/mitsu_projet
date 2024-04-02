CREATE TABLE nom
(
    nom_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    code VARCHAR(255)
);

CREATE TABLE prenom
(
    prenom_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    nom_id INT,
    FOREIGN KEY (train_id) REFERENCES train(train_id)
);

CREATE TABLE password
(
    prenom_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    nom_id INT,
    FOREIGN KEY (train_id) REFERENCES train(train_id)
);