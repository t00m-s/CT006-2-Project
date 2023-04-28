from flask import *
from .backend.database.engine import *
from .backend.database.migration import *
from .frontend.src.index import *
import sys

app = Flask(__name__)
app.register_blueprint(index_blueprint)

migrate()


# Test route for DB migrations
@app.route("/")
def main():
    connection = get_engine()


@app.route("/test")
def test():
    connection = get_engine()
    try:
        is_connesso = 'SONO CONNESSO AL DATABASE<br>Il mio interprete python è: ' + sys.executable
        connection.connect()
    except Exception as e:
        is_connesso = 'non riesco a connettermi al db :( <br> Errore:' + str(e)

    return "Hello, World! Docker funziona!<br>" + is_connesso
