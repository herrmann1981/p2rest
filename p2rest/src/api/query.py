import datetime
import logging

from flask import request, current_app
from flask_restplus import Namespace, Resource, fields
from werkzeug import exceptions

from p2rest.src.database.postgres import Postgres

# Blueprint Configuration
query_api = Namespace(name='query',
                      description='Endpoints for querying data from the database. It is important to know the schema '
                                  'and table or view data shall be returned.')

# Model definition
schema_result_model = query_api.model('schema_result', {
    'status_code': fields.Integer(title='status_code',
                                  description='This is the http status code that can also be found in the response'),
    'message': fields.String(title='message',
                             description='A short message describing the content of the result'),
    'description': fields.String(title='description',
                                 description='A more detailed explanation of what is in this response'),
    'count': fields.Integer(title='count',
                            description='If data is returned this field contains the amount of records'),
    'duration': fields.String(title='duration',
                              description='The time it took the server to process the request'),
    'data': fields.Raw(title='data',
                       description='This array contains data if any is returned from the database. ')
})


def create_schema_select_model():
    model = {
        'schema': fields.String(title='Postgres Schema',
                                description='Specifies the schema where the relation can be found. This is required '
                                            'because otherwise we can not find the correct relation',
                                required=True,
                                example='postgres',
                                default='postgres'),
        'relation': fields.String(title='Table or View',
                                  description='This is the relation (table or view) we want to get data from',
                                  required=True,
                                  example='table_name'),
        'fields': fields.List(fields.String,
                              title='Table or view fields',
                              description='List of fields that shall be returned from the database.',
                              required=False,
                              example=['*'],
                              default=['*']),
        'filter': fields.Nested(create_filter_model(),
                                title='Filter query',
                                description='This is the filter string. If it is empty all rows up to the limit (or '
                                            'server side maximum element number) is returned. Otherwise '
                                            'specify a filter as shown in the documentation',
                                required=False,
                                default=''),
        'order_fields': fields.List(fields.String,
                                    title='Fields to order result',
                                    description='List of fields that shall be used for ordering the result set.',
                                    required=False,
                                    example=['field1'],
                                    default=[]),
        'order_type': fields.String(title='Order type',
                                    description='Specifies hwo the result shall be ordered if order fields were '
                                                'specified. If so the value can be either "asc" or "desc"',
                                    required=False,
                                    example='asc',
                                    default=''),
        'limit': fields.Integer(title='Limit',
                                description='The maximum amount of values that shall be returned from the database. '
                                            'This value will be overwritten by the server settings if it is higher'
                                            'than the maximum that is allowed by the server.',
                                required=False,
                                example=1000),
        'offset': fields.Integer(title='Offset',
                                 description='The offset from where results shall be returned. Can be used for '
                                             'pagination',
                                 required=False,
                                 example=0,
                                 default=0)
    }
    schema_select_model = query_api.model('schema_select', model)
    return schema_select_model


def create_filter_model(iteration=5):
    data_model = {
        'column': fields.String(),
        'value': fields.String(),
        'operator': fields.String()
    }
    if iteration > 0:
        data_model['childs'] = fields.List(fields.Nested(create_filter_model(iteration-1)))
    return query_api.model('Data' + str(iteration), data_model)


@query_api.route('/select')
@query_api.response(exceptions.BadRequest.code, "BadRequest")
@query_api.response(exceptions.InternalServerError.code, "InternalServerError")
@query_api.response(exceptions.Unauthorized.code, "Unauthorized")
@query_api.response(exceptions.Forbidden.code, "Forbidden")
@query_api.response(exceptions.MethodNotAllowed.code, "MethodNotAllowed")
class SelectListApi(Resource):
    """
    This is the resource that is responsible for returning information about schemata within the database
    """

    @query_api.marshal_with(schema_result_model)
    @query_api.expect(create_schema_select_model())
    def post(self):
        """
        This endpoint returns data from a table of view. You can specify a filter expression, the columns that shall
        be returned and the sorting information for this request.
        :return: Row data for the given request
        """
        start_time = datetime.datetime.now()
        args = request.json
        response = {
            'status_code': 200,
            'message': 'Get data',
            'description': 'Get data from from table or view',
            'count': 0,
            'data': []
        }

        if not args:
            exception = exceptions.BadRequest('No arguments provided for querying the database')
            exception.duration = str(datetime.datetime.now() - start_time)
            raise exception
        if 'fields' not in args.keys():
            args['fields'] = '*'
        if 'filter' not in args.keys():
            args['filter'] = ''
        if 'limit' not in args.keys():
            args['limit'] = 100
        if 'offset' not in args.keys():
            args['offset'] = 0
        if args['limit'] > current_app.config['P2REST_MAX_RESULTS']:
            args['limit'] = current_app.config['P2REST_MAX_RESULTS']
        if 'order_type' in args.keys():
            if args['order_type'].lower() not in ['asc', 'desc']:
                exception = exceptions.BadRequest('Invalid order_type provided. Must be asc or desc.')
                exception.duration = str(datetime.datetime.now() - start_time)
                raise exception
        else:
            args['order_type'] = 'asc'
        if 'order_fields' not in args.keys():
            args['order_fields'] = ''

        try:
            response['data'] = Postgres\
                .query_select(host=current_app.config['P2REST_DB_HOST'],
                              port=current_app.config['P2REST_DB_PORT'],
                              dbname=current_app.config['P2REST_DB_NAME'],
                              user=current_app.config['P2REST_DB_USER'],
                              password=current_app.config['P2REST_DB_PASSWORD'],
                              schema=args['schema'],
                              relation=args['relation'],
                              filter=args['filter'],
                              fields=args['fields'],
                              order_fields=args['order_fields'],
                              order_type=args['order_type'],
                              limit=args['limit'],
                              offset=args['offset'])
        except exceptions.BadRequest as error:
            logging.warning('Bad request for POST /query/select: %s', str(error.args))
        except Exception as error:
            logging.warning('Internal Server Error during POST /query/select: %s', str(error.args))
            exception = exceptions.InternalServerError('Could not query data. Error: {}'.format(str(error.args)))
            exception.duration = str(datetime.datetime.now() - start_time)
            raise exception

        response['count'] = len(response['data'])
        response['duration'] = str(datetime.datetime.now() - start_time)
        return response
