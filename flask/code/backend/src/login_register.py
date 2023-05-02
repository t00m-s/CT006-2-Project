from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import *
from passlib.hash import sha512_crypt
from ...frontend.src.utility import render_with_lib
from ..database.session import *
from ..database.maps.user import *
from ..database.maps.role import *
login_register_blueprint = Blueprint('login_register', __name__)


@login_register_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_session().query(User).filter_by(email=request.form['email']).first()
        if user is None or user.password is None:
            flash("User not found.")
            return redirect(url_for('index.index')) 
        if sha512_crypt.verify(request['password'], user.password): #TODO: test this
            return redirect(url_for('home.home'))
        else:
            flash("Wrong password.")
            return redirect(url_for('index.index'))
    else:
        return redirect(url_for('index.index'))

# TODO fare una cosa fatta bene...
@login_register_blueprint.route('/register', methods=['GET'])
def register_page():
    return render_with_lib("register.html")


@login_register_blueprint.route('/register', methods=['POST'])
def register_back():
    if request.method == 'POST': #TODO forse rimuovere questi controlli sotto?
        if request.form['email'] is None:
            flash("You forgot the email")
            return redirect(url_for('index.index'))
        if request.form['password'] is None:
            flash("You forgot the password")
            return redirect(url_for('index.index'))
        if request.form['name'] is None:
            flash("Did you forget your name?")
            return redirect(url_for('index.index'))
        if request.form['surname'] is None:
            flash("Did you forget your surname?")
            return redirect(url_for('index.index'))

        # TODO fare tutti i controlli password di almeno 8 caratteri maiuscole minuscole ecc
        # TODO fare tutti i controlli email valida

        user = get_session().query(User).filter_by(email=request.form['email']).first()
        if user is not None and user.password is not None:
            flash("User already registered.")
            return redirect(url_for('login_register.login'))
        
        # dovrebbe essere tutto okay, non abbiamo trovato nessun utente con questa mail
        # creiamo quello nuovo
        new_user = User(name=request.form['name'],
                        surname=request.form['surname'],
                        email=request.form['email'],
                        password=sha512_crypt.hash(request.form['password']),
                        birth_date=request.form['birth_date'] if request.form['birth_date'] is not None else None)
        get_session().commit()
        return redirect(url_for('login_register.login'))
    else:
        return redirect(url_for('login_register.register_page')) # TODO: importare bootstrap
