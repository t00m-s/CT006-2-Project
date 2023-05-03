from flask import Blueprint, render_template
import os

login_register_blueprint = Blueprint('login_register', __name__, template_folder="../templates")

@login_register_blueprint.route("/register")
