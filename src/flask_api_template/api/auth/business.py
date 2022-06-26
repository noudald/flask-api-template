from http import HTTPStatus

from flask import current_app, jsonify
from flask_restx import abort

from flask_api_template import db
from flask_api_template.models.user import User


def _get_token_expire_time():
    if current_app.config['TESTING']:
        return 5

    token_age_h = current_app.config.get('TOKEN_EXPIRE_HOURS')
    token_age_m = current_app.config.get('TOKEN_EXPIRE_MINUTES')
    expires_in_seconds = 3600 * token_age_h + 60 * token_age_m

    return expires_in_seconds


def process_registation_request(email, password):
    if User.find_by_email(email):
        return abort(
            HTTPStatus.CONFLICT,
            f'{email} is already registered',
            status='fail'
        )

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    access_token = new_user.encode_access_token()
    response = jsonify(
        status='success',
        message='successfully registered',
        access_token=access_token,
        token_type='bearer',
        expires_in=_get_token_expire_time()
    )
    response.status_code = HTTPStatus.CREATED
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'

    return response
