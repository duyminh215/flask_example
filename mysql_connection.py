import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import db_configs
from . import application

def create_db_connection():
    try:
        myapp = Flask(__name__)
        url_connection = 'mysql://' + db_configs.user + ':' + db_configs.password + '@' + db_configs.host + ":" + db_configs.port + '/' + db_configs.db_name
        myapp.config['SQLALCHEMY_DATABASE_URI'] = url_connection
        db.init_app(myapp)
        db.create_all()
        return db
    except:
        return None