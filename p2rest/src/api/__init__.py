from flask_restplus import Api
from .health import health_api
from .schema import schema_api
from .query import query_api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, "
                       "where JWT is the token"
    }
}

api = Api(
    title='p2rest - Python Postgres Rest',
    description='p2rest lets you create a REST API for any postgres database. I provides generic endpoints in order'
                'to query or update data. This is mainly intended for use within a frontend application since'
                'here the developers know the database structure and know what to query. An end user would need'
                'to look up available schemas and tables before she or he can query the data. ',
    version='0.0.1',
    terms_url='',
    license='GPS-3.0',
    license_url='https://github.com/herrmann1981/p2rest/blob/main/LICENSE',
    contact='',
    contact_url='https://github.com/herrmann1981/p2rest',
    contact_email='',
    authorizations=authorizations
)

api.add_namespace(health_api, path='/health')
api.add_namespace(schema_api, path='/schema')
api.add_namespace(query_api, path='/query')
