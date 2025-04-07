# Sanic session management
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


`sanic_sessions` is session management extension for [Sanic](https://sanic.dev) that integrates server-backed sessions with most convenient API.

`sanic_sessions` provides a number of *session interfaces* for you to store a client's session data. The interfaces available right now are:

  * Redis (supports both drivers `aioredis` and `asyncio_redis`)
  * Memcache (via `aiomcache`)
  * Mongodb (via `sanic_motor` and `pymongo`)
  * In-Memory (suitable for testing and development environments)

## Installation

Install with `pip` (there is other options for different drivers, check documentation):

`pip install sanic_sessions`


## Example

A simple example uses the in-memory session interface.

```python
from sanic import Sanic
from sanic.response import text
from sanic_sessions import Session, InMemorySessionInterface

app = Sanic(name="ExampleApp")
session = Session(app, interface=InMemorySessionInterface())

@app.route("/")
async def index(request):
    # interact with the session like a normal dict
    if not request.ctx.session.get('foo'):
        request.ctx.session['foo'] = 0

    request.ctx.session['foo'] += 1

    return text(str(request.ctx.session["foo"]))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)