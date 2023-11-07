"""ArmoniK Admin CLI to perform admnistration tasks for ArmoniK

Usage:
  armonik.py cancel-session list <session>... [--endpoint ENDPOINT] [--ca CA_FILE] [--cert CERT_FILE] [--key KEY_FILE]
  armonik.py cancel-session --running         [--endpoint ENDPOINT] [--ca CA_FILE] [--cert CERT_FILE] [--key KEY_FILE]
  armonik.py cancel-task <task>...            [--endpoint ENDPOINT] [--ca CA_FILE] [--cert CERT_FILE] [--key KEY_FILE]
  armonik.py list-task <session>...           [--endpoint ENDPOINT] [--ca CA_FILE] [--cert CERT_FILE] [--key KEY_FILE] [--all | --creating | --error]
  armonik.py list-session                     [--endpoint ENDPOINT] [--ca CA_FILE] [--cert CERT_FILE] [--key KEY_FILE] [--all | --running | --cancelled]
  armonik.py (-h | --help)
  armonik.py --version
  armonik.py check-task <taskid>


Options:
  -h --help                         Show this screen.
  --version                         Show version.
  -e ENDPOINT --endpoint ENDPOINT   ArmoniK control plane endpoint. [default: localhost:5001]
  --ca CA_FILE                      CA file for mutual tls
  --cert CERT_FILE                  Certificate for mutual tls
  --key KEY_FILE                    Private key for mutual tls
  --all                             Select all sessions or tasks
  --running                         Select running sessions
  --cancelled                       Select cancelled sessions
  --session SESSION                 Select tasks from SESSION
  --creating                        Select creating tasks
  --error                           Select error tasks
"""

from docopt import docopt
import grpc
from armonik.client.sessions import ArmoniKSessions, SessionFieldFilter, TaskOptions
from armonik.client.tasks import ArmoniKTasks, TaskFieldFilter
from armonik.common.enumwrapper import TASK_STATUS_ERROR, TASK_STATUS_CREATING , SESSION_STATUS_RUNNING, SESSION_STATUS_CANCELLED, SESSION_STATUS_UNSPECIFIED
from armonik.common.filter import Filter
from datetime import timedelta

def create_channel(arguments):
    """
    Create a gRPC channel for communication with the ArmoniK control plane

    Args:
        arguments (dict): command-line arguments from docopt

    Returns:
        grpc.Channel: gRPC channel for communication
    """
    if(arguments["--ca"] != None and arguments["--cert"] != None and arguments["--key"] != None):
        ca = open(arguments["--ca"], 'rb').read()
        cert = open(arguments["--cert"], 'rb').read()
        key = open(arguments["--key"], 'rb').read()
        credentials = grpc.ssl_channel_credentials(ca, key, cert)
        return grpc.secure_channel(arguments["--endpoint"], credentials)
    else:
        return grpc.insecure_channel(arguments["--endpoint"])


def create_session_filter(all: bool, running: bool, cancelled: bool) -> Filter:
    """
    Create a session Filter

    Args:
        all (bool): Show all sessions
        running (bool): Show only running sessions
        cancelled (bool): Show only cancelled sessions
    Returns:
        Filter object
    """
    if all:
        session_filter = (SessionFieldFilter.STATUS == SESSION_STATUS_RUNNING) | (SessionFieldFilter.STATUS == SESSION_STATUS_CANCELLED)
    elif running:
        session_filter = SessionFieldFilter.STATUS == SESSION_STATUS_RUNNING
    elif cancelled:
        session_filter = SessionFieldFilter.STATUS == SESSION_STATUS_CANCELLED
    else:
         raise ValueError("SELECT ARGUMENT [--all | --running | --cancelled]")

    return session_filter


def list_sessions(client: ArmoniKSessions, session_filter: Filter):
    """
    List sessions with filter options

    Args:
        client (ArmoniKSessions): ArmoniKSessions instance for session management
        session_filter (Filter) : Filter for the session
    """
    result = []
    page = 0
    sessions = client.list_sessions(session_filter, page=page)
    
    while len(sessions[1]) > 0:
        for session in sessions[1]:
            print(f'Session ID: {session.session_id}')
            result.append(session.session_id)

        page += 1
        sessions = client.list_sessions(session_filter, page=page)

    print(f'\nNumber of sessions: {sessions[0]}\n')
    return result


def cancel_sessions(client: ArmoniKSessions, sessions: list):
    """
    Cancel sessions with a list of session IDs or all sessions running

    Args:
        client (ArmoniKSessions): Instance of the class with cancel_session method
        sessions (list): List of session IDs to cancel
    """
    for session_id in sessions:
        client.cancel_session(session_id)


def create_task_filter(session_ids: list, all: bool , creating: bool, error: bool) -> Filter:
    """
    Create a task Filter based on the provided options

    Args:
        session_id (str): Session ID to filter tasks
        all (bool): List all tasks regardless of status
        creating (bool): List only tasks in creating status
        error (bool): List only tasks in error status

    Returns:
        Filter object
    """
    for session_id in session_ids:
        if all:
            tasks_filter = TaskFieldFilter.SESSION_ID == session_id
        elif creating:
            tasks_filter = (TaskFieldFilter.SESSION_ID == session_id) & (TaskFieldFilter.STATUS == TASK_STATUS_CREATING)
        elif error:
            tasks_filter = (TaskFieldFilter.SESSION_ID == session_id) & (TaskFieldFilter.STATUS == TASK_STATUS_ERROR)
        else:
             raise ValueError("SELECT ARGUMENT [--all | --creating | --error]")

        return tasks_filter
    

def list_tasks(client: ArmoniKTasks, task_filter: Filter):
    """
    List tasks associated with the specified sessions based on filter options

    Args:
        client (ArmoniKTasks): ArmoniKTasks instance for task management
        task_filter (Filter): Filter for the task
    """

    page = 0
    tasks = client.list_tasks(task_filter, page=page)
    while len(tasks[1]) > 0:
        for task in tasks[1]:
            print(f'Task ID: {task.id}')
        page += 1
        tasks = client.list_tasks(task_filter, page=page)

    print(f"\nTotal tasks: {tasks[0]}\n")

def check_task(client: ArmoniKTasks, task_id: str):
    """
    Check the status of a task based on its ID.

    Args:
        client (ArmoniKTasks): ArmoniKTasks instance for task management.
        task_id (str): ID of the task to check.
    """
    tasks = client.list_tasks(TaskFieldFilter.TASK_ID == task_id)
    if len(tasks[1]) > 0:
        print(f"\nTask information for task ID {task_id} :\n")
        print(tasks[1])
    else:
        print(f"No task found with ID {task_id}")


def main():
    arguments = docopt(__doc__, version="ArmoniK Admin CLI  0.0.1")

    grpc_channel = create_channel(arguments)
    session_client = ArmoniKSessions(grpc_channel)
    task_client = ArmoniKTasks(grpc_channel)

    if arguments['list-session']:
        list_sessions(session_client, create_session_filter(arguments["--all"], arguments["--running"], arguments["--cancelled"]))

    if arguments['list-task']:
        session_ids = arguments["<session>"]
        list_tasks(task_client, create_task_filter(session_ids, arguments["--all"], arguments["--creating"], arguments["--error"]))

    if arguments['check-task']:
        task_id = arguments["<taskid>"]
        check_task(task_client, task_id)

    if arguments['cancel-session']:
        if arguments["list"]:
            cancel_sessions(session_client, arguments["<session>"])
        if arguments["--running"]:
            _, session_list = session_client.list_sessions(SessionFieldFilter.STATUS == SESSION_STATUS_RUNNING)
            session_ids = [session.session_id for session in session_list]
            cancel_sessions(session_client, session_ids)
    
if __name__ == '__main__':
    main()
