
from mlhomeserver.utils import get_project_version, get_current_competitions_from_yml

def test_get_project_version():
    assert get_project_version() == '0.1.3'

def test_get_current_competitions_correct():
    assert get_current_competitions_from_yml() == ['aidtec']