from flask import *
from .backend.database.engine import *
from .backend.database.migration import *
from .backend.src.login_register import *
from .frontend.src.index import *
from .frontend.src.home import *
import sys
import os

app = Flask(__name__)
app.register_blueprint(index_blueprint, url_prefix='/')
app.register_blueprint(login_register_blueprint, url_prefix='/')
app.register_blueprint(home_blueprint, url_prefix='/')

app.secret_key = os.getenv("SECRET_KEY") # Secret Key for session management and flash message and flash messages
migrate()  # we want to generate the db table on app load


@app.route("/test")
def test():
    connection = get_engine()
    try:
        is_connesso = 'SONO CONNESSO AL DATABASE<br>Il mio interprete python è: ' + sys.executable
        connection.connect()
    except Exception as e:
        is_connesso = 'non riesco a connettermi al db :( <br> Errore:' + str(e)

    return "Hello, World! Docker funziona!<br>" + is_connesso
