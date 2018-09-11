from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F9F160E1668D818F544E1043657541C7B568FC3003A42B2BD9C8AD69F356A5DB'
database_name = "site_database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+database_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'primary'

from ems import routes
