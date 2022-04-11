
import json, mysql.connector

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR[:-5]+'flasksite')) # hack to include correct path on server
from flasksite import flasksite

def drop_tables():
    mydb = connect(secrets)
    mycursor = mydb.cursor()
    sql = f"DROP TABLE IF EXISTS {annot_table_name}; "
    mycursor.execute(sql)
    mydb.commit()
    sql = f"DROP TABLE IF EXISTS {user_table_name}; "
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def create_tables():
    mydb = connect(secrets)
    mycursor = mydb.cursor()

    sql = f"CREATE TABLE {annot_table_name} (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, object_label varchar(50) NOT NULL "
    for annotN in [1,2,3]:
        for key in all_aff_keys:
            sql += f", anno_{annotN}_{key} INT(6) "
        sql += f", anno_{annotN}_id INT(6) "
    sql += ");"
    mycursor.execute(sql)
    mydb.commit()
    sql = f"CREATE TABLE {user_table_name} (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name varchar(50) NOT NULL);"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def fill_object_labels():
    mydb = connect(secrets)
    mycursor = mydb.cursor()
    with open("all_object_labels.pylist", 'r') as file:
        all_objects = eval(file.read())
    sql = f"INSERT INTO {annot_table_name}(object_label) VALUES "
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
    annot_table_name = "web_annotations_2"
    user_table_name = "users"
    all_affs = flasksite.annotationForms()
    all_aff_keys = []
    for aff_set in all_affs:
        all_aff_keys.extend(list(aff_set.keys()))

    drop_tables()
    create_tables()
    fill_object_labels()