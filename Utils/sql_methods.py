from flasksite import flasksite
import json, mysql.connector

def drop_table():
    mydb = connect(secrets)
    mycursor = mydb.cursor()
    sql = f"DROP TABLE IF EXISTS {name}; "
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def create_table():
    mydb = connect(secrets)
    mycursor = mydb.cursor()

    sql = f"CREATE TABLE {name} (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, object_label varchar(50) NOT NULL "
    for annotN in [1,2,3]:
        for key in all_aff_keys:
            sql += f", anno_{annotN}_{key} INT(6) "
        sql += f", anno_{annotN}_id INT(6) "
    sql += ")"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def fill_object_labels():
    mydb = connect(secrets)
    mycursor = mydb.cursor()
    with open("all_object_labels.pylist", 'r') as file:
        all_objects = eval(file.read())
    sql = f"INSERT INTO {name}(object_label) VALUES "
    for object in all_objects:
        sql += f"('{object}'), \n"
    sql = sql[:-3] # remove trailing comma (and newline)
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def connect(secrets):
    mydb = mysql.connector.connect(
        host="localhost",
        user=secrets["mysqluser"],
        password=secrets["mysqlpass"],
        database="affordance_annotation"
    )
    return mydb

if __name__ == "__main__":
    with open('../flasksite/secrets.json') as file:
        secrets = json.load(file)
    name = "web_annotations_2"

    all_affs = flasksite.annotationForms()
    all_aff_keys = []
    for aff_set in all_affs:
        all_aff_keys.extend(list(aff_set.keys()))

    drop_table()
    create_table()
    fill_object_labels()