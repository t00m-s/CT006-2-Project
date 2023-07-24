from flask import *
from .backend.database.engine import *
from .backend.database.migration import *
from .backend.src.home import *  # tra tutti i file che hanno rotte deve essere il primo in quando definisce flas_login
from .backend.src.login_register import *
from .frontend.src.index import *
from .backend.src.project import *
import sys
import os

app = Flask(__name__)

app.register_blueprint(index_blueprint, url_prefix='/')
app.register_blueprint(login_register_blueprint, url_prefix='/')
app.register_blueprint(home_blueprint, url_prefix='/')
app.register_blueprint(project_blueprint, url_prefix='/')

app.secret_key = os.getenv("SECRET_KEY")  # Secret Key for session management and flash messages
# migrate()  # we want to generate the db table on app load

login_manager.init_app(app)
login_manager.login_view = 'login_register.login'


@app.route('/favicon.ico')
def favicon():
    '''
    Returns the favicon
    '''
    return send_from_directory(os.path.join(app.root_path, 'frontend', 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
