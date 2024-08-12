
from unittest.mock import patch, mock_open

import pytest

from mlhomeserver.utils import get_project_version, get_current_competitions_from_yml

def test_get_project_version_success():
    mock_toml_content = """
    [tool.poetry]
    version = "1.2.0"
    """
    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        with patch("toml.load", return_value={"tool": {"poetry": {"version": "1.2.0"}}}):
            assert get_project_version() == "1.2.0"

def test_get_project_version_missing_key():
    mock_toml_content = """
    [tool.poetry]
    """
    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        with patch("toml.load", return_value={"tool": {"poetry": {}}}):
            with pytest.raises(KeyError):
                get_project_version()

def test_get_project_version_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            get_project_version()

def test_get_current_competitions_correct():
    assert get_current_competitions_from_yml() == ['aidtec', 'efficiency']