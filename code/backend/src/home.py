from flask import *
from flask_login import *

from ..database.session import get_session
from ..database.maps.user import *

# region per importare file molto distanti dal package corrent
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src'))
from home import *

# endregion

home_blueprint = Blueprint('home', __name__)
login_manager = LoginManager()


class LoggedUser(UserMixin):
    def __init__(self, id, user_map):
        self.id = id
        self.user_map = user_map


@login_manager.user_loader
def load_user(user_id):
    my_user = get_session().query(User).filter_by(id=user_id).first()
    return LoggedUser(my_user.email, my_user)


@home_blueprint.route('/')
@login_required
def index():
    return home()
