import unittest
from unittest.mock import patch

import pytest

from boomi_cicd.util.atom import *


class TestAtom(unittest.TestCase):
    @patch('boomi_cicd.util.atom.requests_post')
    def test_query_atom(self, mock_post):
        mock_post.return_value.text = json.dumps({
            "@type": "QueryResult",
            "result": [
                {
                    "@type": "Atom",
                    "capabilities": [],
                    "id": "8a0a749b-4e1f-45c8-b5cc-e637f7c282e5",
                    "name": "Test Atom",
                    "status": "ONLINE",
                    "type": "MOLECULE",
                    "hostName": "localhost",
                    "dateInstalled": "2022-05-11T03:17:09Z",
                    "currentVersion": "23.04.2",
                    "purgeHistoryDays": 1,
                    "purgeImmediate": "false",
                    "forceRestartTime": 900000
                }
            ],
            "numberOfResults": 1
        })
        mock_env = {
            "baseUrl": "https://api.boomi.com/api/rest/v1",
            "accountId": "boomi_account-123",
            "username": "",
            "password": "",
            "environmentName": "Test Cloud Environment",
            "atomName": "Test Atom",
            "workingDirectory": "C:\\Code\\VSCode\\boomi-cli\\"
        }
        expected_payload = {
            "QueryFilter": {
                "expression": {
                    "argument": ["Test Atom"],
                    "operator": "EQUALS",
                    "property": "name"
                }
            }
        }
        result = query_atom(mock_env, mock_env["atomName"])

        # Assert the function calls requests_post with the expected arguments
        mock_post.assert_called_with(mock_env, "/Atom/query", expected_payload)
        # Assert the function returns the expected Atom ID
        assert result == "8a0a749b-4e1f-45c8-b5cc-e637f7c282e5"

    @patch('boomi_cicd.util.atom.requests_post')
    def test_query_atom_no_results(self, mock_post):
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
            "atomName": "Fake Atom",
            "workingDirectory": "C:\\Code\\VSCode\\boomi-cli\\"
        }
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            result = query_atom(mock_env, mock_env["atomName"])
        # Assert that the function raises a SystemExit exception
        assert pytest_wrapped_e.type == SystemExit
