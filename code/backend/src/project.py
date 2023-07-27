from flask import Blueprint, request
from flask_login import LoginManager, current_user, login_required

from ..database.session import get_session
from ..database.maps.user import User
from ..database.maps.project import Project
from ..database.maps.type import Type

import sys
import os

# Region per importare file distanti
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src'))
# endregion
project_blueprint = Blueprint('project', __name__)
login_manager = LoginManager()

from front_project import *


# I wanted to import it from home but flask does not run
@login_manager.user_loader
def user_loader(user_id):
    '''
    Loads user from database with given ID

    @param user_id The user's ID
    @returs User associated with the ID
    '''
    return get_session().query(User).filter_by(id=user_id).first()


@project_blueprint.route('/projects')
@project_blueprint.route('/projects/<project_type>')
@login_required
def projects(project_type=None):
    """
    Route that lists all the projects
    with the given parameter

    @params project_type Type of the project
    """

    values = {}
    if project_type is not None and not project_type.isdigit():
        return 'Error value not integer'

    types = get_session().query(Type)
    projects = get_session().query(Project).filter(Project.id_user == current_user.id)
    if project_type is not None:
        types = types.filter(Type.id == project_type)
        projects = projects.filter(Project.id_user == current_user.id).filter(Project.id_type == project_type)

    types = types.all()
    projects = projects.all()
    if len(projects) == 0:
        return render_project(current_user, [])

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


@project_blueprint.route('/viewproject/<project_id>')
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


@project_blueprint.route('/addproject', methods=['GET', 'POST'])
@login_required
def addproject():
    '''
    Returns the route for addproject page
    '''
    if request.method == 'GET':
        return render_addproject(current_user)
    else:
        return str(request.form) + str(request.files)
