import json

import pytest

from boomi_cicd.util.common_util import parse_json


def test_parse_json(tmpdir):
    # Create a temporary file with some JSON data
    test_data = {'name': 'test', 'value': 42}
    test_file = tmpdir.join('test.json')
    test_file.write(json.dumps(test_data))

    # Test the function
    result = parse_json(str(test_file))
    assert result == test_data


def test_parse_json_no_file():
    # Test that the function raises a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        parse_json('nonexistent/file.json')


def test_parse_json_invalid_json(tmpdir):
    # Create a temporary file with invalid JSON data
    test_file = tmpdir.join('invalid.json')
    test_file.write('not valid json')

    # Test that the function raises a JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        parse_json(str(test_file))


@pytest.fixture
def mock_cli_base_dir(monkeypatch):
    # Mock the CLI_BASE_DIR environment variable
    monkeypatch.setenv('CLI_BASE_DIR', '/test/path')


def test_parse_json_mocked_cli_base_dir(tmpdir, mock_cli_base_dir):
    # Test that the function uses the correct CLI_BASE_DIR value
    test_data = {'name': 'test', 'value': 42}
    test_file = tmpdir.join('test.json')
    test_file.write(json.dumps(test_data))

    result = parse_json(str(test_file))
    assert result == test_data

    # Check that the function used the mocked CLI_BASE_DIR value
    assert test_file.dirname == '/test/path'


def test_parse_json_file_closed(tmpdir):
    # Test that the file is closed after reading
    test_data = {'name': 'test', 'value': 42}
    test_file = tmpdir.join('test.json')
    test_file.write(json.dumps(test_data))

    with open(str(test_file), 'r') as f:
        # Monkeypatch the open() function to return the open file
        with pytest.monkeypatch.context() as m:
            m.setattr(__builtins__, 'open', lambda x: f)
            result = parse_json(str(test_file))
            assert result == test_data

        # Check that the file is closed
        assert f.closed
