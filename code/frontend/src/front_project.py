from flask import Blueprint
from html import unescape
from utility import render_with_lib

project_blueprint = Blueprint(
    'project', __name__, template_folder="../templates")


def render_project(user, values):
    '''
    Renders the project page

    @params user Current user logged in
    @params values Project types
    '''
    # approved 1, submitted 2, changes 3, not approved 4
    return render_with_lib('projects.html', user=user, values=values)


def render_viewproject(user, project, files):
    '''
    Renders the viewproject page

    @params user Current user logged in
    @params project project ID of the current project 
    @params files Files of the current project
    '''
    css = ['/frontend/static/css/chat.css']
    project.description = unescape(project.description)
    return render_with_lib('viewproject.html', user=user, project=project, files=files,
                           custom_javascript='/frontend/static/js/project.js', custom_css=css)


def render_addproject(user, types):
    '''
    Renders the addproject pages

    @params user Current user logged in
    @params types Types of possible project
    '''
    custom_javascript = ['https://unpkg.com/dropzone@5/dist/min/dropzone.min.js',
                         'https://cdn.tiny.cloud/1/cp187ge3odryin5mbbhjjq6vwjr3snwgc8zgakf0oql3z1yl/tinymce/6/tinymce.min.js',
                         'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
                         '/frontend/static/js/upload.js']
    custom_css = ['https://unpkg.com/dropzone@5/dist/min/dropzone.min.css',
                  'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
                  '/frontend/static/css/upload.css']

    return render_with_lib('addproject.html', user=user, types=types,
                           custom_javascript=custom_javascript,
                           custom_css=custom_css)
