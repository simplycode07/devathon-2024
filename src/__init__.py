from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db_name = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = "brrrrrrrrrrrrrr"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"

db = SQLAlchemy(app)

def start():
    global app, db

    from .views import routes, initialize_login
    from .models import User, Files

    with app.app_context():
        if not path.exists(db_name):
            db.create_all()

    initialize_login(app)

    app.register_blueprint(routes)

    return app




