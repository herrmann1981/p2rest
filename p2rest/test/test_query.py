
"""
Test module for our schema endpoint
"""
import unittest
import json
import psycopg2
from p2rest.test.helper.test_helper import check_common_data
from p2rest.src import create_app


QUERY_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS public.{table_name} (
        id serial NOT NULL,
        manufacturer varchar(50) NOT NULL,
        "type" varchar(50) NOT NULL,
        licenseplate varchar(25) NULL
    );
"""

QUERY_INSERT_DATA = """
    INSERT INTO public.{table_name} (id, manufacturer, "type", licenseplate)
    VALUES
        (1, 'BMW', '760i', 'M-VL-2515'),
        (2, 'BMW', '325i', 'M-VL-1515'),
        (3, 'VW', 'Golf', 'H-A-6548'),
        (4, 'VW', 'Passat', 'H-DM-415'),
        (5, 'Audi', 'A4', 'IN-G-489'),
        (6, 'Audi', 'A6', 'IN-MF-45'),
        (7, 'Mercedes', 'S-500', 'S-L-4113'),
        (8, 'Mercedes', 'SEL', 'S-DM-1387'),
        (9, 'Ford', 'Cougar', 'K-Q-485'),
        (10, 'Ford', 'Focus', 'K-OP-8714');
"""

QUERY_DROP_TABLE = """
    DROP TABLE IF EXISTS public.{table_name};
"""


class TestQuery(unittest.TestCase):
    """
    Test case for our Location endpoints
    """

    @classmethod
    def open_connection(cls, app):
        connection = psycopg2.connect(host=app.config['P2REST_DB_HOST'],
                                      port=app.config['P2REST_DB_PORT'],
                                      dbname=app.config['P2REST_DB_NAME'],
                                      user=app.config['P2REST_DB_USER'],
                                      password=app.config['P2REST_DB_PASSWORD'])
        cursor = connection.cursor()
        return connection, cursor

    @classmethod
    def close_connection(cls, connection, cursor):
        try:
            cursor.close()
            connection.close()
        except:
            pass

    def setUp(self):
        """
        Create the app
        :return:
        """
        self.app = create_app('test')
        self.client = self.app.test_client

        # Initialize database
        con, cur = TestQuery.open_connection(self.app)
        cur.execute(QUERY_DROP_TABLE.format(table_name=self._testMethodName))
        cur.execute(QUERY_CREATE_TABLE.format(table_name=self._testMethodName))
        cur.execute(QUERY_INSERT_DATA.format(table_name=self._testMethodName))
        con.commit()
        TestQuery.close_connection(con, cur)

        # self.admin_header = {'Authorization': 'Bearer ' + os.environ['admin_token']}
        # self.user_header = {'Authorization': 'Bearer ' + os.environ['user_token']}

    def tearDown(self):
        """
        Clean up after this test case has run
        :return:
        """

        # clean up database
        con, cur = TestQuery.open_connection(self.app)
        cur.execute(QUERY_DROP_TABLE.format(table_name=self._testMethodName))
        con.commit()
        TestQuery.close_connection(con, cur)

    def test_query_get(self):
        """
        Test a GET call to the query endpoint --> Should fail
        :return:
        """
        response = self.client().get('/query/')  # , headers=self.admin_header)
        self.assertEqual(response.status_code, 404)
        check_common_data(self, response.json, response.status_code)

    def test_query_select_illegal_method(self):
        """
        Test a DELETE PATH or PUT on the /query/select endpoint
        :return:
        """
        response = self.client().get('/query/select')
        self.assertEqual(response.status_code, 405)
        check_common_data(self, response.json, response.status_code)

        response = self.client().put('/query/select')
        self.assertEqual(response.status_code, 405)
        check_common_data(self, response.json, response.status_code)

        response = self.client().patch('/query/select')
        self.assertEqual(response.status_code, 405)
        check_common_data(self, response.json, response.status_code)

        response = self.client().delete('/query/select')
        self.assertEqual(response.status_code, 405)
        check_common_data(self, response.json, response.status_code)

    def test_query_select_no_data(self):
        """
        Test a Post call to the query endpoint without data
        :return:
        """
        response = self.client().post('/query/select')  # , headers=self.admin_header)
        data = response.json

        check_common_data(self, response.json, response.status_code)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['data']), 0)

    def test_query_select_basic(self):
        """
        Test a POST call to the query/select endpoint with basic fields
        :return:
        """
        request_data = {
            'schema': 'public',
            'relation': self._testMethodName
        }
        response = self.client().post('/query/select',
                                      data=json.dumps(request_data),
                                      content_type='application/json')
        data = response.json

        check_common_data(self, response.json, response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], len(data['data']))
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(len(data['data'][0].keys()), 4)

        request_data = {
            'schema': 'public',
            'relation': self._testMethodName,
            'fields': ['id']
        }
        response = self.client().post('/query/select',
                                      data=json.dumps(request_data),
                                      content_type='application/json')
        data = response.json

        check_common_data(self, response.json, response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], len(data['data']))
        self.assertEqual(len(data['data']), 10)
        self.assertEqual(len(data['data'][0].keys()), 1)
