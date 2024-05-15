from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), unique=True)
    name = db.Column(db.String(300))
    password = db.Column(db.String(150))
    files = db.relationship("Files")

    def __init__(self, email, name, password) -> None:
        self.email = email
        self.name = name
        self.password = password

class Files(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    file_data = db.Column(db.LargeBinary)

    def __init__(self, data) -> None:
        self.file_data = data
