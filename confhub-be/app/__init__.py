import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sqlite3")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_path

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_tables():
    from app.models import User, AuthToken
    db.create_all()

from app import views
