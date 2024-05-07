
from mlhomeserver.utils import get_project_version

def test_get_project_version():
    assert get_project_version() == '0.1.0'