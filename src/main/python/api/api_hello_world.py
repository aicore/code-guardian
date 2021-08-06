from api.api_schemas import PARAM_API,\
    validate_input_output_handled, get_input_parameter
from api.util import http_400_bad_request, API_PARAMS, \
    http_200_ok_with_json_response

SCHEMA_DEFINITION_API_NAME = 'api_hello_world'
PARAM_NAME = 'name'

RESPONSE_MESSAGE = 'message'


def validate_api_confirms_to_schema():
    validate_input_output_handled(SCHEMA_DEFINITION_API_NAME, [
        PARAM_API, PARAM_NAME
    ], [
        RESPONSE_MESSAGE
    ])


API_NAME_HELLO_WORLD = get_input_parameter(SCHEMA_DEFINITION_API_NAME, PARAM_API)


def _get_validation_errors_if_any(name):
    if not all(x.isalpha() or x.isspace() for x in name):
        # names should contain only alphabets or space
        return http_400_bad_request("Please provide a valid name without any numbers")
    return None


def say_hello(event_details):
    validate_api_confirms_to_schema()
    name = event_details[API_PARAMS][PARAM_NAME]

    validation_error = _get_validation_errors_if_any(name)
    if validation_error:
        return validation_error

    return http_200_ok_with_json_response({
        RESPONSE_MESSAGE: "Hello World, " + name
    })
