from flask import *
from .backend.database.engine import *
from .backend.database.migration import *
from .frontend.src.index import *
import sys

app = Flask(__name__)
app.register_blueprint(index_blueprint, url_prefix='/')

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


def get_static_resource(path, resource):
    if path[0] == '/':
        path = path[1::]
    if os.path.exists(path + '/' + resource):
        return open('./' + path + '/' + resource).read()
    else:
        return 'error'


@app.route(boostrap_scirpt_path + '/<resource>')
def boostrap_script(resource):
    return get_static_resource(boostrap_scirpt_path, resource)


@app.route(jquery_scirpt_path + '/<resource>')
def jquery_script(resource):
    return get_static_resource(jquery_scirpt_path, resource)
