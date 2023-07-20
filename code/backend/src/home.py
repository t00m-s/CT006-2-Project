from flask import *
from flask_login import LoginManager, current_user
from ..database.session import get_session
from ..database.maps.user import *

# region per importare file molto distanti dal package corrent
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src'))
from front_home import *

# endregion

home_blueprint = Blueprint('home', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    '''
    Loads user from database with given ID

    @param user_id The user's ID
    @returs User associated with the ID
    '''
    return get_session().query(User).filter_by(id=user_id).first()


@home_blueprint.route('/')
@login_required
def index():
    '''
    Returns the route for the current user.
    '''
    return render_home(current_user)


@home_blueprint.route('/logout')
def logout():
    '''
    Returns the route for logout
    '''
    logout_user()
    return redirect(url_for('home.index'))


@home_blueprint.route('/project')
@login_required
def projects():
    '''
    Returns the route for project
    '''
    return render_project(current_user)


@home_blueprint.route('/account')
@login_required
def account():
    '''
    Returns the route for project
    '''
    return render_account(current_user)
