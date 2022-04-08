from flask import Flask, render_template, request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap5
from waitress import serve
import mysql.connector
import os, json

app = Flask(__name__)
Bootstrap5(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

def condCreateDir(dir):
    """
    Create a directory if it does not exist yet.
    """
    # splitdirs = dir.split('/')
    for i, _ in enumerate(dir.split('/')):
        if not os.path.exists('/'.join(dir.split('/')[:i+1])):
            os.mkdir('/'.join(dir.split('/')[:i+1]))


def annotationForms():
    high_level = {"con_move": "can be moved in a constrained manner",
                  "uncon_move": "can be moved in an unconstrained manner",
                  "dir_affs": "object can be interacted with directly",
                  "indir_affs": "object can interact with  other objects",
                  "observe_affs": "object are made for looking at",
                  "no_affs": "object does not readily offer interaction"}

    con_move = {"roll": ["can be rolled", "eg. ball"],
                "push": ["should be pushed", 'eg. pram'],
                "drag": ["should be dragged", "eg. rubbish bin"]
                }

    uncon_move = {"carry": ["can be carried", "small objects eg. pen, book"],
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
                 "hit": ["can be used to hit something", "eg. hammer"]
                 }

    observe_affs = {"info": ["displays information", "eg. screens, information poster"],
                    "deco": ["serves as decoration", "eg. painting"]
                    }

    no_affs = {"none": ["affords no interaction", "eg. wall, floor"],
               "warmth": ["gives off warmth", "eg. fireplace, heater"],
               "illumination": ["illuminates surroundings", "eg. lamp"],
               "walk": ["can be walked on", "eg. floor"]
               }

    no_clue_aff = {"no_clue": "Misspelled word/meaning of the word unclear"}

    return [high_level, no_clue_aff, con_move, uncon_move, dir_affs, indir_affs, observe_affs, no_affs]


def saveAnnotation(form):
    mydb = connect(secrets)
    mycursor = mydb.cursor()

    sql = 'SELECT anno_1_name FROM web_annotations WHERE ID = %S'
    variables = (form.get('currentObject'))
    mycursor.execute(sql, variables)
    name = next(mycursor)
    if name == "":
        annotNumber = 1
    else:
        sql = 'SELECT anno_2_name FROM web_annotations WHERE ID = %S'
        variables = (form.get('currentObject'))
        mycursor.execute(sql, variables)
        name = next(mycursor)
    if name == "":
        annotNumber = 2
    else:
        sql = 'SELECT anno_3_name FROM web_annotations WHERE ID = %S'
        variables = (form.get('currentObject'))
        mycursor.execute(sql, variables)
        name = next(mycursor)
    if name == "":
        annotNumber = 3
    else:
        return
    sql = 'INSERT INTO web_annotations ' \
          '(anno_{annotNumber}_rollable, ' \
          'anno_{annotNumber}_fragile,' \
          'anno_{annotNumber}_stackable,' \
          'anno_{annotNumber}_grasp,' \
          'anno_{annotNumber}_cut_scoop,' \
          'anno_{annotNumber}_support,' \
          'anno_{annotNumber}_wrap_grasp,' \
          'anno_{annotNumber}_pushable,' \
          'anno_{annotNumber}_draggable,' \
          'anno_{annotNumber}_carryable,' \
          'anno_{annotNumber}_openable,' \
          'anno_{annotNumber}_pourable,' \
          'anno_{annotNumber}_observe,' \
          'anno_{annotNumber}_hit,' \
          'anno_{annotNumber}_no_interaction,' \
          'anno_{annotNumber}_pull,' \
          'anno_{annotNumber}_tip_push,' \
          'anno_{annotNumber}_warmth,' \
          'anno_{annotNumber}_illumination,' \
          'anno_{annotNumber}_walk,' \
          'anno_{annotNumber}_movable,' \
          'anno_{annotNumber}_no_clue,' \
          'anno_{annotNumber}_id) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    variables = (form.get('aff_roll'),
                 form.get('aff_fragile'),
                 form.get('aff_stack'),
                 form.get('aff_grasp'),
                 form.get('aff_cut_scoop'),
                 form.get('aff_support'),
                 form.get('aff_wrap'),
                 form.get('aff_push'),
                 form.get('aff_drag'),
                 form.get('aff_carry'),
                 form.get('aff_open'),
                 form.get('aff_pour'),
                 form.get('aff_observe'),
                 form.get('aff_hit'),
                 form.get('aff_none'),
                 form.get('aff_pull'),
                 form.get('aff_tip'),
                 form.get('aff_warmth'),
                 form.get('aff_illumination'),
                 form.get('aff_walk'),
                 form.get('aff_move'),
                 form.get('aff_no_clue'))
    mycursor.execute(sql, variables)
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
    sql = 'SELECT ID FROM users WHERE NAME = %s'
    variables = (name,)
    mycursor.execute(sql, variables)
    id = next(mycursor)[0]

    sql = 'SELECT object_label ' \
          'FROM web_annotations ' \
          'WHERE anno_3_id IS NULL ' \
          'AND NOT anno_1_id <=> %s ' \
          'AND NOT anno_2_id <=> %s ' \
          'LIMIT 1'
    variables = (id, id)
    mycursor.execute(sql, variables)
    label = next(mycursor)
    mydb.close()
    return label

@app.route('/', methods=['GET', 'POST'])
def main():

    forms = annotationForms()
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
    testlist = ['chair','ceiling','wall']
    with open('secrets.json') as file:
        secrets = json.load(file)

    serve(app, listen="*:8080")