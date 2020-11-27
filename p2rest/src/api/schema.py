import datetime
from flask import request, current_app
from flask_restplus import Namespace, Resource, fields
from p2rest.src.database.postgres import Postgres

# Blueprint Configuration
schema_api = Namespace(name='schema',
                       description='Entpoints for retrieving schema information')

schema_result_model = schema_api.model('schema_result', {
    'status_code': fields.Integer(),
    'message': fields.String(),
    'description': fields.String(),
    'count': fields.Integer(),
    'duration': fields.String(),
    'data': fields.Raw()
})

schema_request_model = schema_api.model('schema_select', {
    'schema': fields.String(title='Postgres Schema',
                            description='Specifies the schema where the relation can be found. This is required '
                                        'because otherwise we can not find the correct relation',
                            required=True,
                            example='postgres',
                            default='postgres')
})


@schema_api.route('/')
@schema_api.response(400, 'Bad request.')
@schema_api.response(500, 'Internal server error.')
class SchemaListApi(Resource):
    """
    This is the resource that is responsible for returning information about schemata within the database
    """

    @schema_api.doc('Get all schemata in the database')
    @schema_api.marshal_with(schema_result_model)
    def get(self):
        """
        Returns the api information for this service
        :return:
        """
        starttime = datetime.datetime.now()
        response = {
            'status_code': 200,
            'message': 'DB schema',
            'description': 'Lists all available schemata in the database',
            'count': 0,
            'data': {}
        }

        try:
            response['data'] = Postgres.get_schemata(
                host=current_app.config['P2REST_DB_HOST'],
                port=current_app.config['P2REST_DB_PORT'],
                dbname=current_app.config['P2REST_DB_NAME'],
                user=current_app.config['P2REST_DB_USER'],
                password=current_app.config['P2REST_DB_PASSWORD'],
                limit=current_app.config['P2REST_MAX_RESULTS'],
            )
            response['count'] = len(response['data'])
        except Exception as error:
            response['status_code'] = 500
            response['message'] = 'Error connecting to the database'
            response['description'] = 'We could not connect to the database. Perhaps the connection is wrong or the' \
                                      'database is not reachable at the moment. Error {}'.format(str(error.args))
            response['duration'] = str(datetime.datetime.now() - starttime)
            return response, response['status_code']

        response['duration'] = str(datetime.datetime.now() - starttime)
        return response

    @schema_api.doc('Create a new schema in the database')
    @schema_api.marshal_with(schema_result_model)
    @schema_api.expect(schema_request_model)
    def post(self):
        """
        Creates a new schema in the database
        :return:
        """
        # handle arguments
        starttime = datetime.datetime.now()
        args = request.json

        response = {
            'status_code': 200,
            'message': 'Schema created',
            'description': 'The schema was successfully created in the database',
            'count': 0,
            'data': []
        }

        if not args['name'] or args['name'] == '':
            response['status_code'] = 400
            response['message'] = 'Missing schema name'
            response['description'] = 'You need to provide a name for the schema'
            response['duration'] = str(datetime.datetime.now() - starttime)
            return response, response['status_code']

        try:
            Postgres.create_schema(host=current_app.config['P2REST_DB_HOST'],
                                   port=current_app.config['P2REST_DB_PORT'],
                                   dbname=current_app.config['P2REST_DB_NAME'],
                                   user=current_app.config['P2REST_DB_USER'],
                                   password=current_app.config['P2REST_DB_PASSWORD'],
                                   schema_name=args['schema'])
        except Exception as error:
            response['status_code'] = 500
            response['message'] = 'Could not create schema'
            response['description'] = 'There was an error while creating the new schema. Error: {}'\
                .format(str(error.args))
            response['duration'] = str(datetime.datetime.now() - starttime)
            return response, response['status_code']

        response['duration'] = str(datetime.datetime.now() - starttime)
        return response


@schema_api.route('/<schema>')
@schema_api.response(400, 'Bad request.')
@schema_api.response(500, 'Internal server error.')
class SchemaApi(Resource):
    """
    This is the resource that is responsible for returning information about schemata within the database
    """

    @schema_api.doc('Get a specific schemata from the database')
    @schema_api.marshal_with(schema_result_model)
    def get(self, schema):
        """
        Returns the information about a given schema
        :return:
        """
        starttime = datetime.datetime.now()
        response = {
            'status_code': 200,
            'message': 'DB schema',
            'description': 'Lists all available schemata in the database',
            'count': 0,
            'data': {}
        }

        try:
            response['data'] = Postgres.get_schema(
                host=current_app.config['P2REST_DB_HOST'],
                port=current_app.config['P2REST_DB_PORT'],
                dbname=current_app.config['P2REST_DB_NAME'],
                user=current_app.config['P2REST_DB_USER'],
                password=current_app.config['P2REST_DB_PASSWORD'],
                schema_name=schema
            )
        except Exception as error:
            response['status_code'] = 500
            response['message'] = 'Error connecting to the database'
            response['description'] = 'We could not connect to the database. Perhaps the connection is wrong or the' \
                                      'database is not reachable at the moment. Error: {}'.format(str(error.args))
            response['duration'] = str(datetime.datetime.now() - starttime)
            return response, response['status_code']

        response['duration'] = str(datetime.datetime.now() - starttime)
        return response

    @schema_api.doc('Delete a schema in the databae')
    @schema_api.marshal_with(schema_result_model)
    def delete(self, schema):
        """
        Deletes a schema in the database
        :return:
        """
        starttime = datetime.datetime.now()
        response = {
            'status_code': 200,
            'message': 'Schema deleted',
            'description': 'The schema was successfully deleted in the database',
            'count': 0,
            'data': []
        }

        if not schema or schema == '':
            response['status_code'] = 400
            response['message'] = 'Missing schema name'
            response['description'] = 'You need to provide a name for the schema'
            response['duration'] = str(datetime.datetime.now() - starttime)
            return response, response['status_code']

        try:
            Postgres.create_schema(host=current_app.config['P2REST_DB_HOST'],
                                   port=current_app.config['P2REST_DB_PORT'],
                                   dbname=current_app.config['P2REST_DB_NAME'],
                                   user=current_app.config['P2REST_DB_USER'],
                                   password=current_app.config['P2REST_DB_PASSWORD'],
                                   schema_name=schema)
        except Exception as error:
            response['status_code'] = 500
            response['message'] = 'Could not delete schema'
            response['description'] = 'There was an error while deleting the schema. Error: {}'\
                .format(str(error.args))
            response['duration'] = str(datetime.datetime.now() - starttime)
            return response, response['status_code']

        response['duration'] = str(datetime.datetime.now() - starttime)
        return response
