import armonik_cli.admin as admin
from armonik.client.sessions import ArmoniKSessions, SessionFieldFilter, TaskOptions
from armonik.client.tasks import ArmoniKTasks, TaskFieldFilter
from datetime import timedelta
import pytest

@pytest.fixture
def insecure_grpc_channel():
    return admin.create_channel({'--endpoint': 'localhost:5001', '--ca': None})

@pytest.fixture
def session_client(insecure_grpc_channel):
    return ArmoniKSessions(insecure_grpc_channel)

def test_is_armonik_up(session_client):
    admin.list_sessions(session_client, admin.create_session_filter(True, False,False))

def test_create_session(session_client):
    new_session = TaskOptions(max_duration=timedelta(0,3),priority=1, max_retries=10)
    assert session_client.create_session(new_session) is not None

def test_list_all_sessions(session_client):
    sessions = admin.list_sessions(session_client, admin.create_session_filter(True, False, False))
    assert sessions is not None
    assert len(sessions) > 0 

def test_list_running_sessions(session_client):
    sessions = admin.list_sessions(session_client, admin.create_session_filter(False, True, False))
    assert sessions is not None
    assert len(sessions) > 0 

def test_cancel_sessions(session_client):
    TaskOptions(max_duration=timedelta(0,3),priority=1, max_retries=10)
    sessions = admin.list_sessions(session_client, admin.create_session_filter(False, True, False))
    admin.cancel_sessions(session_client, sessions)
    update_sessions = admin.list_sessions(session_client, admin.create_session_filter(False, True, False))
    assert len(update_sessions) == 0
    
def test_list_cancelled_sessions(session_client):
    sessions = admin.list_sessions(session_client, admin.create_session_filter(False, False, True))
    assert sessions is not None
    assert len(sessions) > 0 
    


 