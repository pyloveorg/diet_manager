from flask import Flask
from flask_login import LoginManager
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.app = app
db.init_app(app)

# migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login_user_dm'

app.static_path = path.join(path.split(path.dirname(path.abspath(__file__)))[0], 'static')
app.static_folder = app.static_path

from diet_manager import views, models
