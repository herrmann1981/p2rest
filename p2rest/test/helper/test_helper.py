"""
Helper function for our test cases
"""
import unittest


def check_common_data(testcase: unittest.TestCase, data, status_code):
    """
    Check if all common fields are present in a returned data
    :param testcase: The test case that was executed
    :param data: The json data that was returned from the test call
    :param status_code: The status code of the request, so we can check it in the content
    :return: None
    """
    testcase.assertTrue(type(data) == dict)
    for k in ['status_code', 'message', 'description', 'count', 'duration', 'data']:
        testcase.assertTrue(k in data.keys())
    testcase.assertEqual(data['status_code'], status_code)
    testcase.assertIsNotNone(data['message'])
    testcase.assertIsNotNone(data['description'])
    testcase.assertTrue(len(data['message']) > 3)
    testcase.assertTrue(len(data['message']) < len(data['description']))
