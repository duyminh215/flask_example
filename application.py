from flask import Flask
from flask import request, session
from flask import render_template
import json
from .settings import DevelopmentConfig
from .settings import config
from .extensions import db
from .models import Notes
from . import utils

DEFAULT_APP_NAME = 'app'

def create_app(config=None):
    app = Flask(DEFAULT_APP_NAME)

    configure_app(app, config)
    configure_extensions(app)

    configure_logging(app)

    app.debug_logger.debug(' * Runing in -----* ')

    return app

def configure_app(app, config):
    if not config:
        config = DevelopmentConfig

    app.config.from_object(config)

def configure_extensions(app):

    db.init_app(app)


def configure_logging(app):

    import logging
    from logging import StreamHandler

    class DebugHandler(StreamHandler):
        def emit(x, record):
            StreamHandler.emit(x, record) if app.debug else None

    logger = logging.getLogger('app')
    logger.addHandler(DebugHandler())
    logger.setLevel(logging.DEBUG)

    app.debug_logger = logger

app = create_app(config['development'])

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    note_results = Notes.query.all()
    notes = []
    for row in note_results:
        notes.append(utils.row2dict(row))
    print(json.dumps(notes))
    return json.dumps(notes)


@app.route('/login/', methods=['POST'])
def login():
    json_data = request.json
    phone = json_data['phone']
    password = json_data['password']

    if phone == '0981713034' and password == '826dabf6e74e583ffbfccb2c7cab747d':
        session['phone'] = json_data
        return 'Bạn đã đăng nhập thành công'

    return json.dumps(json_data)

@app.route('/session/test')
def test_session():
    if 'phone' in session:
        return 'Bạn đã login rồi'
    return 'Bạn chưa login'

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('phone', None)
    return 'Bạn đã logout rồi'