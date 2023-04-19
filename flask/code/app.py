from flask import Flask
from backend.database.engine import *
import sys
app = Flask(__name__)



@app.route("/")
def hello_world():
    connection=get_engine()
    try:
        is_connesso = 'SONO CONNESSO AL DATABASE<br>Il mio interprete python è: '+sys.executable
        connection.connect()
    except Exception as e:
        is_connesso = 'non riesco a connettermi al db :( <br> Errore:'+str(e)

    return "Hello, World! Docker funziona!<br>"+ is_connesso
