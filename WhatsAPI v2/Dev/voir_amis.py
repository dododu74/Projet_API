import sqlite3
from mainV2 import list_util

DB_FILE = 'BDD.db'
SQL_FILE = 'BDD.sql'

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
    execution_SQL("BDD.sql")
    execution_SQL("BDDtest2.sql")

    #Teste de voir_amis()   
    #Status 0
    assert voir_amis("Tom.clv") == {'status' : 0, 'data' : []}
    execution_SQL("BDDtest3.sql")

    assert voir_amis("Tom.clv") == {'status' : 0, 'data' : ['Dorian.jsr']}
    assert voir_amis('Dorian.jsr') == {'status' : 0, 'data' : ["Tom.clv"]}
    execution_SQL("BDDtest1.sql")
    execution_SQL("BDD.sql")
    assert voir_amis("Tom.clv") == {'status' : 0, 'data' : []}
    #Status 1
    assert voir_amis(5) == {'status' : 1, 'data' : ['INPUT Type not STR']}
    #Status 2
    assert voir_amis("1234567891011121314151617181920") == {'status' : 2, 'data' : ['INPUT Lenght not between 5, 20']}
    assert voir_amis("123") == {'status' : 2, 'data' : ['INPUT Lenght not between 5, 20']}
    #Status 3
    assert voir_amis("Josseline") == {'status' : 3, 'data' : ['INPUT Not Registered in UTILISATEUR']}

    DB_FILE = 'BDD.db'