from flask import Flask, render_template, Blueprint
from flask_socketio import SocketIO, send
from flask_login import LoginManager, current_user, login_required
from code import app

from code.frontend.src.front_chat import render_chat

app.config['SECRET'] = "secret!123"
socketio = SocketIO(app, cors_allowed_origins="*")
chat_blueprint = Blueprint('chat', __name__)

@socketio.on('message')
def handle_message(message):
    print("received message " + message)
    if message != "User connected!":
        send(message, broacast=True)

@chat_blueprint.route('/chat')
@login_required
def chat():
    return render_chat()


socketio.run(app, host="localhost")