from flask import Blueprint, render_template
import os
from utility import *

login_register_blueprint = Blueprint('login_register', __name__, template_folder="../templates")


def render_login():
    return render_with_lib("login.html")


def render_register():
    return render_with_lib("register.html")
