from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap5
from waitress import serve
import mysql.connector
import os, json

app = Flask(__name__)
Bootstrap5(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

all_aff_keys = []

def annotationForms():
    global all_aff_keys
    high_level = {"con_move": "object can be moved in a constrained manner",
                  "uncon_move": "object can be moved in an unconstrained manner",
                  "dir_affs": "object can be interacted with directly",
                  "indir_affs": "object can interact with  other objects",
                  "observe_affs": "object is made for looking at",
                  "social_affs": "object fullfills social role",
                  "no_affs": "object does not readily offer interaction"}

    con_move = {"roll": ["can be rolled", "eg. ball"],
                "push": ["can be pushed", 'eg. stroller'],
                "drag": ["can be dragged", "eg. rubbish bin"],
                "tether": ["is tethered", "eg. wired computer mouse"]
                }

    uncon_move = {"pick_up_carry": ["can be picked up/carried", "small objects eg. pen, book"],
                  "pour": ["can serve to pour something out of", "eg. cup, flask"]
                  }

    dir_affs = {"fragile": ["should be handled with care", "breakable items eg. glass vase"],
                "open": ["can be opened", "eg. cupboard, bottle"],
                "grasp": ["can be grasped", "small objects eg. phone or objects with handles"],
                "pull": ["can be pulled", "eg. handle, knob"],
                "tip": ["has buttons that can be pressed", "eg. light switch, buttons on device"]
                }

    indir_affs ={"stack": ["can be stacked (onto)", "eg. plates, stackable chairs"],
                 "cut_scoop": ["can serve to cut or scoop", "eg. knife, spoon, scoop"],
                 "support": ["can support other objects", "surfaces which can you can put something on, eg. desk, table"],
                 "transfer": ["transfers media to other object", "eg. pen, coffeemaker"],
                 "requires_other": ["requires other objects to be used", "eg. whiteboard (marker), paper (pen)"]
                 }

    observe_affs = {"info": ["displays information", "eg. screens, information poster"],
                    "deco": ["serves as decoration", "eg. painting"]
                    }

    social_affs = {"together": ["is made to be used with more than one person", "eg. foosball table, board game, pingpong table"]
                    }

    no_affs = {"none": ["affords no interaction", "eg. wall, floor"],
               "warmth": ["regulates temperature", "eg. fireplace, heater, air conditioning"],
               "illumination": ["illuminates surroundings", "eg. lamp"],
               "walk": ["can be walked on", "eg. floor"]
               }

    no_clue_aff = {"no_clue": "Misspelled word/meaning of the word unclear"}

    all_affs = [high_level, no_clue_aff, con_move, uncon_move, dir_affs, indir_affs, observe_affs, social_affs, no_affs]

    for aff_set in all_affs:
        all_aff_keys.extend(list(aff_set.keys()))

    return all_affs


def saveAnnotation(form):
    mydb = connect(secrets)
    mycursor = mydb.cursor()

    sql = 'SELECT ID FROM users WHERE name = %s LIMIT 1'
    variables = (form.get('annotatorName'),)
    mycursor.execute(sql, variables)
    id = next(mycursor)[0]


    sql = 'SELECT anno_1_id, anno_2_id, anno_3_id FROM web_annotations WHERE object_label = %s LIMIT 1'
    currentObject = form.get('currentObject')
    variables = (currentObject,)
    mycursor.execute(sql, variables)
    result = next(mycursor)

    if result[0] is None:
        annotNumber = 1
    elif result[1] is None:
        annotNumber = 2
    elif result[2] is None:
        annotNumber = 3
    else:
        return  # a race condition occurred and the current annotation is discarded
    sql = f'UPDATE web_annotations SET '
    for key in all_aff_keys:
        sql += f'anno_{annotNumber}_{key} = %s, '
    sql += f'anno_{annotNumber}_id = %s WHERE object_label = %s'


    variables = [(1 if form.get(f'{key}') is not None else 0) for key in all_aff_keys]
    variables.extend([id, currentObject])

    mycursor.execute(sql, variables)
    mydb.commit()
    mydb.close()


def getNewPosts(name):
    mydb = connect(secrets)
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(name) FROM users WHERE name = %s"
    variables = (name,)
    mycursor.execute(sql, variables)
    if next(mycursor)[0] == 0:
        sql = "INSERT INTO users (name) VALUES (%s)"
        variables = (name,)
        mycursor.execute(sql, variables)
        mydb.commit()
    sql = 'SELECT ID FROM users WHERE NAME = %s LIMIT 1'
    variables = (name,)
    mycursor.execute(sql, variables)
    id = next(mycursor)[0]

    sql = 'SELECT object_label ' \
          'FROM web_annotations ' \
          'WHERE anno_3_id IS NULL ' \
          'AND NOT anno_1_id <=> %s ' \
          'AND NOT anno_2_id <=> %s ' \
          'AND exclude <=> %s ' \
          'ORDER BY `rank` DESC ' \
          'LIMIT 1'
    variables = (id, id, 0)
    mycursor.execute(sql, variables)
    label = next(mycursor)
    mydb.close()
    return label

@app.route('/', methods=['GET', 'POST'])
def main():
    name = request.cookies.get("annotatorName")

    if request.form.get('form_type') == 'aff':
        saveAnnotation(request.form)
        # name = form.annotatorName.data
        currentObject = getNewPosts(name)
    elif name:
        currentObject = getNewPosts(name)
    elif request.form.get('form_type') == 'name':
        name = request.form.get('annotatorName')
        currentObject = getNewPosts(name)
    else:
        return render_template("annotatorInfo.html", forms=forms)

    resp = make_response(render_template("annotatorInfo.html", forms=forms, currentObject=currentObject, name=name, zip=zip))
    resp.set_cookie("annotatorName", name)
    return resp

def connect(secrets):
    mydb = mysql.connector.connect(
        host="localhost",
        user=secrets["mysqluser"],
        password=secrets["mysqlpass"],
        database="affordance_annotation"
    )
    return mydb

if __name__ == "__main__":

    forms = annotationForms()
    with open(os.path.dirname(os.path.abspath(__file__))+'/secrets.json') as file:
        secrets = json.load(file)

    serve(app, listen="*:8081")