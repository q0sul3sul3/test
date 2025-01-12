import json
from datetime import datetime, timedelta, timezone

import jwt
from flask_login import UserMixin

from . import app, bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            'utf-8'
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def generate_reset_token(self, seconds=600):
        encoded = jwt.encode(
            {
                'email': self.email,
                'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=seconds),
            },
            app.config['SECRET_KEY'],
            algorithm='HS256',
        )
        return encoded

    def verify_reset_token(token):
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            email = decoded['email']
        except:
            return None
        return User.query.filter_by(email=email).first()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    slug = db.Column(db.String(20), unique=True, nullable=False)
    items = db.relationship('Item', backref='category', lazy='dynamic')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False, unique=True)


class JSONEncodedDict(db.TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage:

        JSONEncodedDict(255)

    """

    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        else:
            value = '{}'
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        else:
            value = {}
        return value


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(10), nullable=False, default='Paid')
    shipping = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    detail = db.Column(JSONEncodedDict)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(5), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
