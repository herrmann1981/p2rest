
"""
Test module for our application configuration
"""
import unittest
import os
import psycopg2
from flask import current_app

from p2rest.src import create_app


class TestHealth(unittest.TestCase):
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

    def test_get_health_endpoint(self):
        """
        Tests the Get endpoint without any content
        :return:
        """
        response = self.client().get('/health/') # , headers=self.admin_header)
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertTrue('status_code' in data.keys())
        self.assertTrue('message' in data.keys())
        self.assertTrue('description' in data.keys())
        self.assertTrue('data' in data.keys())
        self.assertEqual(data['status_code'], 200)
        self.assertTrue('status' in data['data'].keys())
        self.assertTrue('db_connection' in data['data'].keys())

    def test_post_health_endpoint(self):
        """
        Tests the Get endpoint without any content
        :return:
        """
        response = self.client().post('/health/')  # , headers=self.admin_header)
        self.assertEqual(response.status_code, 405)  # not allowed

    def test_patch_health_endpoint(self):
        """
        Tests the Get endpoint without any content
        :return:
        """
        response = self.client().patch('/health/')  # , headers=self.admin_header)
        self.assertEqual(response.status_code, 405)  # not allowed

    def test_put_health_endpoint(self):
        """
        Tests the Get endpoint without any content
        :return:
        """
        response = self.client().put('/health/')  # , headers=self.admin_header)
        self.assertEqual(response.status_code, 405)  # not allowed

    def test_delete_health_endpoint(self):
        """
        Tests the Get endpoint without any content
        :return:
        """
        response = self.client().delete('/health/')  # , headers=self.admin_header)
        self.assertEqual(response.status_code, 405)  # not allowed