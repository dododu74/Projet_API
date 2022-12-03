import sqlite3
from list_util import list_util
from ajouter_util import ajouter_util
from info_util import info_util


DB_FILE = 'BDDv1.db'
SQL_FILE = 'BDDv1.sql'

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
    execution_SQL("BDD.sql")


    #Teste de voir_amis()   
    Status 0
    assert voir_amis("Tom.clv") == {'status' : 0, 'data' : []}
    execution_SQL("BDDtest2.sql")
    execution_SQL("BDDtest3.sql")
    assert voir_amis("Tom.clv") == {'status' : 0, 'data' : ['Dorian.jsr']}
    assert voir_amis('Dorian.jsr') == {'status' : 0, 'data' : ["Tom.clv"]}
    execution_SQL("BDD.sql")
    assert voir_amis("Tom.clv") == {'status' : 0, 'data' : []}
    #Status 1
    assert voir_amis(5) == {'status' : 1, 'data' : ['INPUT Type not STR']}
    #Status 2
    assert voir_amis("1234567891011121314151617181920") == {'status' : 2, 'data' : ['INPUT Lenght not between 5, 20']}
    assert voir_amis("123") == {'status' : 2, 'data' : ['INPUT Lenght not between 5, 20']}
    #Status 3
    assert voir_amis("Josseline") == {'status' : 3, 'data' : ['INPUT Registered in UTILISATEUR']}
    
    #Teste de ajouter_amis()
    #Status 0
    assert ajouter_amis('Tom.clv','Nyn.luk') == {"status" : 0, "data": []}
    #Status 1
    assert ajouter_amis('Dorian.jsr',1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert ajouter_amis(1880,'Dorian.jsr') == {"status" : 1, "data" : ['INPUT type not STR']}
    #Status 2
    assert ajouter_amis('Tom.clv','Le.Boulanger.Qui.Fait.Du.Pain') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis('Le.Boulanger.Qui.Fait.Du.Pain','Tom.clv') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis('Nyn.luk',' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_amis(' ','Nyn.luk') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    #Status 3
    assert ajouter_amis('Tom.clv','Xx_Michelle_xX') == {"status" : 3, "data": ['INPUT Not register in UTILISATEUR']}
    assert ajouter_amis('Xx_Michelle_xX','Tom.clv') == {"status" : 3, "data": ['INPUT Not register in UTILISATEUR']}
    #Status 4
    assert ajouter_amis('Tom.clv','Dorian.jsr') == {"status" : 4, "data": ['INPUT already register as friend']}
    #Status 4
    assert ajouter_amis('Tom.clv','Tom.clv') == {"status" : 5, "data": ['INPUT are the same']}
    
    #Teste de supprimer_amis
    #status 0
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
    assert supprimer_amis('Nyn.luk','util.inexistant') == {"status" : 3, "data": ['INPUT Not in database']}
    assert supprimer_amis('util.inexistant','Nyn.luk') == {"status" : 3, "data": ['INPUT Not in database']}
    #status4
    assert supprimer_amis('Dorian.jsr','Nyn.luk') == {"status" : 4, "data" : ['INPUT Not in friendlist']}


    SQL_FILE = 'BDD.sql'
    DB_FILE = 'BDD.db'