import json
import os
import sys
import pathlib
import traceback
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, str(pathlib.Path(__file__).parent.absolute()))

from api import exec_api
from api import util
from scheduler import do_work

STAGE = 'stage'
EVENT_TYPE = 'event_type'
EVENT_TYPE_WORKER = 'worker'
EVENT_TYPE_REST_API_CALL = 'rest_api_call'
EVENT = 'event'
REST_API_HTTP_METHOD = 'httpMethod'

_WORKER_INFO = 'worker_info'


def _get_env(event):
    if event.get(_WORKER_INFO):
        return {
            EVENT_TYPE: EVENT_TYPE_WORKER,
            STAGE: event[_WORKER_INFO][STAGE]
        }
    return {
        EVENT_TYPE: EVENT_TYPE_REST_API_CALL,
        STAGE: event['requestContext'][STAGE],
        REST_API_HTTP_METHOD: event['httpMethod']
    }


def _setup_env_variables(env_vars):
    for enk_key in env_vars:
        os.environ[enk_key] = env_vars[enk_key]


def _setup(event):
    env_vars = _get_env(event)
    _setup_env_variables(env_vars)
    return env_vars


def lambda_handler(event, context):
    print(json.dumps(event))
    event_type = EVENT_TYPE_REST_API_CALL
    try:
        env = _setup(event)
        if env.get(EVENT_TYPE) == EVENT_TYPE_WORKER:
            event_params = event[_WORKER_INFO][EVENT]
            event_type = EVENT_TYPE_WORKER
            return do_work.process_event(event_params)
        if env["httpMethod"].upper() == 'OPTIONS':
            # for CORS support
            return util.http_200_ok('{}')
        return exec_api.process_event(event)
    except Exception as e:
        # printing stack trace
        traceback.print_exc()
        if event_type == EVENT_TYPE_WORKER:
            raise e
        return util.http_500_inernal_server_error()
