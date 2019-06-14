from flask import Flask
from flask import render_template
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from . import db_configs
from . import mysql_connection
import json
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from . import utils

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + db_configs.user + ':' + db_configs.password + '@' + db_configs.host + ":" + db_configs.port + '/' + db_configs.db_name
db = SQLAlchemy(app)

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(Integer, primary_key=True)
    content = db.Column(String(255), unique=True)
    title = db.Column(String(255), unique=True)
    created_at = db.Column(DateTime())
    updated_at = db.Column(DateTime())

    def __init__(self):
        self.title = ""
        self.content = ""

    def __repr__(self):
        return '<Note %r>' % (self.title)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    note_results = Notes.query.all()
    notes = []
    for row in note_results:
        notes.append(utils.row2dict(row))
    print(json.dumps(notes))
    return json.dumps(notes)

