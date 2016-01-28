# Example Core API  server

This is an example [Core API][core-api] service, that demonstrates implementing a simple To-Do note API.

It is written in Python, using [the Flask web framework][flask].

Note that this simplified implementation does not use a database or other storage backend, so the application state will not be persisted when restarting the service.

The source code is contained in the `server.py` module, and can be [viewed here][server-source-code].

---

## Installation

Clone the repository, then install the requirements and start the web server.

    $ pip install -r requirements.txt
    $ gunicorn -k flask_sockets.worker server:app
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

---

## License

Copyright © 2015, Tom Christie.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[core-api]: https://github.com/core-api/core-api
[flask]: http://flask.pocoo.org/
[server-source-code]: https://github.com/core-api/example-server/blob/master/server.py
[python-client]: https://github.com/core-api/python-client
