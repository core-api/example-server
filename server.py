from collections import OrderedDict
from coreapi import Document, Link, Error, Field, dump
from flask import Flask, Response, request
import uuid


app = Flask(__name__)

# We store all the notes in a mapping of UUIDs to dictionary instances.
# In a real system we would be using a database or other persistent backend.
notes = OrderedDict()


def get_notes():
    """
    Return the top level Document object, containing all the note instances.
    """
    return Document(
        url='/',
        title='Notes',
        content={
            'notes': [
                get_note(identifier)
                for identifier in reversed(notes.keys())
            ],
            'add_note': Link(action='post', fields=[Field(name='description', required=True)])
        }
    )


def get_note(identifier):
    """
    Return a Document object for a single note instance.
    """
    note = notes[identifier]
    return Document(
        url='/' + identifier,
        title='Note',
        content={
            'description': note['description'],
            'complete': note['complete'],
            'edit': Link(action='put', fields=[Field(name='description'), Field(name='complete')]),
            'delete': Link(action='delete')
        }
    )


@app.route('/', methods=['GET', 'POST'])
def note_list():
    """
    API endpoint to list the notes, or create a new note.
    """
    global notes

    if request.method == 'POST':
        identifier = str(uuid.uuid4())
        data = request.get_json()
        notes[identifier] = {
            'description': str(data['description']),
            'complete': False
        }

    doc = get_notes()
    accept = request.headers.get('Accept')
    media_type, content = dump(doc, accept=accept)
    return Response(content, mimetype=media_type)


@app.route('/<identifier>', methods=['GET', 'PUT', 'DELETE'])
def note_detail(identifier):
    """
    API endpoint to retrieve, update or delete a note.
    """
    global notes

    if identifier not in notes:
        error = Error(
            title='Not found',
            content={'messages': ['This note no longer exists.']}
        )
        accept = request.headers.get('Accept')
        media_type, content = dump(error, accept=accept)
        return Response(content, status=404, mimetype=media_type)

    if request.method == 'DELETE':
        del notes[identifier]
        return Response(status=204)

    elif request.method == 'PUT':
        data = request.get_json()
        note = notes[identifier]
        if 'description' in data:
            note['description'] = str(data['description'])
        if 'complete' in data:
            note['complete'] = bool(data['complete'])

    doc = get_note(identifier)
    accept = request.headers.get('Accept')
    media_type, content = dump(doc, accept=accept)
    return Response(content, mimetype=media_type)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
