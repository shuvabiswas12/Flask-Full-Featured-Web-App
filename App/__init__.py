from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = "1f157c192086567f577cc2fe83a45091"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db = SQLAlchemy(app=app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app=app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from App import route
