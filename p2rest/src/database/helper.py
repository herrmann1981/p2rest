import psycopg2
import logging
import datetime
from werkzeug.exceptions import BadRequest


class PostgresHelper(object):
    """
    Helper class for postgres
    """

    @classmethod
    def CheckConnection(cls, host, port, dbname, user, password) -> bool:
        """
        Check if we can connect to the database
        :param host: The host ip or dns name for our connection
        :param port: Database servers port
        :param dbname: The database name we want to connect to
        :param user: The db user for connecting
        :param password: The db users password for connecting
        :return: boolean indicating if we can connect (true) or not (false)
        """
        connection_available = True
        logging.debug('Check database connection for host: %s, port: %s', host, str(port))

        try:
            connection = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
            if connection:
                connection.close()
            else:
                raise psycopg2.DatabaseError('Could not connect to the database')
        except psycopg2.Error as error:
            logging.error('We could not connect to the database: %s', str(error.args))
            connection_available = False

        logging.debug('Database status is: %s', str(connection_available))
        return connection_available

    @classmethod
    def ConvertPsycopg2Data(cls, data, columns):
        """
        Converts a psycopgs list of tuples into a dictionary representation
        :param data: The result data from the cursor fetch operation
        :param columns: Column description
        :return: List of dictionary entries
        """
        result = []
        for row in data:
            entry = {}
            for i in range(0, len(columns)):
                if isinstance(row[i], datetime.datetime):
                    entry[columns[i].name] = row[i].strftime('%Y-%m-%dT%H:%M:%S.%f')
                elif isinstance(row[i], datetime.timedelta):
                    entry[columns[i].name] = str(row[i])
                else:
                    entry[columns[i].name] = row[i]
            result.append(entry)
        return result

    @classmethod
    def convert_request_filter_to_string(cls, json_filter):
        """
        This method takes a json object representing a filter and constructs a postgres filter
        expression for it
        :param json_filter: json object representing the filter
        :return: postgres filter string
        """
        result = ''
        if not json_filter or len(json_filter) == 0:
            return result

        try:
            filter = json_filter
            result = PostgresHelper._convert_request_filter_node(filter)

            if result and len(result) > 0:
                return 'WHERE ' + result
            else:
                return ''
        except Exception as error:
            logging.error('Failed to parse json filter into postgres filter: %s', str(error.args))
            raise error

    @classmethod
    def _convert_request_filter_node(cls, node):
        """
        Converts one json node into a filter expression part
        :param node:
        :return:
        """
        if 'column' in node.keys():
            # leaf node
            if 'operator' not in node.keys():
                raise BadRequest('No operand specified for column {}'.format(node['column']))
            if 'value' not in node.keys():
                raise BadRequest('No value specified for column {}'.format(node['column']))
            if node['operator'] not in ('=', '<', '>', '<=', '>=', '!=', '<>', 'like', 'ilike'):
                raise BadRequest('Operator "{}" is not supported for columnd {}'.format(node['operator'],
                                                                                        node['column']))

            return "({column} {operator} {value})".format(column=node['column'], operator=node['operator'],
                                                          value=node['value'])
        else:
            # logical node
            if 'operator' not in node.keys():
                raise BadRequest('There was neither a logical node nor a expression node provided')
            if 'childs' not in node.keys():
                raise BadRequest('No child nodes specified for logical node')

            if node['operator'] == 'not':
                if len(node['childs']) != 0:
                    raise BadRequest('For a logical not condition only one subexpression can be provided')
                return "NOT ({expression})".format(expression=PostgresHelper
                                                   ._convert_request_filter_node(node['childs'][0]))
            if node['operator'] == 'and':
                if len(node['childs']) < 2:
                    raise BadRequest('At least two sub expressions must be provided for a logical and')
                temp = []
                for sub_expression in node['childs']:
                    temp.append('{subexpression}'.format(subexpression=PostgresHelper
                                                           ._convert_request_filter_node(sub_expression)))
                return '({logicalexpression})'.format(logicalexpression=' and '.join(temp))
            if node['operator'] == 'or':
                if len(node['childs']) < 2:
                    raise BadRequest('At least two sub expressions must be provided for a logical or')
                temp = []
                for sub_expression in node['childs']:
                    temp.append('{subexpression}'.format(subexpression=PostgresHelper
                                                           ._convert_request_filter_node(sub_expression)))
                return '({logicalexpression})'.format(logicalexpression=' or '.join(temp))

    @classmethod
    def convert_order_by_to_string(cls, order_fields, order_type):
        """
        Converts a list of fields tjat shall be used for ordering into a Postgres string
        :param order_fields:
        :param order_type:
        :return:
        """
        if order_fields and len(order_fields) > 0:
            return 'ORDER BY {fields} {type}'.format(fields=', '.join(order_fields), type=order_type)
