import os
from flask import Flask
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError, NotFound, NotImplemented, MethodNotAllowed, \
    Unauthorized, Forbidden
from p2rest.src.api import api
from p2rest.src.config import config_by_name


def configure_app(app, config_name):
    """
    Handle configuration for the application
    :param app:
    :param config_name: The name of the configuration to be used: 'dev', 'test', 'prod'
    :return:
    """
    app.config.from_object(config_by_name[config_name])
    # overwrite config variables if config file is provided
    if os.getenv('P2REST_CONFIG') is not None:
        app.config.from_envvar('P2REST_CONFIG')
    # overwrite config variables that are provided as environment variables
    if os.getenv('P2REST_DB_HOST') is not None:
        app.config['P2REST_DB_HOST'] = os.getenv('P2REST_DB_HOST')
    if os.getenv('P2REST_DB_PORT') is not None:
        app.config['P2REST_DB_PORT'] = os.getenv('P2REST_DB_PORT')
    if os.getenv('P2REST_DB_NAME') is not None:
        app.config['P2REST_DB_NAME'] = os.getenv('P2REST_DB_NAME')
    if os.getenv('P2REST_DB_USER') is not None:
        app.config['P2REST_DB_USER'] = os.getenv('P2REST_DB_USER')
    if os.getenv('P2REST_DB_PASSWORD') is not None:
        app.config['P2REST_DB_PASSWORD'] = os.getenv('P2REST_DB_PASSWORD')


def create_app(config_name='prod') -> Flask:
    """
    Application factory for the core application
    :return: Returns instance of our application
    """
    app = Flask('p2rest', instance_relative_config=False)
    configure_app(app, config_name)

    # Create app context
    with app.app_context():
        # Register Blueprints
        api.init_app(app)

        @api.errorhandler(HTTPException)
        @app.errorhandler(HTTPException)
        def handle_bad_request(error, *args, **kwargs):
            temp = {
                       'status_code': error.code,
                       'message': error.name,
                       'description': error.description,
                       'duration': error.duration if hasattr(error, 'duration') else 0,
                       'count': 0,
                       'data': []
                   }
            temp.update(**kwargs)
            return temp, error.code

        # @api.errorhandler(InternalServerError)
        # def internal_error_handler(error, *args, **kwargs):
        #     return {
        #                'status_code': InternalServerError.code,
        #                'message': 'Internal Server Error',
        #                'description': str(error.specific),
        #                'duration': 0,
        #                'count': 0,
        #                'data': []
        #            }, InternalServerError.code
        #
        # @api.errorhandler(NotFound)
        # def not_error_handler(error, *args, **kwargs):
        #     return {
        #                'status_code': NotFound.code,
        #                'message': 'Internal Server Error',
        #                'description': str(error.specific),
        #                'duration': 0,
        #                'count': 0,
        #                'data': []
        #            }, NotFound.code
        #
        # @api.errorhandler(NotImplemented)
        # def not_implemented_error_handler(error, *args, **kwargs):
        #     return {
        #                'status_code': NotImplemented.code,
        #                'message': 'Internal Server Error',
        #                'description': str(error.specific),
        #                'duration': 0,
        #                'count': 0,
        #                'data': []
        #            }, NotImplemented.code
        #
        # @api.errorhandler(MethodNotAllowed)
        # def method_not_allowed_error_handler(error, *args, **kwargs):
        #     return {
        #                'status_code': MethodNotAllowed.code,
        #                'message': 'Internal Server Error',
        #                'description': str(error.specific),
        #                'duration': 0,
        #                'count': 0,
        #                'data': []
        #            }, MethodNotAllowed.code
        #
        # @api.errorhandler(Unauthorized)
        # def method_not_allowed_error_handler(error, *args, **kwargs):
        #     return {
        #                'status_code': Unauthorized.code,
        #                'message': 'Internal Server Error',
        #                'description': str(error.specific),
        #                'duration': 0,
        #                'count': 0,
        #                'data': []
        #            }, Unauthorized.code
        #
        # @api.errorhandler(Forbidden)
        # def method_not_allowed_error_handler(error, *args, **kwargs):
        #     return {
        #                'status_code': Forbidden.code,
        #                'message': 'Internal Server Error',
        #                'description': str(error.specific),
        #                'duration': 0,
        #                'count': 0,
        #                'data': []
        #            }, Forbidden.code

        return app
