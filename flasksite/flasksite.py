from flask import Flask, render_template, request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange
import os
from flask_bootstrap import Bootstrap
import pandas
import datetime
from waitress import serve

import mysql.connector
import os, json

app = Flask(__name__)
Bootstrap(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

backupcounter = 0

def condCreateDir(dir):
    """
    Create a directory if it does not exist yet.
    """
    # splitdirs = dir.split('/')
    for i, _ in enumerate(dir.split('/')):
        if not os.path.exists('/'.join(dir.split('/')[:i+1])):
            os.mkdir('/'.join(dir.split('/')[:i+1]))


class annotatorNameForm(FlaskForm):
    annotatorNamefield = StringField("Username:",  validators=[DataRequired()])
    submitName = SubmitField('Save and continue')


class annotationForm(FlaskForm):
    annotatorName = StringField("Username:", validators=[DataRequired()])
    aff_roll = BooleanField('should be rolled')
    aff_fragile = BooleanField('should be handled with care')
    aff_stack = BooleanField('can be stacked (onto)')
    aff_grasp = BooleanField('can be grasped')
    aff_cut_scoop = BooleanField('can serve to cut or scoop')
    aff_support = BooleanField('can support other objects')
    aff_wrap = BooleanField('can be wrapped in a hand')
    aff_push = BooleanField('should be pushed')
    aff_drag = BooleanField('should be dragged')
    aff_carry = BooleanField('can be carried')
    aff_open = BooleanField('can be opened')
    aff_pour = BooleanField('can serve to pour something out of')
    aff_observe = BooleanField('can be observed')
    aff_hit = BooleanField('can be used to hit something')
    aff_none = BooleanField('affords no interaction')
    aff_pull = BooleanField('has parts that can be pulled')
    aff_tip = BooleanField('has buttons that can be pressed')
    aff_warmth = BooleanField('gives off warmth')
    aff_illumination = BooleanField('illuminates surroundings')
    aff_walk = BooleanField('can be walked on')
    aff_move = BooleanField('can be moved')
    aff_no_clue = BooleanField('Misspelled word/don\'t know')

    currentObject = StringField()
    submit = SubmitField('Submit')


def saveAnnotation(form):
    mydb = connect(secrets)
    mycursor = mydb.cursor()

    sql = 'SELECT anno_1_name FROM web_annotations WHERE ID = %S'
    variables = (form.currentObject)
    mycursor.execute(sql, variables)
    name = next(mycursor)
    if name == "":
        annotNumber = 1
    else:
        sql = 'SELECT anno_2_name FROM web_annotations WHERE ID = %S'
        variables = (form.currentObject)
        mycursor.execute(sql, variables)
        name = next(mycursor)
    if name == "":
        annotNumber = 2
    else:
        sql = 'SELECT anno_3_name FROM web_annotations WHERE ID = %S'
        variables = (form.currentObject)
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
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)'

    variables = (form.aff_roll.data,
                 form.aff_fragile.data,
                 form.aff_stack.data,
                 form.aff_grasp.data,
                 form.aff_cut_scoop.data,
                 form.aff_support.data,
                 form.aff_wrap.data,
                 form.aff_push.data,
                 form.aff_drag.data,
                 form.aff_carry.data,
                 form.aff_open.data,
                 form.aff_pour.data,
                 form.aff_observe.data,
                 form.aff_hit.data,
                 form.aff_none.data,
                 form.aff_pull.data,
                 form.aff_tip.data,
                 form.aff_warmth.data,
                 form.aff_illumination.data,
                 form.aff_walk.data,
                 form.aff_move.data,
                 form.aff_no_clue.data)
    mycursor.execute(sql, variables)
    mydb.close()


def getNewPosts(name):
    mydb = connect(secrets)
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(name) FROM users WHERE name = %s"
    variables = (name,)
    mycursor.execute(sql, variables)
    if next(mycursor)[0] == 0:
        sql = "INSERT INTO users(name) VALUES (%s)"
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
    nameForm = annotatorNameForm()
    form = annotationForm()
    name = request.cookies.get("annotatorName")

    if form.validate_on_submit():
        saveAnnotation(form)
        # name = form.annotatorName.data
        currentObject = getNewPosts(name)
    elif name:
        currentObject = getNewPosts(name)
    elif nameForm.validate_on_submit():
        name = nameForm.annotatorNamefield.data
        currentObject = getNewPosts(name)
    else:
        return render_template("annotatorInfo.html", form=annotatorNameForm())
    resp = make_response(render_template("annotatorInfo.html", form=annotationForm(), currentObject=currentObject, name=name))
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