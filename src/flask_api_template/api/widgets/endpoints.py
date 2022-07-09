from http import HTTPStatus

from flask_restx import Namespace, Resource

from flask_api_template.api.widgets.dto import create_widget_reqparser
from flask_api_template.api.widgets.business import create_widget

widget_ns = Namespace(name='widgets', validate=True)


@widget_ns.route('', endpoint='widget_list')
@widget_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
@widget_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Unauthorized.')
@widget_ns.response(
    int(HTTPStatus.INTERNAL_SERVER_ERROR),
    'Internal server error.'
)
class WidgetList(Resource):
    @widget_ns.doc(security='Bearer')
    @widget_ns.response(int(HTTPStatus.CREATED), 'Added new widget.')
    @widget_ns.response(
        int(HTTPStatus.FORBIDDEN),
        'Administrator token required.'
    )
    @widget_ns.response(
        int(HTTPStatus.CONFLICT),
        'Widget name already exists.'
    )
    @widget_ns.expect(create_widget_reqparser)
    def post(self):
        widget_dict = create_widget_reqparser.parser_args()
        return create_widget(widget_dict)
