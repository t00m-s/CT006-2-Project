import datetime

from flask import Blueprint
from utility import render_with_lib
<<<<<<< HEAD
=======

# from ...backend.database.session import get_session  TODO: fix
>>>>>>> 2229714d32a1d5acee6b8b765542c39772294d51
home_blueprint = Blueprint('home', __name__, template_folder="../templates")


def render_home(user):
    '''
    Renders the home page
    '''
    return render_with_lib('admin_dashboard.html', user=user)

<<<<<<< HEAD
def render_project(user, query):
=======

def render_project(user):
>>>>>>> 2229714d32a1d5acee6b8b765542c39772294d51
    '''
    Renders the project page
    '''
    # approved 1, submitted 2, changes 3, not approved 4
    return render_with_lib('project.html', user=user, query=query)

<<<<<<< HEAD
def render_viewproject(user, id_project):
    '''
    Renders the viewproject page
    '''
    return render_with_lib('viewproject.html', user=user)
=======

def render_account(user):
    '''
    Renders the user account page
    '''
    dob = user.birth_date.strftime('%Y-%m-%d') if user.birth_date is not None and user.birth_date != '' else None
    return render_with_lib('account.html', user=user, dob=dob, custom_css='/frontend/static/css/account.css',
                           custom_javascript='/frontend/static/js/account.js')
>>>>>>> 2229714d32a1d5acee6b8b765542c39772294d51
