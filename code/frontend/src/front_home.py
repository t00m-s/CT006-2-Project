from flask import Blueprint 
from utility import render_with_lib

home_blueprint = Blueprint('home', __name__, template_folder="../templates")


def home(user):
    '''
    Renders the home page
    '''
    return render_with_lib('dashboard.html', user=user)

def project(user):
    '''
    Renders the project page
    '''
    return render_with_lib('project.html', user=user)
