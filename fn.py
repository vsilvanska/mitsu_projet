import sqlite3
import os
import re

def fn_question_alpha(question, erreur):
    reponse = input(question)
    while not reponse.isalpha():
        print(erreur)
        reponse = input(question)
    return reponse

def fn_question_int(question, erreur):
    reponse = input(question)
    while not reponse.isnumeric():
        print(erreur)
        reponse = input(question)
    return reponse

def fn_question_train_code(question, erreur):
    reponse = input(question).upper()
    pattern = re.compile(r'^[A-Z]{2}\d{4}$')
    while not bool(pattern.match(reponse)):
        print(erreur)
        reponse = input(question).upper()
    return reponse

def fn_get_db_name():
    file_path = os.path.realpath(__file__)
    work_dir = os.path.dirname(file_path)
    # print(f'Chemin du dossier script : {work_dir}')
    # print(f'Chemin de la db : {work_dir}/data.db')
    db_name = f'{work_dir}/data.db'
    return db_name

def fn_get_sql_script():
    file_path = os.path.realpath(__file__)
    work_dir = os.path.dirname(file_path)
    sql_init_script = f'{work_dir}/sql-scripts/init-horaire-train.sql'
    return sql_init_script

def fn_init_db(db_name, sql_init_script):
    sqliteConnection = None
    try:            
        with sqlite3.connect(db_name, timeout=10) as sqliteConnection:
            print(f"Connected to the database {db_name}")
            cursor = sqliteConnection.cursor()
            try:
                with open(sql_init_script, "r") as sqlite_file:
                    try:
                        sql_script = sqlite_file.read()
                    except Exception as error:
                        print(f"Error while reading the SQL script: {error}")
                        return
            except Exception as error:
                print(f"Error while opening the SQL file: {error}")
                return                
            try:
                cursor.executescript(sql_script)
                print("SQLite script executed successfully")
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

def fn_input_train_code():
    q_status = "Entrer un code de 6 caractères pour le train (Ex : AB1234) : "
    e_status = "\nErreur : Codes invalides \nEntrer un code de 6 caractères pour le train (Ex : AB1234) : \n"
    train_code = fn_question_train_code(q_status, e_status)
    return train_code
    
def fn_set_train_code(db_name, train_code):
    sqliteConnection = None
    try:            
        with sqlite3.connect(db_name, timeout=10) as sqliteConnection:
            print(f"Connected to the database {db_name}")
            cursor = sqliteConnection.cursor()                                
            try:
                print(f"Commande SQL exécutée : INSERT INTO TRAIN (code) VALUES ('{train_code}');")
                cursor.execute(f"INSERT INTO TRAIN (code) VALUES ('{train_code}');")
                # print("SQLite script executed successfully")
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

def fn_init_set_train_code_menu():
    q_choix_1 = "[1] Ajouter un train"
    q_choix_2 = "[2] Quitter"
    list_menu = [q_choix_1, q_choix_2]
    return list_menu

def fn_set_train_code_menu(list_menu):
    print(f'\n----Menu - Projet Horaire train----')
    for item in list_menu:
        print(f'{item}')
    q_status = "Entrer votre choix (1-2) : "
    e_status = "\nErreur : Caractères invalides\n"
    status = int(fn_question_int(q_status, e_status))
    match status:
        case 1:
            train_code = fn_input_train_code()
            db_name = fn_get_db_name()
            fn_set_train_code(db_name, train_code)
            return True
        case 2:
            print(f'Fermeture de l\'application')
            return False
        case _:
            print(f'\nErreur : Choix non-valide\n')
            return True
    
def fn_create_db():
    try:
        list_menu = fn_init_set_train_code_menu()
        create_db_out = fn_set_train_code_menu(list_menu)            
    except Exception as error:
        print(f"{error}")
    finally:
        return create_db_out

def fn_read_db(db_name):
    sqliteConnection = None
    try:            
        with sqlite3.connect(db_name, timeout=10) as sqliteConnection:
            print(f"Connected to the database {db_name}")
            cursor = sqliteConnection.cursor()                                
            try:
                cursor.execute(f"SELECT * FROM TRAIN;")
                data = cursor.fetchall()
                print("SQLite script executed successfully")
                print(f'\nExecution du SELECT :')
                for line in data:
                    print(line)
                print()
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

def fn_question_id(question, erreur):
    train_id = input(question)
    while not train_id.isnumeric():
        print(erreur)
        train_id = input(question)
    return train_id

def fn_create_train_code():
    q_status = "Entrer un code de 6 caractères pour le train (Ex : AB1234) : "
    e_status = "\nErreur : Codes invalides \nEntrer un code de 6 caractères pour le train (Ex : AB1234) : \n"
    train_code = fn_question_train_code(q_status, e_status)
    return train_code

def fn_update_db(train_code, train_id, db_name):
    sqliteConnection = None
    try:            
        with sqlite3.connect(db_name, timeout=10) as sqliteConnection:
            print(f"Connected to the database {db_name}")
            cursor = sqliteConnection.cursor()
            try:
                print(f"UPDATE TRAIN SET Code='{train_code}' WHERE train_id='{train_id}';")
                cursor.execute(f"UPDATE TRAIN SET Code='{train_code}' WHERE train_id='{train_id}';")
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
    
def fn_init_update_menu():
    q_choix_1 = "[1] Modifier un train"
    q_choix_2 = "[2] Quitter"
    list_menu = [q_choix_1, q_choix_2]
    return list_menu

def fn_update_menu(list_menu):
    print(f'\n----Menu - Projet Horaire train----')
    for item in list_menu:
        print(f'{item}')
    q_status = "Entrer votre choix (1-2) : "
    e_status = "\nErreur : Caractères invalides\n"
    status = int(fn_question_int(q_status, e_status))
    match status:
        case 1:
            db_name = fn_get_db_name()
            train_id = fn_question_id()
            train_code = fn_create_train_code()
            fn_update_db(train_code, train_id, db_name)
        case 2:
            print(f'Fermeture de l\'application')
            return False, 0, 0
        case _:
            print(f'\nErreur : Choix non-valide\n')
            return True, 0, 0

def fn_delete_db(self):
    sqliteConnection = None
    try:            
        with sqlite3.connect(self.db_name, timeout=10) as sqliteConnection:
            print(f"Connected to the database {self.db_name}")
            cursor = sqliteConnection.cursor()
            try:
                cursor.execute("DELETE FROM TRAIN WHERE train_id = 4;")                    
                print("SQLite script executed successfully")                    
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
            
def fn_init_delete_train_code_menu():
    q_choix_1 = "[1] Supprimer un train"
    q_choix_2 = "[2] Quitter" 
    list_menu = [q_choix_1, q_choix_2]
    return list_menu

def fn_delete_db():
    try:
        list_menu = fn_init_delete_train_code_menu()
        create_db_out = fn_delete_train_code_menu(list_menu)            
    except Exception as error:
        print(f"{error}")
    finally:
        return create_db_out