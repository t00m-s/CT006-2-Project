from flask import Blueprint, abort, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required
from front_admin import *
from ..database.session import get_session
from ..database.maps.user import User
from ..database.maps.role import Role

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
    users = get_session().query(User)

    columns = ['ID', 'Nome', 'Cognome', 'Email', 'Data Di Nascita', 'Ruolo', 'Ban']

    users = users.join(Role).filter(User.id != current_user.id, User.id_role != 1).all()
    available_roles = (
        get_session().query(Role).filter(Role.id != current_user.id_role).all()
    )
    return render_admin(current_user, users, columns, available_roles)


@admin_blueprint.route("/editrole", methods=["POST"])
@login_required
def editrole():
    if not current_user.isAdmin():
        flash("Non sei autorizzato")
        return redirect(url_for("admin_blueprint.admin"))
    if (
            "selected_role" not in request.form
            or request.form["selected_role"] is None
            or request.form["selected_role"] == ""
    ):
        flash("Error while changing role")
        return redirect(url_for("admin_blueprint.admin"))
    if (
            "user_id" not in request.form
            or request.form["user_id"] is None
            or request.form["user_id"] == ""
    ):
        flash("Utente non selezionato")
        return redirect(url_for("admin_blueprint.admin"))

    role = get_session().query(Role).filter(Role.id == request.form["selected_role"]).first()
    if role is None:
        flash("Nuovo ruolo non trovato")
        return redirect(url_for("admin_blueprint.admin"))

    user = get_session().query(User).filter(User.id == request.form["user_id"]).first()
    if user is None:
        flash("Utente non trovato")
        return redirect(url_for("admin_blueprint.admin"))

    setattr(user, "id_role", role.id)
    get_session().commit()
    flash("Succesfully updated role")
    return redirect(url_for("admin.admin"))


@admin_blueprint.route("/banuser", methods=["POST"])
@login_required
def banuser():
    if (
            "user_id" not in request.form
            or request.form["user_id"] is None
            or request.form["user_id"] == ""
    ):
        flash("Error while trying to ban user.")
        return redirect(url_for("admin_blueprint.admin"))

    user = get_session().query(User).filter(User.id == request.form["user_id"]).first()

    if not user.is_active:
        flash("You can't ban again this user")
        return redirect(url_for("admin_blueprint.admin"))
    setattr(user, is_active, False)
    get_session().commit()

    flash("User succesfully banned.")
    return redirect(url_for("admin_blueprint.admin"))
