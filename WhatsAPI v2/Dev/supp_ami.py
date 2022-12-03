import sqlite3
from voir_amis import voir_amis

DB_FILE = 'BDD.db'
SQL_FILE = 'BDD.sql'

def supprimer_amis(pseudo_utilisateur, pseudo_utilisateur_a_supp):
    '''
    Cette fonction permet de supprimer un ami choisit.

    INPUT
        pseudo_utilisateur type STR
        pseudo_utilisateur_a_supp type STR

    OUTPUT

        Type Dict {
            status : 
            data : []
            }
        
        status : 
            0 -> None
            1 -> 'INPUT Type not STR'
            2 -> 'INPUT Lenght not between 5, 20'
            4 -> 'INPUT Not in friendlist'
    '''

    #data_util = list_util()['data']
    data_amis = voir_amis(pseudo_utilisateur)['data']

    if type(pseudo_utilisateur) != str or type(pseudo_utilisateur_a_supp) != str:
        return ({'status' : 1, 'data' : ['INPUT type not STR']})

    elif len(pseudo_utilisateur) <5 or len(pseudo_utilisateur)>20:
        return ({"status" : 2, "data" : ['INPUT Length not between 5, 20']})
    elif len(pseudo_utilisateur_a_supp) <5 or len(pseudo_utilisateur_a_supp)>20:
        return ({"status" : 2, "data" : ['INPUT Length not between 5, 20']})

    #test status 4
    erreur4 = True
    for i in range (len(data_amis)):
        if  pseudo_utilisateur_a_supp == data_amis[i]:
            erreur4 = False
    if erreur4:    
        return {'status' : 4, 'data' : ['INPUT Not in friendlist']}
            

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM AMITIE WHERE  util1 ='{pseudo_utilisateur}' AND  util2 = '{pseudo_utilisateur_a_supp}'")
    rows = cur.fetchall()
    conn.close()

    return{'status' :0, 'data' : []}





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

def voir_amis(pseudo_utilisateur):
    '''
    Cette fonction permet d'afficher le pseudo des personnes qui sont les amis de "pseudo_utilisateur"

    INPUT
        pseudo_utilisateur type STR

    OUTPUT

        Type Dict {
            status : 
            data : []
            }
        
        status : 
            0 -> pseudo_utilisateur type STR, . . . 
            1 -> 'INPUT Type not STR'
            2 -> 'INPUT Lenght not between 5, 20'
            3 -> 'INPUT Not Registered in UTILISATEUR'
    '''
    global DB_FILE
    if type(pseudo_utilisateur) != str:
        return {'status' : 1, 'data' : ['INPUT Type not STR']}

    elif len(pseudo_utilisateur) < 5 or len(pseudo_utilisateur) > 20:
        return {'status' : 2, 'data' : ['INPUT Lenght not between 5, 20']}

    erreur3 = True
    data3 = list_util()['data']
    for i in range (len(data3)):
        if pseudo_utilisateur == data3[i]['pseudo_utilisateur']:
            erreur3 = False

    if erreur3 == True:
        return {'status' : 3, 'data': ['INPUT Not Registered in UTILISATEUR']}
    

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute(f"SELECT util2 FROM AMITIE WHERE util1=\'{pseudo_utilisateur}\'")
    rows = cur.fetchall()
    conn.close()
    
    data = []
    for elm in rows:
        data.append(elm[0])

    return({'status' : 0, 'data' : data})


def execution_SQL(SQL_FILE):
    global DB_FILE 

    with open(SQL_FILE, 'r') as f :
        createSql = f.read()
    # Placement des requêtes dans un tableau
    sqlQueries = createSql.split(";")

    try:
        # Ouverture de la connexion avec la bdd
        conn = sqlite3.connect(DB_FILE)
        #On active les foreign key
        conn.execute("PRAGMA foreign_keys = 1")
    except sqlite3.Error as e:
        print(e)


    # Execution de toutes les requêtes du tableau
    cursor = conn.cursor()
    for query in sqlQueries:
        cursor.execute(query)
    # commit des modifications
    conn.commit()
    # fermeture de la connexion
    conn.close()

if __name__ == "__main__":
    DB_FILE = 'BDDtest.db'
    execution_SQL('BDD.sql')
    execution_SQL('BDDtest2.sql')
    execution_SQL('BDDtest3.sql')


    #Teste de supprimer_amis
    #status 0()
    print(supprimer_amis('Tom.clv','Dorian.jsr'))
    assert supprimer_amis('Tom.clv','Dorian.jsr') == {"status" : 0, "data": []}
    #status 1
    assert supprimer_amis('Dorian.jsr',1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert supprimer_amis(1880,'Dorian.jsr') == {"status" : 1, "data" : ['INPUT type not STR']}
    #status 2
    assert supprimer_amis('Tom.clv','Le.Boulanger.Qui.Fait.Du.Pain') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert supprimer_amis('Le.Boulanger.Qui.Fait.Du.Pain','Tom.clv') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert supprimer_amis('Nyn.luk',' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert supprimer_amis(' ','Nyn.luk') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    #status 3
    #assert supprimer_amis('Nyn.luk','util.inexistant') == {"status" : 3, "data": ['INPUT Not in database']}
    #assert supprimer_amis('util.inexistant','Nyn.luk') == {"status" : 3, "data": ['INPUT Not in database']}
    #status4
    assert supprimer_amis('Dorian.jsr','Nyn.luk') == {"status" : 4, "data" : ['INPUT Not in friendlist']}

    

    DB_FILE = 'BDD.db'