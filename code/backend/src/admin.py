from flask import Blueprint, abort
from flask_login import LoginManager, current_user, login_required
from ..database.session import get_session
from ..database.maps.user import User

# Region per importare file distanti
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "src"))
# endregion

admin_blueprint = Blueprint("admin", __name__)
login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    """
    Loads user from database with given ID

    @param user_id The user's ID
    @returs User associated with the ID
    """
    try:
        return (
            get_session().query(User).filter(User.id_role == 1).first()
        )  # TODO remove hardcoded value
    except:
        abort(500)


@admin_blueprint.route("/admin", methods=["GET"])
@login_required
def admin():
    pass
