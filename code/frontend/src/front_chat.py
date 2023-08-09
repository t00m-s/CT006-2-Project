from flask import Blueprint
from utility import render_with_lib
from flask_login import LoginManager, current_user, login_required

chat_blueprint = Blueprint('chat', __name__)


@chat_blueprint.route('/chat')
@login_required
def chat():
    return render_chat(current_user)


def render_chat(user):
    custom_js = ['https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.3/socket.io.js', '/frontend/static/js/chat.js']
    return render_with_lib("chat.html", custom_javascript=custom_js, user_name=user.name)
