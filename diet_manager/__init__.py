from flask import Flask
from flask_login import LoginManager
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import path
from config import Config

# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.app = app
db.init_app(app)

# migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login_user_dm'

# bcrypt = Bcrypt()

app.static_path = path.join(path.abspath(__file__), 'static')

from diet_manager import views, models
