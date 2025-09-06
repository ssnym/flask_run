from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv

app = Flask(__name__)

# To configure our SQL DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Used for Hashing
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# for SQL DataBase
db = SQLAlchemy(app)

# for storing hashed passwords
bcrypt = Bcrypt(app)

# for managing User's login session
login_manager = LoginManager(app)

# When user is not Loged In but is accessing the route with @login_required
login_manager.login_view = 'login_page'

login_manager.login_message_category='info'

from project import routes