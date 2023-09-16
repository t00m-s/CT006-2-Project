from flask import *
from flask_login import LoginManager, current_user, login_required, logout_user
from sqlalchemy.exc import SQLAlchemyError

from ..database.session import get_session
from ..database.maps.user import *
from ..database.maps.project import *

# region per importare file molto distanti dal package corrent
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "src"))
from front_home import *

# endregion

home_blueprint = Blueprint("home", __name__)
login_manager = LoginManager()


@home_blueprint.route("/")
@login_required
def index():
    """
    Returns the route for the current user.
    """
    if current_user.is_authenticated:
        return render_home(current_user)
    else:
        return redirect(url_for("login_register.login"))


@home_blueprint.route("/logout")
def logout():
    """
    Returns the route for logout
    """
    logout_user()
    return redirect(url_for("login_register.login"))


@home_blueprint.route("/account", methods=["GET"])
@login_required
def account():
    """
    Returns the route for project
    """
    return render_account(current_user)
