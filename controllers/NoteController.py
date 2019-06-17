from flask import Blueprint
from flask import request, session
import json
from ..models import Notes
from .. import utils

note_api = Blueprint('note_api', __name__)

@note_api.route('/note/all')
def list_all_note(name=None):
    note_results = Notes.query.all()
    notes = []
    for row in note_results:
        notes.append(utils.row2dict(row))
    print(json.dumps(notes))
    return json.dumps(notes)
