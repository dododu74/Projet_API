import sqlite3

DB_FILE = "BDD.db"

def ajouter_amis(pseudo_utilisateur, pseudo_utilisateur_a_ajouter):
    '''
    Cette fonction permet d'ajouter un amis a un utilisateur précis.

    INPUT
        pseudo_utiur type STR
        pseudo_utilisateur_a_ajouter type STR

    OUTPUT

        Type Dict {
            status : 
            data : []
            }
        
        status : 
            0 -> None
            1 -> 'INPUT Type not STR'
            2 -> 'INPUT Lenght not between 5, 20'
            3 -> 'INPUT Not register in UTILISATEUR'
            4 -> 'INPUT already register as friend'
            5 -> 'INPUT are the same'
    '''
    global DB_FILE

    data_util = list_util()['data']
    data_amis = voir_amis(pseudo_utilisateur)['data']

    #test status 1
    if type(pseudo_utilisateur) != str or type(pseudo_utilisateur_a_ajouter) != str:
        return {'status' : 1, 'data' : ['INPUT type not STR']}

    #test status 2
    elif len(pseudo_utilisateur) > 20 or len(pseudo_utilisateur) < 5:
        return {'status' : 2, 'data' : ['INPUT Length not between 5, 20']}
    elif len(pseudo_utilisateur_a_ajouter) > 20 or len(pseudo_utilisateur_a_ajouter) < 5:
        return {'status' : 2, 'data' : ['INPUT Length not between 5, 20']}

    #test status 3
    erreur3_1 = True
    erreur3_2 = True
    for i in range (len(data_util)):
        if pseudo_utilisateur == data_util[i]['pseudo_utilisateur']:
            erreur3_1 = False
        if pseudo_utilisateur_a_ajouter == data_util[i]['pseudo_utilisateur']:
            erreur3_2 = False
    if erreur3_1 == True or erreur3_2 == True:
        return {'status' : 3, 'data' : ['INPUT Not register in UTILISATEUR']}

    #test status 4
    for i in range (len(data_amis)):
        if pseudo_utilisateur_a_ajouter == data_amis[i]:
            return {'status' : 4, 'data' : ['INPUT already register as friend']}
    
    #test status 5
    if pseudo_utilisateur == pseudo_utilisateur_a_ajouter :
        return {'status' : 5, 'data' : ['INPUT are the same']}
        
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO AMITIE (util1, util2) VALUES ('{pseudo_utilisateur}','{pseudo_utilisateur_a_ajouter}')")
    conn.commit()
    # Fermeture de la connexion a la bdd
    conn.close()

    return {'status' : 0, 'data' : []}

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
    
    #test de la fonction ajouter_amis
    assert ajouter_amis('Tom.clv','Nyn.luk') == {"status" : 0, "data": []}

    assert ajouter_amis('Dorian.jsr',1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert ajouter_amis(1880,'Dorian.jsr') == {"status" : 1, "data" : ['INPUT type not STR']}

    assert ajouter_amis('Tom.clv','Le.Boulanger.Qui.Fait.Du.Pain') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis('Le.Boulanger.Qui.Fait.Du.Pain','Tom.clv') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis('Nyn.luk',' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis(' ','Nyn.luk') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}

    assert ajouter_amis('Tom.clv','Xx_Michelle_xX') == {"status" : 3, "data": ['INPUT Not register in UTILISATEUR']}
    assert ajouter_amis('Xx_Michelle_xX','Tom.clv') == {"status" : 3, "data": ['INPUT Not register in UTILISATEUR']}

    assert ajouter_amis('Tom.clv','Dorian.jsr') == {"status" : 4, "data": ['INPUT already register as friend']}

    assert ajouter_amis('Tom.clv','Tom.clv') == {"status" : 5, "data": ['INPUT are the same']}

    DB_FILE = 'BDD.db'