import json
import pathlib

SAMPLE_API_REQUEST = 'sample_request.json'
SAMPLE_WORK_REQUEST = 'worker_request.json'


def _get_test_resource_file_path(file_name):
    return pathlib.Path(__file__).parent.parent.absolute() \
        .joinpath('test_resources') \
        .joinpath(file_name)


def load_json_test_resource(json_file_name):
    file_path = _get_test_resource_file_path(json_file_name)
    f = open(file_path, "r")
    data = json.loads(f.read())
    f.close()
    return data


def create_sample_event(query_string_params={}, body_obj=None, http_verb=None):
    sample_req = load_json_test_resource(SAMPLE_API_REQUEST)
    if query_string_params:
        sample_req['queryStringParameters'] = query_string_params
    if body_obj:
        sample_req['body'] = json.dumps(body_obj)
    if http_verb:
        sample_req['httpMethod'] = http_verb
    return sample_req


def create_sample_worker_event(override_event=None):
    sample_req = load_json_test_resource(SAMPLE_WORK_REQUEST)
    if override_event:
        sample_req['worker_info']['event'] = override_event
    return sample_req
