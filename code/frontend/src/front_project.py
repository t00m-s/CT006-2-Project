from flask import Blueprint
from utility import render_with_lib

project_blueprint = Blueprint(
    'project', __name__, template_folder="../templates")



def render_project(user, values):
    '''
    Renders the project page
    '''
    # approved 1, submitted 2, changes 3, not approved 4
    return render_with_lib('projects.html', user=user, values=values)


<<<<<<< HEAD
def render_viewproject(user, project, files):
=======
def render_viewproject(user, project):
>>>>>>> f55a346d982bea39e6c18673ecd72dfb7de6a6d8
    '''
    Renders the viewproject page
    '''
    if project.description is None:
        project.description = ''

    files = [1, 2, 3]
    return render_with_lib('viewproject.html', user=user, project=project, files=files, custom_javascript='/frontend/static/js/project.js')



def render_addproject(user):
    '''
    Renders the addproject pages
    '''
<<<<<<< HEAD
    return render_with_lib('addproject.html', user=user)
=======
    custom_javascript = ['https://unpkg.com/dropzone@5/dist/min/dropzone.min.js', '/frontend/static/js/upload.js']
    custom_css = ['https://unpkg.com/dropzone@5/dist/min/dropzone.min.css', '/frontend/static/css/upload.css']
    return render_with_lib('addproject.html', user=user, custom_javascript=custom_javascript,
                           custom_css=custom_css)
>>>>>>> f55a346d982bea39e6c18673ecd72dfb7de6a6d8
