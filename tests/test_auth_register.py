from http import HTTPStatus

from flask import url_for

from flask_api_template.models.user import User


def register_user(test_client, email, password):
    return test_client.post(
        url_for('api.auth_register'),
        data=f'email={email}&password={password}',
        content_type='application/x-www-form-urlencoded'
    )


def test_auth_register(client, db):
    response = register_user(client, 'user@test.com', '1234')
    assert response.status_code == HTTPStatus.CREATED
    assert 'status' in response.json and response.json['status'] == 'success'
    assert 'message' in response.json and response.json['message'] == 'successfully registered'
    assert 'token_type' in response.json and response.json['token_type'] == 'bearer'
    assert 'expires_in' in response.json and response.json['expires_in'] == 5
    assert 'access_token' in response.json and 0 < len(response.json['access_token'])

    access_token = response.json['access_token']
    result = User.decode_access_token(access_token)
    assert result.success

    user_dict = result.value
    assert not user_dict['admin']

    user = User.find_by_public_id(user_dict['public_id'])
    assert user and user.email == 'user@test.com'
