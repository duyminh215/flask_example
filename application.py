from flask import Flask
from flask import request, session
from flask import render_template
import json
from .settings import DevelopmentConfig
from .settings import config
from .extensions import db
from .controllers.AccountController import account_api
from .controllers.NoteController import note_api

DEFAULT_APP_NAME = 'app'

def create_app(config=None):
    app = Flask(DEFAULT_APP_NAME)

    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app)
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

def configure_blueprints(app):
    app.register_blueprint(account_api)
    app.register_blueprint(note_api)


app = create_app(config['development'])
if __name__ == "__main__":
    app.run()