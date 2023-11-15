import armonik_cli.admin as admin
from armonik.common.filter import Filter
import pytest
from unittest.mock import Mock

mock = Mock()

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

def test_creating_task_filter_all():
    task_filter = admin.create_task_filter(["a","b"], True, False, False)
    assert isinstance(task_filter, Filter)

def test_creating_task_filter_creating():
    task_filter = admin.create_task_filter(["a","b"], True, False, False)
    assert isinstance(task_filter, Filter)

def test_creating_task_filter_error():
    mock = admin.create_task_filter(([1,"b"], True, False, False))
    task_filter = admin.create_task_filter([1,"b"], True, False, False)
    assert isinstance(task_filter, Filter)


