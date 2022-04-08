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

    sql = 'SELECT ID FROM users WHERE name = %s'
    variables = (form.get('annotatorName'),)
    mycursor.execute(sql, variables)
    id = next(mycursor)[0]


    sql = 'SELECT anno_1_id, anno_2_id, anno_3_id FROM web_annotations WHERE object_label = %s'
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

    sql = f'UPDATE web_annotations SET ' \
          f'anno_{annotNumber}_rollable = %s, ' \
          f'anno_{annotNumber}_fragile = %s, ' \
          f'anno_{annotNumber}_stackable = %s, ' \
          f'anno_{annotNumber}_grasp = %s, ' \
          f'anno_{annotNumber}_cut_scoop = %s, ' \
          f'anno_{annotNumber}_support = %s, ' \
          f'anno_{annotNumber}_pushable = %s, ' \
          f'anno_{annotNumber}_draggable = %s, ' \
          f'anno_{annotNumber}_carryable = %s, ' \
          f'anno_{annotNumber}_openable = %s, ' \
          f'anno_{annotNumber}_pourable = %s, ' \
          f'anno_{annotNumber}_observe = %s, ' \
          f'anno_{annotNumber}_hit = %s, ' \
          f'anno_{annotNumber}_no_interaction = %s, ' \
          f'anno_{annotNumber}_pull = %s, ' \
          f'anno_{annotNumber}_tip_push = %s, ' \
          f'anno_{annotNumber}_warmth = %s, ' \
          f'anno_{annotNumber}_illumination = %s, ' \
          f'anno_{annotNumber}_walk = %s, ' \
          f"anno_{annotNumber}_con_move = %s, " \
          f"anno_{annotNumber}_uncon_move = %s, " \
          f"anno_{annotNumber}_dir_affs = %s, " \
          f"anno_{annotNumber}_indir_affs = %s, " \
          f"anno_{annotNumber}_observe_affs = %s, " \
          f"anno_{annotNumber}_no_affs = %s, " \
          f'anno_{annotNumber}_no_clue = %s, ' \
          f'anno_{annotNumber}_id = %s ' \
          'WHERE object_label = %s'


    variables = ((1 if form.get('roll') is not None else 0),
                 (1 if form.get('fragile') is not None else 0),
                 (1 if form.get('stack') is not None else 0),
                 (1 if form.get('grasp') is not None else 0),
                 (1 if form.get('cut_scoop') is not None else 0),
                 (1 if form.get('support') is not None else 0),
                 (1 if form.get('push') is not None else 0),
                 (1 if form.get('drag') is not None else 0),
                 (1 if form.get('carry') is not None else 0),
                 (1 if form.get('open') is not None else 0),
                 (1 if form.get('pour') is not None else 0),
                 (1 if form.get('observe') is not None else 0),
                 (1 if form.get('hit') is not None else 0),
                 (1 if form.get('none') is not None else 0),
                 (1 if form.get('pull') is not None else 0),
                 (1 if form.get('tip') is not None else 0),
                 (1 if form.get('warmth') is not None else 0),
                 (1 if form.get('illumination') is not None else 0),
                 (1 if form.get('walk') is not None else 0),
                 (1 if form.get('con_move') is not None else 0),
                 (1 if form.get('uncon_move') is not None else 0),
                 (1 if form.get('dir_affs') is not None else 0),
                 (1 if form.get('indir_affs') is not None else 0),
                 (1 if form.get('observe_affs') is not None else 0),
                 (1 if form.get('no_affs') is not None else 0),
                 (1 if form.get('no_clue') is not None else 0),
                 id,
                 currentObject
                 )
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
    sql = 'SELECT ID FROM users WHERE NAME = %s'
    variables = (name,)
    mycursor.execute(sql, variables)
    id = next(mycursor)[0]

    sql = 'SELECT object_label ' \
          'FROM web_annotations ' \
          'WHERE anno_3_id IS NULL ' \
          'AND NOT anno_1_id <=> %s ' \
          'AND NOT anno_2_id <=> %s ' \
          'ORDER BY RAND() ' \
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