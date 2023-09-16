from front_login_register import *
from flask import Blueprint, request, redirect, url_for, flash, abort
from flask_login import *
import hashlib
import re
from ..database.session import get_session
from ..database.maps.user import User
from datetime import date

# region per importare file molto distanti dal package corrent
import sys
import os

from ...app import app

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "src"))

# endregion


login_register_blueprint = Blueprint("login_register", __name__)


@login_register_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_login()
    user = get_session().query(User).filter(User.email == request.form["email"]).first()
    get_session().commit()
    if user is None:
        flash("User not found.")
        return redirect(url_for("login_register.login"))
    if user.ban:
        flash("You have been banned.")
        return redirect(url_for("login_register.login"))
    hash_object = hashlib.sha512(request.form["password"].encode("utf-8"))
    password = hash_object.hexdigest()
    if password == user.password:
        login_user(user)
        # return "Ti ho loggato stronzo ma il redirect non va"
        return redirect(url_for("home.index"))  # RIGA ERRORE
    else:
        flash("Wrong password.")
        return redirect(url_for("login_register.login"))


@login_register_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_register()

    backurl = "login_register.register"
    check_register_parameters(request, backurl)
    user = None
    try:
        user = get_session().query(User).filter_by(email=request.form["email"]).first()
    except:
        get_session().rollback()

    if user is not None:
        flash("User already registered.")
        return redirect(url_for("login_register.login"))

        # dovrebbe essere tutto okay, non abbiamo trovato nessun utente con questa mail
        # creiamo quello nuovo
    try:
        new_user = User(
            name=request.form["name"],
            surname=request.form["surname"],
            email=request.form["email"],
            password=request.form["password"],
            birth_date=request.form["birth_date"]
            if request.form["birth_date"] is not None
               and request.form["birth_date"] != ""
            else None,
            id_role=3,
            ban=False,
        )  # set default id to researcher
        get_session().add(new_user)
        get_session().commit()

        flash("Account creato, effettua il login")
        return redirect(url_for("login_register.login"))
    except:
        get_session().rollback()
        flash("Errore durante la registrazione")
        return redirect(url_for(backurl))


def check_register_parameters(my_request, backurl):
    if my_request.method != "POST":
        abort(500)  # TODO gestire l'errore
    if my_request.form["name"] is None:
        flash("Did you forget your name?")
        return redirect(url_for(backurl))
    if my_request.form["surname"] is None:
        flash("Did you forget your surname?")
        return redirect(url_for(backurl))
    if my_request.form["email"] is None:
        flash("You forgot the email.")
        return redirect(url_for(backurl))
    check_email(my_request, backurl)
    if request.form["password"] is None:
        flash("You forgot the password")
        return redirect(url_for(backurl))
    check_password(my_request, backurl)

    # html salva l'input date secondo il formato year-month-day
    # separo l'input e salvo in una list di dimensione 3
    if (
            hasattr(my_request.form, "birth_date")
            and my_request.form["birth_date"] is not None
            and my_request.form["birth_date"] != ""
    ):
        dateTokens = my_request.form["birth_date"].split("-")
        # creo l'oggetto date di python
        pythonDate = date(int(dateTokens[0]), int(dateTokens[1]), int(dateTokens[2]))
        if date.today() < pythonDate:
            flash("Are you a time traveller? Your birth date is later than today")
            return redirect(url_for(backurl))


def check_email(my_request, backurl):
    if not re.match(
            "[^@]+@[^@]+\.[^@]+", my_request.form["email"]
    ):
        flash("Email malformed.")
        return redirect(url_for(backurl))
    return None


def check_password(my_request, backurl):
    if (
            "password" not in my_request.form
            or my_request.form["password"] is None
            or my_request.form["password"] == ""
    ):
        flash("Password can not be empty.")
        return redirect(url_for(backurl))
    if (
            "password_2" not in my_request.form
            or my_request.form["password_2"] is None
            or my_request.form["password_2"] == ""
    ):
        flash("Confirmation password can not be empty.")
        return redirect(url_for(backurl))
    if my_request.form["password"] != my_request.form["password_2"]:
        flash("Your passwords do not match.")
        return redirect(url_for(backurl))


@login_register_blueprint.route("/account", methods=["POST"])
def edit_account():
    backurl = "home.account"
    test = check_register_parameters(request, backurl)
    if test is not None:
        return test
    if "password" in request.form:
        test = check_password(request, backurl)
        if test is not None:
            return test
    if "email" in request.form:
        test = check_email(request, backurl)
        if test is not None:
            return test

    for key, val in request.form.items():
        setattr(current_user, key, val)

    get_session().commit()
    flash(
        "Account correctly updated", "info"
    )  # TODO CAMBIARE IL COLORE (ORA IL BANNER VIENE FUORI ROSSO, DOVREBBE ESSERE VERDE9
    return redirect(url_for(backurl))
