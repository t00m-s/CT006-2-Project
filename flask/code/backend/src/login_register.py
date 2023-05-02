from flask import Flask, Blueprint, request, redirect, url_for, flash
from flask_login import *
from flask_security import hash_password
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
        # TODO fare sha256 di request.form['user_email'] e confrontare il risultato con user.passwrd,  di fatto salveremo nel db lo sha256 della password
        if user.password == hash_password(request.form['password']):
            return redirect(url_for('home.home'))
        else:
            flash("Wrong password.")
            return redirect(url_for('index.index'))
    else:
        return redirect(url_for('index.index'))


@login_register_blueprint.route('/register', methods=['POST'])
def register_back():
    if request.form['email'] is None:
        flash("You forgot the email") # TODO ma se invece mettiamo il campo html required?
        return redirect(url_for('index.index'))
    if request.form['password'] is None:
        flash("You forgot the password") # TODO ma se invece mettiamo il campo html required?
        return redirect(url_for('index.index'))
    if request.form['name'] is None:
        flash("Did you forget your name?") # TODO ma se invece mettiamo il campo html required?
        return redirect(url_for('index.index'))
    if request.form['surname'] is None:
       flash("Did you forget your surname?") # TODO ma se invece mettiamo il campo html required?
       return redirect(url_for('index.index'))

    # TODO fare tutti i controlli password di almeno 8 caratteri maiuscole minuscole ecc
    # TODO fare tutti i controlli email valida

    user = get_session().query(User).filter_by(email=request.form['email']).first()
    if user.password is not None:
        flash("User already registered.")
        return redirect(url_for('index.index'))
    
    # dovrebbe essere tutto okay, non abbiamo trovato nessun utente con questa mail
    # creiamo quello nuovo

    # sha_password = request.form['password']  # TODO fare lo sha256 della pass

    new_user = User(name=request.form['name'],
                    surname=request.form['surname'],
                    email=request.form['email'],
                    password=hash_password(request.form['password']),
                    birth_date=request.form['birth_date'] if request.form['birth_date'] is not None else None)
