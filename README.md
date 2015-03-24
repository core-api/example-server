# Example Core API  server

This is an example Core API service, that demonstrates implementing a simple To-Do note API.

It is written in Python, using [the Flask web framework][flask].

Note that this simplified implementation does not use a database or other storage backend, so the application state will not be persisted when restarting the service.

The source code is contained in the `server.py` module, and can be [viewed here][server-source-code].

---

## Installation

Clone the repository, then install the requirements and start the web server.

    $ pip install -r requirements.txt
    $ python ./server.py
     * Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)

---

## Usage

You'll probably want to use the [Python client library][python-client] to interact with the API.

    >>> import coreapi
    >>> doc = coreapi.get('http://127.0.0.1:3000/')
    >>> print(doc)
    <Notes 'http://127.0.0.1:3000/'>
        'notes': [],
        'add_note': link(description)

You can now explore and interact with the API.

See the [Python client library documentation][python-client] for more details.

[flask]: http://flask.pocoo.org/
[server-source-code]: https://github.com/core-api/example-server/blob/master/server.py
[python-client]: https://github.com/core-api/python-client