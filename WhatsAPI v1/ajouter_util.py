import sqlite3
from list_util import list_util

DB_FILE = 'BDDv1test.db'
SQL_FILE = 'BDDv1.sql'

def ajouter_util(pseudo_utilisateur):
    '''
    Cette fonction permet d'ajouter un nouvel utilisateur à la base de donnée.

    INPUT
        pseudo_utilisateur type STR

    OUTPUT

        Type Dict {
            status : 
            data : []
            }
        
        status -> data : 
            0 -> None
            1 -> 'INPUT Type not STR'
            2 -> 'INPUT Lenght not between 5, 20'
            3 -> 'INPUT already in database'
    '''
    global DB_FILE, SQL_FILE

    data = list_util()['data']

    #test numero 1
    if type(pseudo_utilisateur) != str:
        return {'status' : 1, 'data' : ['INPUT type not STR']}

    #test numero 2
    elif len(pseudo_utilisateur) > 20 or len(pseudo_utilisateur) < 5:
        return {'status' : 2, 'data' : ['INPUT Length not between 5, 20']}
        
    #test numero 3
    for i in range (len(data)):
        if pseudo_utilisateur == data[i]['pseudo_utilisateur']:
            return {'status' : 3, 'data' : ['INPUT already in database']}
        
        
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")

    cur = conn.cursor()
    cur.execute(f"INSERT INTO UTILISATEUR (pseudo_utilisateur) VALUES ('{pseudo_utilisateur}')")

    conn.commit()
    # Fermeture de la connexion a la bdd
    conn.close()

    return {'status' : 0, 'data' : []}