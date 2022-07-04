import time
from http import HTTPStatus

from flask import url_for

from tests.util import (
    register_user,
    login_user,
    get_user
)


def test_auth_user(client, db):
    register_user(client)
    response = login_user(client)

    assert 'access_token' in response.json

    access_token = response.json['access_token']
    response = get_user(client, access_token)

    assert response.status_code == HTTPStatus.OK
    assert (
        'email' in response.json
            and response.json['email'] == 'new_user@email.com'
    )
    assert 'admin' in response.json and not response.json['admin']
