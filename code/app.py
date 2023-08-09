from flask import *
from .backend.database.engine import *
from .backend.database.migration import *
# tra tutti i file che hanno rotte deve essere il primo in quando definisce flask_login
from .backend.src.home import *
from .backend.src.login_register import *
from .frontend.src.index import *
from .frontend.src.front_chat import *
from .backend.src.project import *

import sys
import os

app = Flask(__name__)

app.register_blueprint(index_blueprint, url_prefix='/')
app.register_blueprint(login_register_blueprint, url_prefix='/')
app.register_blueprint(home_blueprint, url_prefix='/')
app.register_blueprint(project_blueprint, url_prefix='/')
app.register_blueprint(chat_blueprint, url_prefix='/')

# Secret Key for session management and flash messages
app.secret_key = os.getenv("SECRET_KEY")
migrate()  # we want to generate the db table on app load

login_manager.init_app(app)
login_manager.login_view = 'login_register.login'

UPLOAD_FOLDER = os.path.join(app.root_path, 'db_files')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 5 Mb as maximum file size
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000


@app.route(
    '/favicon.ico')  # TODO METTERE INSIEME AGLI ALTRI ASSETS (css, js, image...) USANDO LA FUNZIONE get_static_resource NEL FILE CHE LA CONTIENE
def favicon():
    '''
    Returns the favicon
    '''
    return send_from_directory(os.path.join(app.root_path, 'frontend', 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# region socket for chat

# region workaround for library compatibility
import werkzeug
import werkzeug.serving
import werkzeug._reloader

werkzeug.serving.run_with_reloader = werkzeug._reloader.run_with_reloader
# endregion


from flask_socketio import SocketIO, send

app.config['SECRET'] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
if __name__ == '__main__':
    socketio.run(app)


@socketio.on('message')
def handle_message(data):
    # TODO chiamare una funzione per salvare i dati a db
    send(data, broadcast=True)

# endregion
