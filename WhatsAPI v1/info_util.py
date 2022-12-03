import sqlite3
from list_util import list_util

DB_FILE = 'BDDv1.db'
SQL_FILE = 'BDDv1.sql'

def info_util(pseudo_utilisateur):
    '''
    Cette fonction permet d'afficher les informations relatives à un utilisateur.

        INPUT
            pseudo_utilisateur type STR

        OUTPUT
    
            Type Dict {
                status : 
                data : []
                }
            
            status : 
                0 -> {id_utilisateur : INT, pseudo_utilisateur : STR,...}
                1 -> 'Type not STR'
                2 -> 'INPUT Lenght not between 5, 20'
                3 -> 'INPUT Not in database'
    '''
    global DB_FILE, SQL_FILE

    if type(pseudo_utilisateur) != str:
        return ({'status' : 1, 'data' : ['INPUT type not STR']})
    
    elif len(pseudo_utilisateur) <5 or len(pseudo_utilisateur)>20:
        return ({"status" : 2, "data" : ['INPUT Length not between 5, 20']})
    
    erreur3 = True
    data3 = list_util()['data']
    for i in range (len(data3)):
        if pseudo_utilisateur == data3[i]['pseudo_utilisateur']:
            erreur3 = False
            
    if erreur3 == True:
        return {"status" : 3, "data": ['INPUT Not in database']}
    
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute("SELECT * FROM UTILISATEUR")
    rows = cur.fetchall()
    conn.close()

    for elm in rows:
        if elm[1] == pseudo_utilisateur:
            data = [{'id_utilisateur' : elm[0],'pseudo_utilisateur': elm[1]}]
            return({'status' : 0, 'data' : data})