from functools import wraps

from flask import request

from werkzeug.exceptions import Unauthorized

from flask_api_template.api.exceptions import ApiUnauthorized, ApiForbidden
from flask_api_template.models.user import User


def _check_access_token(admin_only):
    token = request.headers.get('Authorization')
    if not token:
        raise ApiUnauthorized(
            description='Unauthorized',
            admin_only=admin_only
        )

    result = User.decode_access_token(token)
    if result.failure:
        raise Unauthorized()
        # TODO: ApiUnauthorized doesn't seem to work well. Fix this.
        # raise ApiUnauthorized(
        #     description=result.error,
        #     admin_only=admin_only,
        #     error='invalid_token',
        #     error_description=result.error
        # )

    return result.value


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token(admin_only=False)
        for name, val in token_payload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = _check_access_token(admin_only=True)
        if not token_payload['admin']:
            raise ApiForbidden()
        for name, val in token_payload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated
