import time

from flask_api_template.models.user import User


def test_encode_access_token(user):
    access_token = user.encode_access_token()
    assert 0 < len(access_token)
    assert isinstance(access_token, str)


def test_decode_access_token_success(user):
    access_token = user.encode_access_token()
    result = User.decode_access_token(access_token)
    assert result.success

    user_dict = result.value
    assert user.public_id == user_dict['public_id']
    assert user.admin == user_dict['admin']


def test_decode_access_token_expired(user):
    access_token = user.encode_access_token()
    time.sleep(6)
    result = User.decode_access_token(access_token)
    assert not result.success
    assert result.error == 'Access token expired.'
