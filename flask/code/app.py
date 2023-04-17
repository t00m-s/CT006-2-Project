from flask import Flask
from sqlalchemy import *
from urllib.parse import quote_plus
import os

url='ciao'
def get_db_engine():
    user=os.getenv('POSTGRES_USER')
    password=(os.getenv('POSTGRES_PASSWORD'))
    url=f'postgresql://{user}:{password}@db/{user}'
    return create_engine(url)


app = Flask(__name__)

@app.route("/")
def hello_world():
    engine=get_db_engine()
    try:
        is_connesso = 'SONO CONNESSO AL DATABASE'
        engine.connect()
    except Exception as e:
        is_connesso = 'non riesco a connettermi al db :( <br> Errore:'+str(e)+url

    return "Hello, World! Docker funziona!<br>"+ is_connesso

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
