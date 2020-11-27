
"""
Test module for our schema endpoint
"""
import unittest
import os
import psycopg2
from flask import current_app

from p2rest.src import create_app


class TestSchema(unittest.TestCase):
    """
    Test case for our Location endpoints
    """

    def setUp(self):
        """
        Create the app
        :return:
        """
        self.app = create_app('test')
        self.client = self.app.test_client

        # self.admin_header = {'Authorization': 'Bearer ' + os.environ['admin_token']}
        # self.user_header = {'Authorization': 'Bearer ' + os.environ['user_token']}

    def tearDown(self):
        """
        Clean up after this test case has run
        :return:
        """
        pass

    def test_get_schema_endpoint(self):
        """
        Tests the Get endpoint without any content
        :return:
        """
        response = self.client().get('/schema/') # , headers=self.admin_header)
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertTrue('status_code' in data.keys())
        self.assertTrue('message' in data.keys())
        self.assertTrue('description' in data.keys())
        self.assertTrue('data' in data.keys())
        self.assertTrue('count' in data.keys())
        self.assertTrue('duration' in data.keys())
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['count'] > 0)
