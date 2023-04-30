from flask import *
from flask_login import *
from ..database.session import *

from ..database.maps.user import *
from ..database.maps.role import *

login_register_blueprint = Blueprint('login_register', __name__)


@login_register_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = get_session().query(User).filter_by(email=request.form['user_email']).first()
        except Exception as e:
            return str(e)  # TODO sostituire con "Errore mail non trovata"
            # return redirect(url_for('/'))
        if not user.has_key('password') or user.password is None:
            return "Nooooone"
            return redirect(url_for('home'))

        # TODO fare sha256 di request.form['user_email'] e confrontare il risultato con user.passwrd,  di fatto salveremo nel db lo sha256 della password
        if user.passwrod == request.form['user_email']:
            return redirect(url_for('home'))
        else:
            return "WRONG PASS"  # TODO sostituire con "Errore password non valida"
    else:
        return redirect(url_for('/'))
