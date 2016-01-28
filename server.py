from collections import OrderedDict
from coreapi import Document, Link, Error, Field, dump
from flask import Flask, Response, request
from flask_sockets import Sockets
import json
import jsonpatch
import time
import uuid


app = Flask(__name__)
sockets = Sockets(app)
clients = []


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
        notify_clients()

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
        notify_clients()
        return Response(status=204)

    elif request.method == 'PUT':
        data = request.get_json()
        note = notes[identifier]
        if 'description' in data:
            note['description'] = str(data['description'])
        if 'complete' in data:
            note['complete'] = bool(data['complete'])
        notify_clients()

    doc = get_note(identifier)
    accept = request.headers.get('Accept')
    media_type, content = dump(doc, accept=accept)
    return Response(content, mimetype=media_type)


# WebSockets

@sockets.route('/live')
def echo_socket(ws):
    message = ws.receive()
    doc = get_notes()
    media_type, content = dump(doc, accept='application/vnd.coreapi+json')
    data = json.loads(content)
    ws.send('Content-Type: application/vnd.coreapi+json\n\n' + content)
    clients.append((ws, data))
    while True:
        time.sleep(1)


def notify_clients():
    global clients

    if not clients:
        return

    doc = get_notes()

    media_type, next_content = dump(doc, accept='application/vnd.coreapi+json')
    next_data = json.loads(next_content)
    new_clients = []
    print 'Sending message to %d clients' % len(clients)
    for (client, previous_data) in list(clients):
        if next_data == previous_data:
            continue
        patch = jsonpatch.make_patch(previous_data, next_data).to_string()
        try:
            client.send(patch)
        except:
            print 'Client left'
        else:
            new_clients.append((client, next_data))
    clients = new_clients


if __name__ == '__main__':
    app.run(port=3000, debug=True)
