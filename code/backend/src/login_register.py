from flask import Blueprint, request, redirect, url_for, flash, render_template
from .home import set_user
import hashlib
import re
from ...frontend.src.utility import render_with_lib
from ..database.session import *
from ..database.maps.user import *
from ..database.maps.role import *
from datetime import date
from datetime import datetime
# region per importare file molto distanti dal package corrent
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src'))
from front_login_register import *

# endregion


login_register_blueprint = Blueprint('login_register', __name__)


@login_register_blueprint.route('/login', methods=['GET'])
def show_login():
    return render_login()


@login_register_blueprint.route('/register', methods=['GET'])
def show_register():
    return render_register()


@login_register_blueprint.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = get_session().query(User).filter_by(email=request.form['email']).first()
        if user is None or user.password is None:
            flash("User not found.")
            return redirect(url_for('login_register.show_login'))
        hash_object = hashlib.sha512(request.form['password'].encode('utf-8'))
        password = hash_object.hexdigest()
        if password == user.password:
            return redirect(url_for('home.index'))
        else:
            flash("Wrong password.")
            return redirect(url_for('login_register.show_login'))
    else:
        return redirect(url_for('login_register.show_login'))


@login_register_blueprint.route('/register', methods=['POST'])
def register_back():
    if request.method == 'POST':
        if request.form['email'] is None:
            flash("You forgot the email")
            return redirect(url_for('login_register.show_register'))
        if request.form['password'] is None:
            flash("You forgot the password")
            return redirect(url_for('login_register.show_register'))
        if request.form['name'] is None:
            flash("Did you forget your name?")
            return redirect(url_for('login_register.show_register'))
        if request.form['surname'] is None:
            flash("Did you forget your surname?")
            return redirect(url_for('login_register.show_register'))
        if request.form['password'] != request.form['password_2']:
            flash("Your passwords do not match.")
            return redirect(url_for('login_register.show_register'))
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$',
                        request.form['password']):
            flash("Your passwords must be at least 8 chars. <br> At least: "
                  "<ul>"
                  "<li>1 Upper case</li>"
                  "<li>1 Lower case</li>"
                  "<li>1 Number</li>"
                  "</ul> ")
            return redirect(url_for('login_register.show_register'))
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', request.form['email']):
            flash("Email malformed.")
            return redirect(url_for('login_register.show_register'))
        # TODO fare la regex anche per la data di nascita: attenzione non è un campo obbligatorio


        dateTokens = request.form['birth_date'].split('-')
        print(dateTokens)
        pythonDate = date(int(dateTokens[0]),int(dateTokens[1]),int(dateTokens[2]))
        if date.today() < pythonDate :
            flash("Are you a time traveller? Your birth date is later than today")
            return redirect(url_for('login_register.show_register'))

        user = get_session().query(User).filter_by(email=request.form['email']).first()
        if user is not None and user.password is not None:
            flash("User already registered.")
            return redirect(url_for('login_register.show_login'))

        # dovrebbe essere tutto okay, non abbiamo trovato nessun utente con questa mail
        # creiamo quello nuovo
        new_user = User(name=request.form['name'],
                        surname=request.form['surname'],
                        email=request.form['email'],
                        password=request.form['password'],
                        birth_date=request.form['birth_date'] if request.form['birth_date'] is not None and
                                                                 request.form['birth_date'] != '' else None,
                        id_role=None)
        get_session().add(new_user)
        get_session().commit()
        set_user(new_user.id)
        return redirect(url_for('home.index'))
    else:
        return redirect(url_for('login_register.show_register'))
