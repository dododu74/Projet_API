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
    DB_FILE = 'BDDv1test.db'

    #teste de list_util() avec une bdd vide
    execution_SQL('BDDv1test1.sql')
    assert list_util() == {"status" : 0, "data" : []}
    #teste de list_util() avec une bdd non vide
    execution_SQL('BDDv1test2.sql')
    assert list_util() == {"status" : 0, "data" : [{"id_utilisateur" : 1, "pseudo_utilisateur" : 'Tom.clv'},{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'}]}
	
	
    #teste de ajouter_util()
    assert ajouter_util('Nyn.luk') == {"status" : 0, "data" : []}
    assert ajouter_util(1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert ajouter_util(' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_util('Le.Boulanger.Qui.Fait.Du.Pain ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert ajouter_util('Tom.clv') == {"status" : 3, "data" : ['INPUT already in database']}
    #teste de ajouter_util() (état de la bdd après les testes)
    assert list_util() == {"status" : 0, "data" : [{"id_utilisateur" : 1, "pseudo_utilisateur" : 'Tom.clv'},{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'},{"id_utilisateur" : 3, "pseudo_utilisateur" : 'Nyn.luk'}]}

    #teste de info_util()
    assert info_util('Dorian.jsr') == {"status" : 0, "data": [{"id_utilisateur": 2, "pseudo_utilisateur": 'Dorian.jsr'}]}
    assert info_util(1880) == {"status" : 1, "data" : ['INPUT type not STR']}
    assert info_util('Le.Boulanger.Qui.Fait.Du.Pain') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert info_util(' ') == {"status" : 2, "data" : ['INPUT Length not between 5, 20']}
    assert info_util('util.inexistant') == {"status" : 3, "data": ['INPUT Not in database']}