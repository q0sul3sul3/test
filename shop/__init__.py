import os

import stripe
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS'
)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')
app.config['ENDPOINT_SECRET'] = os.environ.get('ENDPOINT_SECRET')
app.config['AWS_BUCKET_NAME'] = os.environ.get('AWS_BUCKET_NAME')
app.config['AWS_REGION_NAME'] = os.environ.get('AWS_REGION_NAME')
app.config['AWS_ACCESS_KEY_ID'] = os.environ.get('AWS_ACCESS_KEY_ID')
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PROT'] = os.environ.get('MAIL_PROT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
stripe.api_key = app.config['STRIPE_SECRET_KEY']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
csrf = CSRFProtect(app)
mail = Mail(app)

from . import routes
