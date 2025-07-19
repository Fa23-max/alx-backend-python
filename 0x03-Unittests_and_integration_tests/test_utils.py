#!/usr/bin/env python3
import unittest
from utils import access_nested_map 
from parameterized import parameterized
from unittest.mock import patch, Mock
import requests
import json
class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": {"c": 3}}}, ("a", "b", "c"), 3),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)



class TestGetJson(unittest.TestCase):
    """
    Test suite for the get_json function.
    """

    # Use parameterized.expand to run the test with multiple inputs
    # Each tuple represents a test case: (test_name, test_url, test_payload)
    @parameterized.expand([
        ("test_example_url", "http://example.com", {"payload": True, "status": "success"}),
        ("test_holberton_url", "http://holberton.io", {"payload": False, "data": "empty"}),
    ])
    # Use unittest.mock.patch to replace requests.get with a Mock object during the test
    # The patched object (Mock) is passed as the last argument to the test method (mock_requests_get)
    @patch('requests.get')
    def test_get_json(self, name, test_url, test_payload, mock_requests_get):
        """
        Tests that get_json returns the expected result and that requests.get
        is called exactly once with the correct URL.
        """
        # 1. Configure the Mock object that requests.get will return:
        #    - Create a Mock object to simulate the HTTP response.
        #    - Set its 'json.return_value' to the desired test_payload.
        #    - Set the mock_requests_get's return_value to this mock_response.
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_requests_get.return_value = mock_response

        # 2. Call the function under test (get_json)
        #    This call will now use the mocked requests.get, not the real one.
        actual_result = get_json(test_url)

        # 3. Assertions:

        #    a. Test that the mocked 'get' method was called exactly once
        #       with 'test_url' as argument.
        mock_requests_get.assert_called_once_with(test_url)

        #    b. Test that the output of 'get_json' is equal to 'test_payload'.
        self.assertEqual(actual_result, test_payload)

# To run the tests from the command line:
if __name__ == '__main__':
    # unittest.main processes command-line arguments.
    # argv=['first-arg-is-ignored'] is used to prevent unittest.main from
    # trying to parse the script name as a test argument, which is common
    # when running directly. exit=False allows the script to continue
    # after tests if needed (e.g., for more code or interactive sessions).
    unittest.main(argv=['ignored-arg'], exit=False)