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
        flash("Utente non trovato.", "error")
        return redirect(url_for("login_register.login"))
    if user.ban:
        flash("Non disponi più dei diritti per accedere al sito.", "error")
        return redirect(url_for("login_register.login"))
    hash_object = hashlib.sha512(request.form["password"].encode("utf-8"))
    password = hash_object.hexdigest()
    if password == user.password:
        login_user(user)
        flash("Login effettuato corretamente")
        return redirect(url_for("home.index"))  # RIGA ERRORE
    else:
        flash("Password errata.")
        return redirect(url_for("login_register.login"))


@login_register_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_register()

    backurl = "login_register.register"
    if "email" not in request.form:
        flash("Hai dimenticato l'email.", "error")
        return redirect(url_for(backurl))
    if "password" not in request.form:
        flash("Hai dimenticato la password.", "error")
        return redirect(url_for(backurl))
    if "password_2" not in request.form:
        flash("Hai dimenticato la conferma della password.", "error")
        return redirect(url_for(backurl))

    test = check_register_parameters(request, backurl)
    if test is not None:
        return test
    user = None
    try:
        user = get_session().query(User).filter_by(email=request.form["email"]).first()
    except:
        get_session().rollback()

    if user is not None:
        flash("Utente già registrato.", "error")
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
        flash("Richiesta non valida.", "error")
        return redirect(url_for(backurl))
    if my_request.form["name"] is None:
        flash("Hai dimenticato il nome.", "error")
        return redirect(url_for(backurl))
    if my_request.form["surname"] is None:
        flash("Hai dimenticato il cognome.", "error")
        return redirect(url_for(backurl))
    if "email" in my_request.form and (
        my_request.form["email"] is None or my_request.form["email"] == ""
    ):
        flash("Hai dimenticato l'email?", "error")
        return redirect(url_for(backurl))
    test = check_email(my_request, backurl)
    if test is not None:
        return test
    if "password" in my_request.form and (
        my_request.form["password"] is None or my_request.form["password"] == ""
    ):
        flash("Hai dimenticato la password.", "error")
        return redirect(url_for(backurl))
    check_password(my_request, backurl)

    # html salva l'input date secondo il formato year-month-day
    # separo l'input e salvo in una list di dimensione 3
    if (
        "birth_date" in my_request.form
        and my_request.form["birth_date"] is not None
        and my_request.form["birth_date"] != ""
    ):
        dateTokens = my_request.form["birth_date"].split("-")
        # creo l'oggetto date di python
        pythonDate = date(int(dateTokens[0]), int(dateTokens[1]), int(dateTokens[2]))
        if date.today() < pythonDate:
            flash("Sei un viaggiatore temporale?", "error")
            return redirect(url_for(backurl))
    return None


def check_email(my_request, backurl):
    if "email" in my_request.form and not re.match(
        "[^@]+@[^@]+\.[^@]+", my_request.form["email"]
    ):
        flash("Email non valida.", "error")
        return redirect(url_for(backurl))
    return None


def check_password(my_request, backurl):
    if "password" in my_request.form and (
        my_request.form["password"] is None or my_request.form["password"] == ""
    ):
        flash("La password non può essere vuota.", "error")
        return redirect(url_for(backurl))
    if "password_2" in my_request.form and (
        my_request.form["password_2"] is None or my_request.form["password_2"] == ""
    ):
        flash("La password di conferma non può essere vuota.", "error")
        return redirect(url_for(backurl))
    if my_request.form["password"] != my_request.form["password_2"]:
        flash("Le due password non corrispondono.", "error")
        return redirect(url_for(backurl))


@login_register_blueprint.route("/account", methods=["POST"])
def edit_account():
    backurl = "home.account"
    test = check_register_parameters(request, backurl)
    if test is not None:
        return test
    for key, val in request.form.items():
        if val == "":
            val = None
        setattr(current_user, key, val)

    get_session().commit()
    flash("Dati account aggiornati correttamente")
    return redirect(url_for(backurl))
