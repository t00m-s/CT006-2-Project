from flask import *
from flask_login import LoginManager, current_user
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

@home_blueprint.route('/projects/<project_type>')
@login_required
def projects(project_type):
    '''
    Route that lists all the projects 
    with the given parameter

    @params project_type Type of the project
    ''' 
    type = None
    if project_type == 'all':
        pass
    elif project_type == 'approved': 
        type = 1
    elif project_type == 'submitted':
        type = 2
    elif project_type == 'changes': #TODO find a better name 
        type = 3
    elif project_type == 'rejected':
        type = 4
    else:
        pass #TODO render error page

    temp = get_session().query(Project.id, Project.id_type, Project.name).all()
    query = {'approved': [], 'submitted':[], 'changes':[], 'rejected':[]}

    for row in temp:
        if row.id_type == 1 and (type is None or type == 1):
            query['approved'].append(row)
        elif row.id_type == 2 and (type is None or type == 2):
            query['submitted'].append(row)
        elif row.id_type == 3 and (type is None or type == 3):
            query['changes'].append(row)
        elif row.id_type == 4 and (type is None or type == 4):
            query['rejected'].append(row)

    return render_project(current_user, query)

@home_blueprint.route('/viewproject/<project_id>')
@login_required
def viewproject(project_id):
    '''
    Route that shows a single project given the id in input

    @params project_id ID of the project
    '''

    if project_id is None:
        pass # TODO render custom error page

    query = get_session().query(Project)
    return render_viewproject(current_user, project_id, query)
