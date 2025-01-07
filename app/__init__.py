from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
login.blueprint_login_views = {
    "users": "users.login",
    "admin": "admin.admin_login",
}

from app import views, models

app.register_blueprint(views.users_blueprint)
app.register_blueprint(views.admin_blueprint)
