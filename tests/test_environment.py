import json
import unittest
from unittest.mock import patch

import pytest

from cli.scripts.bin.environment import query_environment


class TestEnvironment(unittest.TestCase):
    @patch('cli.scripts.bin.environment.requests_post')
    def test_query_environment(self, mock_post):
        mock_post.return_value.text = json.dumps({"@type": "QueryResult", "result": [
            {"@type": "Environment", "id": "13da4a90-53f4-4396-b63d-83ef772ee8d", "name": "Test Cloud Environment",
             "classification": "TEST"}], "numberOfResults": 1})
        mock_env = {
            "baseUrl": "https://api.boomi.com/api/rest/v1",
            "accountId": "boomi_test-WI542T",
            "username": "",
            "password": "",
            "environmentName": "Test Cloud Environment",
            "workingDirectory": "C:\\Code\\VSCode\\boomi-cli\\"
        }
        expected_payload = {
            "QueryFilter": {
                "expression": {
                    "argument": ["Test Cloud Environment"],
                    "operator": "EQUALS",
                    "property": "name"
                }
            }
        }

        result = query_environment(mock_env)

        # Assert the function calls requests_post with the expected arguments
        mock_post.assert_called_with(mock_env, "/Environment/query", expected_payload)
        # Assert the function returns the expected environment ID
        assert result == "13da4a90-53f4-4396-b63d-83ef772ee8d"

    @patch('cli.scripts.bin.environment.requests_post')
    def test_query_environment_no_results(self, mock_post):
        mock_post.return_value.text = json.dumps({
            "@type": "QueryResult",
            "result": [],
            "numberOfResults": 0
        })
        mock_env = {
            "baseUrl": "https://api.boomi.com/api/rest/v1",
            "accountId": "boomi_test-WI542T",
            "username": "",
            "password": "",
            "environmentName": "Fake Environment",
            "workingDirectory": "C:\\Code\\VSCode\\boomi-cli\\"
        }
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            result = query_environment(mock_env)
        # Assert that the function raises a SystemExit exception
        assert pytest_wrapped_e.type == SystemExit
