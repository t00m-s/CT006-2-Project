from front_project import *
from flask import Blueprint, request
from flask_login import LoginManager, current_user, login_required

from ..database.session import get_session
from ..database.maps.user import User
from ..database.maps.project import Project
from ..database.maps.type import Type
from ..database.maps.project_files import ProjectFiles
from ..database.maps.project_history import ProjectHistory
import sys
import os

from ...frontend.src.front_project import render_addproject

# Region per importare file distanti
sys.path.append(os.path.join(os.path.dirname(
    __file__), '..', '..', 'frontend', 'src'))
# endregion
project_blueprint = Blueprint('project', __name__)
login_manager = LoginManager()


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
        return 'Error, value not integer'

    types = get_session().query(Type)
    projects = get_session().query(Project).filter(
        Project.id_user == current_user.id)
    if project_type is not None:
        types = types.filter(Type.id == project_type)
        projects = projects.filter(Project.id_user == current_user.id).filter(
            Project.id_type == project_type)

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
    files = get_session().query(ProjectFiles).join(
        ProjectHistory).filter_by(id_user=current_user.id).all()
    return render_viewproject(current_user, query, files)


@project_blueprint.route('/addproject', methods=['GET', 'POST'])
@login_required
def addproject():
    '''
    Returns the route for addproject page
    '''
    if request.method == 'GET':
        return render_addproject(current_user, get_session().query(Type).all())
    elif request.method == 'POST':
        # Add new project
        new_project = Project(id_user=current_user.id,
                              id_type=request.form.type,
                              name=request.form.name,
                              description=request.form.description)
        get_session().add(new_project)

        # Add project history
        # 3 = Submitted for Evaluation
        new_project_history = ProjectHistory(
            new_project.id, 3, current_user.id)
        get_session().add(new_project_history)

        # Add project files
        dir_path = os.path.join(os.getcwd(), 'db_files', str(
            current_user.id), new_project.id, str(1))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for file in request.files.getlist('files'):
            file_path = os.path.join(dir_path, file.filename)
            file.save(file_path)
            get_session.add(ProjectFiles(file_path,
                                         new_project_history.id))

        get_session().commit()
        return redirect('/viewproject/' + new_project.id)


@ project_blueprint.route('/viewfile/<file_id>')
@ login_required
def viewfile(file_id):
    '''
    Returns a route for the viewfile page

    @params file_id ID of the file to obtain
    '''

    if file_id is None:
        pass  # TODO render custom error page
    query = get_session().query(ProjectFiles).join(
        ProjectHistory).filter_by(id_user=current_user.id, id=file_id).all()
    return query
    return str(request.form) + str(request.files)
