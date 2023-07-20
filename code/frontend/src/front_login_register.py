from flask import Blueprint, render_template
import os
from utility import render_with_lib

login_register_blueprint = Blueprint('login_register', __name__, template_folder="../templates")


def render_login():
    '''
    Renders the login page
    '''
    return render_with_lib("login.html")


def render_register():
    '''
    Renders the registration page
    '''
    return render_with_lib("register.html", custom_javascript='/frontend/static/js/register.js',
                           custom_css='/frontend/static/css/register.css')
