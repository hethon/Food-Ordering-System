from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
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
