from flask import Flask
from backend.models import *
from backend.api import api

app = None  # initial value

def init_app():
    my_app = Flask(__name__)    # object of Flask
    my_app.debug = True
    my_app.app_context().push() # direct access app by other modules (database, authentication)
    my_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_app_database.sqlite3"
    database.init_app(my_app)   # object.method(<parameter>)
    api.init_app(my_app)
    print("Application started...")
    return my_app

app = init_app()
from backend.controllers import *

if __name__ == "__main__":
    app.run()


# code ends

