from werkzeug.exceptions import Unauthorized, Forbidden

_REALM_REGULAR_USER = 'registered_users@mydomain.com'
_REALM_ADMIN_USER = 'admin_users@mydomain.com'


class ApiUnauthorized(Unauthorized):
    def __init__(
        self,
        description='Unauthorized',
        admin_only=False,
        error=None,
        error_description=None
    ):
        self.description = description
        self.www_auth_value = self.__get_www_auth_value(
            admin_only, error, error_description
        )
        Unauthorized.__init__(
            self,
            description=description,
            response=None,
            www_authenticate=None
        )

    def get_headers(self, environ):
        return [
            ('Content-Type', 'text/html'),
            ('WWW-Authenticate', self.www_auth_value)
        ]

    def __get_www_auth_value(self, admin_only, error, error_description):
        realm = _REALM_ADMIN_USER if admin_only else _REALM_REGULAR_USER
        www_auth_value = f'Bearer realm="{realm}"'
        if error:
            www_auth_value += f', error="{error}"'
        if error_description:
            www_auth_value += f', error_description="{error_description}"'

        return www_auth_value


class ApiForbidden(Forbidden):
    description = 'You are not an administrator'

    def get_headers(self, environ):
        return [
            ('Content-Type', 'text/html'),
            (
                'WWW-Authenticate',
                f'Bearer realm="{_REALM_ADMIN_USER}", '
                'error="insufficient_scope", '
                'error_description="You are not an administrator"'
            )
        ]
