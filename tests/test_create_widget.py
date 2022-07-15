from datetime import date, timedelta
from http import HTTPStatus

import pytest

from tests.util import (
    ADMIN_EMAIL,
    BAD_REQUEST,
    DEFAULT_NAME,
    login_user,
    create_widget
)


@pytest.mark.parametrize(
    'widget_name',
    ['abc123', 'widget-name', 'new_widget1']
)
def test_create_widget_valid_name(client, db, admin, widget_name):
    response = login_user(client, email=ADMIN_EMAIL)
    assert 'access_token' in response.json

    access_token = response.json['access_token']
    response = create_widget(
        client,
        access_token,
        widget_name=widget_name
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'status' in response.json and response.json['status'] == 'success'

    message = f'New widget added: {widget_name}.'
    assert 'message' in response.json and response.json['message'] == message

    location = f'/api/v1/widgets/{widget_name}'
    assert ('Location' in response.headers
            and response.headers['Location'] == location)


@pytest.mark.parametrize(
    'deadline_str',
    [
        date.today().strftime('%m/%d/%Y'),
        date.today().strftime('%Y-%m-%d'),
        (date.today() + timedelta(days=3)).strftime('%b %d %Y')
    ]
)
def test_create_widget_valid_deadline(client, db, admin, deadline_str):
    response = login_user(client, email=ADMIN_EMAIL)
    assert 'access_token' in response.json

    access_token = response.json['access_token']
    response = create_widget(
        client,
        access_token,
        deadline_str=deadline_str
    )
    assert response.status_code == HTTPStatus.CREATED
    assert ('status' in response.json
            and response.json['status'] == 'success')

    message = f'New widget added: {DEFAULT_NAME}.'
    assert 'message' in response.json and response.json['message'] == message

    location = f'/api/v1/widgets/{DEFAULT_NAME}'
    assert ('Location' in response.headers
            and response.headers['Location'] == location)


@pytest.mark.parametrize(
    'deadline_str',
    [
        '1/1/1970',
        (date.today() - timedelta(days=3)).strftime('%Y-%m-%d'),
        'This is not a deadline string.'
    ]
)
def test_create_widget_invalid_deadline(client, db, admin, deadline_str):
    response = login_user(client, email=ADMIN_EMAIL)
    assert 'access_token' in response.json

    access_token = response.json['access_token']
    response = create_widget(
        client,
        access_token,
        deadline_str=deadline_str
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert ('message' in response.json
            and response.json['message'] == BAD_REQUEST)
    assert ('errors' in response.json
            and 'deadline' in response.json['errors'])
