from flask import *
from flask_login import LoginManager, current_user
from sqlalchemy.exc import SQLAlchemyError

from ..database.session import get_session
from ..database.maps.user import *
from ..database.maps.project import *
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


@home_blueprint.route('/projects')
@home_blueprint.route('/projects/<project_type>')
@login_required
def projects(project_type=None):
    """
    Route that lists all the projects
    with the given parameter

    @params project_type Type of the project
    """

    values = {}
    if project_type is not None and not project_type.isdigit():
        return 'Error value not integer'  # TODO error page

    types = get_session().query(Type)
    projects = get_session().query(Project).filter(Project.id_user == current_user.id)
    if project_type is not None:
        types = types.filter(Type.id == project_type)
        projects = projects.filter(Project.id_user == current_user.id).filter(Project.id_type == project_type)

    types = types.all()
    projects = projects.all()
    if len(types) == 0:
        return 'Error, type not found'  # TODO 404 page

    for type in types:
        values[type.id] = {
            'name': type.name,
            'projects': []
        }

    for project in projects:
        values[project.id_type]['projects'].append(project)

    return render_project(current_user, values)


@home_blueprint.route('/viewproject/<project_id>')
@login_required
def viewproject(project_id):
    '''
    Route that shows a single project given the id in input

    @params project_id ID of the project
    '''

    if project_id is None:
        pass  # TODO render custom error page

    query = get_session().query(Project).filter_by(id=project_id).first()
    return render_viewproject(current_user, query)

@home_blueprint.route('/addproject', methods=['GET', 'POST'])
@login_required
def addproject():
    '''
    Returns the route for addproject page
    '''
    if request.method == 'GET':
        return render_addproject(current_user)
    else:
        return redirect(url_for('home.index'))
@home_blueprint.route('/account', methods=['GET'])
@login_required
def account():
    '''
    Returns the route for project
    '''
    return render_account(current_user)
