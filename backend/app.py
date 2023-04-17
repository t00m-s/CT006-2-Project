from flask import Flask
import os
app = Flask(__name__)

'''
@app.route('/')
def hello_world():  # put application's code here
    user=os.getenv('POSTGRES_USER')
    return 'Hello World prova!'+ user
'''

@app.route("/")
def hello_world():
    return "Hello, World! Docker funzia!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
