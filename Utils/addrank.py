
import json, mysql.connector
import time
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR[:-5]+'flasksite')) # hack to include correct path on server


def set_params():
    mydb = connect(secrets)
    mycursor = mydb.cursor()
    sql = f"SELECT object_label FROM web_annotations"
    mycursor.execute(sql)
    all_objects = list(mycursor)


    obj_exclude = {}
    obj_n = {}

    with open("transfer table.csv") as file:
        data = file.readlines()

    for line in data:
        item = line.split(",")
        obj = item[0][1:-1]
        index = item[1]

        if obj in obj_n.keys():
            obj_n[obj] = obj_n[obj] + int(item[2])
        else:
            obj_n[obj] = int(item[2])

        if item[3] != "":
            ## if object should be excluded
            obj_exclude[obj] = 1
            ## excluded items should always have a replacement value
            assert item[6][:-1] != '#N/A'
            ## add n object to replacement
            if item[6][1:-2] in obj_n.keys():
                obj_n[item[6][1:-2]] = obj_n[item[6][1:-2]] + int(item[2])
            else:
                obj_n[item[6][1:-2]] = int(item[2])

        else:
            obj_exclude[obj] = 0


    for object in all_objects:
        assert object[0] in obj_exclude.keys()
        assert object[0] in obj_n.keys()

    for object in all_objects:
        sql = f"UPDATE {annot_table_name} SET exclude = %s, rank = %s WHERE object_label = %s"
        variables = [obj_exclude[object[0]], obj_n[object[0]], object[0]]
        mycursor.execute(sql, variables)
        time.sleep(0.2)

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
    annot_table_name = "web_annotations"
    user_table_name = "users"
    set_params()