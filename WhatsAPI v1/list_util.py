import sqlite3

DB_FILE = 'BDDv1test.db'
SQL_FILE = 'BDDv1.sql'

def list_util():
    '''
    Cette fonction permet d'afficher tous les utilisateurs de WhatsAPI.

    OUTPUT

        Type Dict {
            status : 
            data : []
            }

        status -> data : 
            0 -> [{id_utilisateur : (type INT), pseudo_utilisateur : (type STR)}, . . . ]
            1 -> 'INPUT Type incorrect'
            2 -> 'INPUT Lenght incorrect'
            3 -> 'INPUT Not Correspond'
    '''
    global DB_FILE, SQL_FILE


    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")

    cur = conn.cursor()
    cur.execute("SELECT * FROM UTILISATEUR")
    rows = cur.fetchall()
    conn.close()
    
    status = 0
    data = []
    for elm in rows :
        data.append({"id_utilisateur" : elm[0], "pseudo_utilisateur" : elm[1] })
        
    return { 'status' : status, 'data' : data }