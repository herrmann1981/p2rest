import datetime
from flask import current_app
from flask_restplus import Namespace, Resource, fields
from p2rest.src.database.helper import PostgresHelper

# Blueprint Configuration
health_api = Namespace(name='health',
                       description='Entpoints for retrieving status information about the service')

health_result_model = health_api.model('health_result', {
    'status_code': fields.Integer(),
    'message': fields.String(),
    'description': fields.String(),
    'duration': fields.String(),
    'data': fields.Nested(health_api.model('health_result_data', {
        'status': fields.String(),
        'db_connection': fields.String(),
    })),
})


@health_api.route('/')
@health_api.response(500, 'Internal server error.')
class HealthApi(Resource):
    """
    This is the resource that is responsible for returning a helth inforation about the server
    """

    @health_api.doc('Shows the basic service status')
    @health_api.marshal_with(health_result_model)
    def get(self):
        starttime = datetime.datetime.now()
        response = {
            'status_code': 200,
            'message': 'Service api',
            'description': 'Contains information about the basic status of this service',
            'data': {
                'status': 'Up',
                'db_connection': 'Ok'
            }
        }

        try:
            db_connection = PostgresHelper.CheckConnection(
                host=current_app.config['P2REST_DB_HOST'],
                port=current_app.config['P2REST_DB_PORT'],
                dbname=current_app.config['P2REST_DB_NAME'],
                user=current_app.config['P2REST_DB_USER'],
                password=current_app.config['P2REST_DB_PASSWORD']
            )
        except Exception as error:
            response['status_code'] = 500
            response['message'] = 'Status error'
            response['description'] = 'We could not evaluate the service status. Error: {}'.format(str(error.args))
            response['data']['status'] = 'Error'
            response['data']['db_connection'] = 'NOK'
            response['duration'] = str(datetime.datetime.now() - starttime)
            return response, response['status_code']

        response['data']['db_status'] = 'OK' if db_connection else 'NOK'
        response['duration'] = str(datetime.datetime.now() - starttime)
        return response
