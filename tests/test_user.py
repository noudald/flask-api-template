def test_encode_access_token(user):
    access_token = user.encode_access_token()
    assert 0 < len(access_token)
    assert isinstance(access_token, str)
