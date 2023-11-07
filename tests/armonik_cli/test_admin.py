import armonik_cli.admin as admin
from armonik.client.sessions import ArmoniKSessions, SessionFieldFilter, TaskOptions
from armonik.client.tasks import ArmoniKTasks, TaskFieldFilter
from armonik.common.filter import Filter
from datetime import timedelta
import pytest


grpc_channel = admin.create_channel({'--endpoint' : 'localhost:5001', '--ca' : None})
session_client = ArmoniKSessions(grpc_channel)
task_client = ArmoniKTasks(grpc_channel)


def test_is_armonik_up():
    session_client = admin.ArmoniKSessions(grpc_channel)
    admin.list_sessions(session_client, admin.create_session_filter(True, False,False))

def test_create_session():
    new_session = TaskOptions(max_duration=timedelta(0,3),priority=1, max_retries=10)
    assert session_client.create_session(new_session) is not None

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

def test_list_all_sessions():
    sessions = admin.list_sessions(session_client, admin.create_session_filter(True, False, False))
    assert sessions is not None
    assert len(sessions) > 0 

def test_list_running_sessions():
    sessions = admin.list_sessions(session_client, admin.create_session_filter(False, True, False))
    assert sessions is not None
    assert len(sessions) > 0 

def test_cancel_sessions():
    TaskOptions(max_duration=timedelta(0,3),priority=1, max_retries=10)
    sessions = admin.list_sessions(session_client, admin.create_session_filter(False, True, False))
    admin.cancel_sessions(session_client, sessions)
    update_sessions = admin.list_sessions(session_client, admin.create_session_filter(False, True, False))
    assert len(update_sessions) == 0
    
def test_list_cancelled_sessions():
    sessions = admin.list_sessions(session_client, admin.create_session_filter(False, False, True))
    assert sessions is not None
    assert len(sessions) > 0 
    


 