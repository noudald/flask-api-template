from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_api_template.api.auth.dto import auth_reqparser
from flask_api_template.api.auth.business import process_registation_request


auth_ns = Namespace(name='auth', validate=True)


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
