from flask import *
from flask_login import *

from ..database.session import get_session
from ..database.maps.user import *

# region per importare file molto distanti dal package corrent
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src'))
from front_home import *

# endregion

home_blueprint = Blueprint('home', __name__)
login_manager = LoginManager()


class LoggedUser(UserMixin):
    def __init__(self, id, user_map):
        self.id = id
        self.user_map = user_map


@login_manager.user_loader
def load_user(user_id):
    user_map = get_session().query(User).filter_by(id=user_id).first()  # TODO testare
    if user_map is not None:
        return LoggedUser(user_map.id, user_map)


@home_blueprint.route('/')
@login_required
def index():
    user = current_user
    if user is not None:
        return home(user)


@home_blueprint.route('/logout')
def logout():
    logout_user()  # chiamata a Flask-Login return redirect(url_for(’home’))
    return redirect(url_for('home.index'))


def set_user(user_id):
    user = load_user(user_id)
    login_user(user)
