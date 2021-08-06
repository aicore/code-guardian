import json
from api.util import http_400_bad_request, API, http_401_unauthorized, \
    STAGE, API_PARAMS, ROLE
from api.api_schemas import check_event_confirms_to_schema_and_get_error
from api.api_hello_world import say_hello, API_NAME_HELLO_WORLD

QUERY_STRING_PARAMS_EVENT = 'queryStringParameters'
BODY = 'body'


def _intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def _is_duplicate_params_present(api_params, body_params):
    if len(_intersection(api_params.keys(), body_params.keys())) != 0:
        return True
    return False


def _merge_query_and_body_params(event):
    error = None
    all_params = event.get(QUERY_STRING_PARAMS_EVENT, {
        API: None
    })
    body_params_str = event.get(BODY)
    if body_params_str:
        body_params = json.loads(body_params_str)
        if _is_duplicate_params_present(all_params, body_params):
            error = http_400_bad_request('Error: Query string parameters conflicts with body parameters')
        else:
            all_params = {**all_params, **body_params}
    return all_params, error


def _get_event_details_and_login_role(event):
    event_details = {
        STAGE: event['requestContext']['stage'],
        API_PARAMS: None,
        ROLE: None
    }
    event_details[API_PARAMS], error = _merge_query_and_body_params(event)
    if error:
        return None, error
    if not event_details[API_PARAMS]:
        return None, http_400_bad_request("All required parameters missing")

    # TODO: Do github auth validations here after gateway filters
    # event_details[ROLE] = find github auth
    # if event_details[ROLE] is None:
    #    return None, http_401_unauthorized()
    return event_details, None


API_HANDLERS = {
    API_NAME_HELLO_WORLD: say_hello
}


def process_event(event):
    event_details, error = _get_event_details_and_login_role(event)

    if error:
        return error

    api_name = event_details[API_PARAMS][API]
    api_handler = API_HANDLERS.get(api_name)
    if api_handler is None:
        return http_400_bad_request('unknown API: ' + event_details[API_PARAMS][API])
    error = check_event_confirms_to_schema_and_get_error(api_name, event_details)
    if error:
        return http_400_bad_request(error)

    print("Executing API handler:", api_name, ":", event_details)
    return api_handler(event_details)

