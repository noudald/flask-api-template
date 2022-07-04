from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_api_template.api.auth.dto import auth_reqparser, user_model
from flask_api_template.api.auth.business import (
    process_registation_request,
    get_logged_in_user,
)


auth_ns = Namespace(name='auth', validate=True)
auth_ns.models[user_model.name] = user_model


@auth_ns.route('/register', endpoint='auth_register')
class RegisterUser(Resource):
    @auth_ns.expect(auth_reqparser)
    @auth_ns.response(
        int(HTTPStatus.CREATED),
        'New user was successfully create'
    )
    @auth_ns.response(
        int(HTTPStatus.CONFLICT),
        'Email address is already registered'
    )
    @auth_ns.response(
        int(HTTPStatus.BAD_REQUEST),
        'Parse error, bad payload request'
    )
    @auth_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR),
        'Internal server error'
    )
    def post(self):
        request_data = auth_reqparser.parse_args()
        email = request_data.get('email')
        password = request_data.get('password')

        return process_registation_request(email, password)


@auth_ns.route('/user', endpoint='auth_user')
class GetUser(Resource):
    @auth_ns.doc(security='Bearer')
    @auth_ns.response(
        int(HTTPStatus.OK),
        'Token is currently valid',
        user_model
    )
    @auth_ns.response(
        int(HTTPStatus.BAD_REQUEST),
        'Validation error'
    )
    @auth_ns.response(
        int(HTTPStatus.UNAUTHORIZED),
        'Token is invalid or expired'
    )
    @auth_ns.marshal_with(user_model)
    def get(self):
        return get_logged_in_user()
