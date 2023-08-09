from flask import Blueprint
from html import unescape
from utility import render_with_lib

def render_chat():
    custom_js = ['https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js', '/frontend/static/js/chat.js']
    return render_with_lib("chat.html", custom_javascript=custom_js)