import armonik_cli.admin as admin
from armonik.common.filter import Filter
import pytest

def test_creating_session_filter_all():
    session_filter = admin.create_session_filter(True, False, False)
    assert isinstance(session_filter, Filter)

def test_creating_session_filter_running():
    session_filter = admin.create_session_filter(False, True, False)
    assert isinstance(session_filter, Filter)

def test_creating_session_filter_cancelled():
    session_filter = admin.create_session_filter(False, False, True)
    assert isinstance(session_filter, Filter)

def test_not_creating_session_filter():
    with pytest.raises(ValueError):
        admin.create_session_filter(False, False, False)