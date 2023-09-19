from locale import str

from flask import jsonify

from utility import render_with_lib


def render_chat(messages):
    json = {}
    for msg in messages:
        json[msg.id] = {
            'user_name': msg.sender.name,
            'message': msg.message,
            'user_id': msg.id_user,
            'timestamp': msg.created_at
        }
    return jsonify(json)
