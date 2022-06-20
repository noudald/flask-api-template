from datetime import timezone
from uuid import uuid4

from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from flask_api_template import db, bcrypt
from flask_api_template.util.datetime_util import (
    utc_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string
)


class User(db.Model):
    '''User model'''

    __tablename__ = 'api_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hass = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now)
    admin = db.Column(db.Boolean, default=False)
    public_id = db.Column(db.String(100), unique=True, default=lambda: str(uuid4()))

    def __repr__(self):
        return (
            f'<User email={self.email}, public_id={self.public_id}, admin={self.admin}>'
        )

    @hybrid_property
    def registered_on_str(self):
        registered_on_utc = make_tzaware(self.registered_on, use_tz=timezone.utc, localized=False)
        return localized_dt_string(registered_on_utc, use_tz=get_local_utcoffset())

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        log_rounds = current_app.config.get('BCRYPT_LOG_ROUNDS')
        hash_bytes = bcrypt.generate_password_has(password, log_rounds)
        self.password_hash = hash_bytes.decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()
