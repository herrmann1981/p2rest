import psycopg2
import logging
from .helper import PostgresHelper


class Postgres(object):
    """
    Database communication
    """

    @classmethod
    def get_schemata(cls, **kwargs):
        """
        Check if we can connect to the database
        """
        logging.debug('Geting all available schemata for host: %s, port: %s', kwargs['host'], str(kwargs['port']))

        result = None
        connection = None
        cursor = None

        args = dict({'limit': 10000, 'offset': 0}, **kwargs)
        if not {'host', 'port', 'dbname', 'user', 'password'} <= args.keys():
            raise ValueError('Missing required parameter for database connection')

        try:
            connection = psycopg2.connect(host=args['host'], port=args['port'], dbname=args['dbname'],
                                          user=args['user'], password=args['password'])
            cursor = connection.cursor()
            cursor.execute('SELECT schema_name FROM information_schema.schemata LIMIT {limit} OFFSET {offset}'
                           .format(limit=args['limit'], offset=args['offset']))
            temp = cursor.fetchall()
            columns = cursor.description
            result = PostgresHelper.ConvertPsycopg2Data(temp, columns)
        except psycopg2.Error as error:
            logging.error('We could not connect to the database: %s', str(error.args))
            raise psycopg2.DatabaseError('Database connection error')
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return result

    @classmethod
    def get_schema(cls, **kwargs):
        """
        Check if we can connect to the database
        :return: boolean indicating if we can connect (true) or not (false)
        """
        result = None
        connection = None
        cursor = None

        args = dict({'limit': 10000, 'offset': 0}, **kwargs)
        if not {'host', 'port', 'dbname', 'user', 'password', 'schema_name'} <= args.keys():
            raise ValueError('Missing required parameter for database connection')

        logging.debug('Geting schemat info for %s on host: %s, port: %s', args['schema_name'], args['host'],
                      str(args['port']))

        try:
            connection = psycopg2.connect(host=args['host'], port=args['port'], dbname=args['dbname'],
                                          user=args['user'], password=args['password'])
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM information_schema.schemata WHERE schema_name=\'{schema_name}\''
                           .format(schema_name=args['schema_name']))
            temp = cursor.fetchall()
            columns = cursor.description
            result = PostgresHelper.ConvertPsycopg2Data(temp, columns)
        except psycopg2.Error as error:
            logging.error('We could not connect to the database: %s', str(error.args))
            raise error
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return result

    @classmethod
    def create_schema(cls, **kwargs):
        """
        Create a new schema in the database
        :return: boolean indicating if we can connect (true) or not (false)
        """
        result = None
        connection = None
        cursor = None

        args = dict({'limit': 10000, 'offset': 0}, **kwargs)
        if not {'host', 'port', 'dbname', 'user', 'password', 'schema_name'} <= args.keys():
            raise ValueError('Missing required parameter for database connection')

        logging.debug('Create schema %s on host: %s, port: %s', args['schema_name'], args['host'], str(args['port']))

        try:
            connection = psycopg2.connect(host=args['host'], port=args['port'], dbname=args['dbname'],
                                          user=args['user'], password=args['password'])
            cursor = connection.cursor()
            cursor.execute('CREATE SCHEMA IF NOT EXISTS {schema_name}'
                           .format(schema_name=args['schema_name']))
            connection.commit()
        except psycopg2.Error as error:
            logging.error('We could not connect to the database: %s', str(error.args))
            raise error
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def delete_schema(cls, **kwargs):
        """
        Create a new schema in the database
        :return: boolean indicating if we can connect (true) or not (false)
        """
        connection = None
        cursor = None

        args = dict(**kwargs)
        if not {'host', 'port', 'dbname', 'user', 'password', 'schema_name'} <= args.keys():
            raise ValueError('Missing required parameter for database connection')

        logging.debug('Delete schema %s on host: %s, port: %s', args['schema_name'], args['host'], str(args['port']))

        try:
            connection = psycopg2.connect(host=args['host'], port=args['port'], dbname=args['dbname'],
                                          user=args['user'], password=args['password'])
            cursor = connection.cursor()
            cursor.execute('DROP SCHEMA IF EXISTS {schema_name} CASCADE'
                           .format(schema_name=args['schema_name']))
            connection.commit()
        except psycopg2.Error as error:
            logging.error('We could not connect to the database: %s', str(error.args))
            raise error
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def query_select(cls, **kwargs):
        """
        Check if we can connect to the database
        :param host: The host ip or dns name for our connection
        :param port: Database servers port
        :param dbname: The database name we want to connect to
        :param user: The db user for connecting
        :param password: The db users password for connecting
        :return: boolean indicating if we can connect (true) or not (false)
        """
        result = None
        connection = None
        cursor = None

        args = dict({'limit': 10000, 'filter': '', 'offset': 0, 'fields': '*', 'order_fields': '', 'order_type': 'asc'},
                    **kwargs)
        if not {'host', 'port', 'dbname', 'user', 'password', 'schema', 'relation'} <= args.keys():
            raise ValueError('Missing required parameter for database connection')

        logging.debug('Geting data from %s:%s from host: %s, port: %s', args['schema'], args['relation'], args['host'],
                      str(args['port']))

        try:
            connection = psycopg2.connect(host=args['host'], port=args['port'], dbname=args['dbname'],
                                          user=args['user'], password=args['password'])
            cursor = connection.cursor()
            query = '''
                SELECT {fields} FROM {schema}.{relation} {filter} {order} LIMIT {limit} OFFSET {offset}
            '''.format(
                fields=', '.join(args['fields']),
                schema=args['schema'],
                relation=args['relation'],
                filter=PostgresHelper.convert_request_filter_to_string(args['filter']),
                order=PostgresHelper.convert_order_by_to_string(args['order_fields'], args['order_type']),
                limit=args['limit'],
                offset=args['offset']
            )
            cursor.execute(query)
            temp = cursor.fetchall()
            columns = cursor.description
            result = PostgresHelper.ConvertPsycopg2Data(temp, columns)
        except psycopg2.Error as error:
            logging.error('We could not cget data: %s', str(error.args))
            raise error
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return result