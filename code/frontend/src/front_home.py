import datetime

from flask import Blueprint
from utility import render_with_lib

home_blueprint = Blueprint('home', __name__, template_folder="../templates")


def render_home(user):
    '''
    Renders the home page
    '''
    return render_with_lib('admin_dashboard.html', user=user)

def render_project(user, values):
    '''
    Renders the project page
    '''
    # approved 1, submitted 2, changes 3, not approved 4
    return render_with_lib('projects.html', user=user, values=values)

def render_viewproject(user, project):
    '''
    Renders the viewproject page
    '''
    return render_with_lib('viewproject.html', user=user, project=project)

def render_addproject(user):
    '''
    Renders the addproject page
    '''
    return render_with_lib('addproject.html', user=user)

def render_account(user):
    '''
    Renders the user account page
    '''
    dob = user.birth_date.strftime('%Y-%m-%d') if user.birth_date is not None and user.birth_date != '' else None
    return render_with_lib('account.html', user=user, dob=dob, custom_css='/frontend/static/css/account.css',
                           custom_javascript='/frontend/static/js/account.js')
