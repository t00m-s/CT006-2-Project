from flask import *
from flask_login import *
from ..database.session import *

from ..database.maps.user import *
from ..database.maps.role import *

login_register_blueprint = Blueprint('login_register', __name__)


@login_register_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_session().query(User).filter_by(email=request.form['email']).first()
        if user is None or user.password is None:
            return redirect(url_for('index.index'))  # TODO user non trovato
        # TODO fare sha256 di request.form['user_email'] e confrontare il risultato con user.passwrd,  di fatto salveremo nel db lo sha256 della password
        if user.password == request.form['password']:
            return redirect(url_for('home.home'))
        else:
            return "WRONG PASS"  # TODO sostituire con "Errore password non valida"
    else:
        return redirect(url_for('index.index'))


@login_register_blueprint.route('/register', methods=['POST'])
def register_back():
    if request.form['email'] is None:
        return 'Errore mail'  # todo erroe email obblgiatoria tornare alla pagina di registrazione
    if request.form['password'] is None:
        return 'Errore password'  # todo erroe pass obblgiatoria tornare alla pagina di registrazione
    if request.form['name'] is None:
        return 'Errore name'  # todo erroe nome obblgiatoria tornare alla pagina di registrazione
    if request.form['surname'] is None:
        return 'Errore surname'  # todo erroe surnome obblgiatoria tornare alla pagina di registrazione

    # TODO fare tutti i controlli password di almeno 8 caratteri maiuscole minuscole ecc
    # TODO fare tutti i controlli email valida

    user = get_session().query(User).filter_by(email=request.form['email']).first()
    if user.password is not None:
        return 'Errore gia tovato'  # TODO tornare messaggio di erroe utente gia trovato, redirect a registrazioner
    # dovrebbe essere tutto okay, non abbiamo trovato nessun utente con questa mail
    # creiamo quello nuovo

    sha_password = request.form['password']  # TODO fare lo sha256 della pass

    new_user = User(name=request.form['name'],
                    surname=request.form['surname'],
                    email=request.form['email'],
                    password=sha_password,
                    birth_date=request.form['birth_date'] if request.form['birth_date'] is not None else None)
