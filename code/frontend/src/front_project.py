from flask import Blueprint
from utility import render_with_lib

project_blueprint = Blueprint('project', __name__, template_folder="../templates")


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

    return render_with_lib('addproject.html', user=user, custom_javascript='/frontend/static/js/upload.js',
                           custom_css='/frontend/static/css/upload.css')
