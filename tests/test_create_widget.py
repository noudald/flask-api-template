from http import HTTPStatus

import pytest

from tests.util import ADMIN_EMAIL, login_user, create_widget


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
