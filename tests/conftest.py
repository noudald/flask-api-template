import pytest

from flask_api_template import create_app
from flask_api_template import db as database
from flask_api_template.models.user import User

EMAIL = 'test@users.com'
PASSWORD = 'password1234'


@pytest.fixture
def app():
    app = create_app('testing')
    return app


@pytest.fixture
def db(app, client, request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)
    return database


@pytest.fixture
def user(db):
    user = User(email=EMAIL, password=PASSWORD)
    db.session.add(user)
    db.session.commit()
    return user
