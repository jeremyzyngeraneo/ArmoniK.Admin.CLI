import subprocess

import pytest
from unittest.mock import Mock


import armonik_cli.admin as admin
from armonik.common.filter import Filter
from armonik.client.sessions import Session

# def test_list_session():
#     assert 5 == 6
    
grpc_channel = admin.create_channel({'--endpoint' : 'localhost:5001', '--ca' : None})
session_client = admin.ArmoniKSessions(grpc_channel)

def test_is_armonik_up():
    admin.list_sessions(session_client, admin.create_session_filter(True, False,False))

def test_is_armonik_down():
    with pytest.raises(Exception):
        admin.list_sessions(session_client, admin.create_session_filter(True, False, False))

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


def test_list_sessions():

    mock = Mock()

    mock = admin.list_sessions(session_client, admin.create_session_filter(True, False, False))

    print(mock, type)


test_list_sessions()


