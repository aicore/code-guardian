import collections
import json

from api.util import API_PARAMS

PARAM_API = 'api'


def validate_lists_are_same(list1, list2, exception_message):
    if collections.Counter(list1) != collections.Counter(list2):
        raise Exception(exception_message)


def validate_input_output_handled(api_name, handled_inputs, handled_outputs):
    input_params = API_SCHEMAS[api_name]['input'].keys()
    validate_lists_are_same(input_params, handled_inputs, 'ERROR: ' + api_name +
                            ' : Inputs handled in API and schema definition differs ')
    output_params = API_SCHEMAS[api_name]['output']['BODY'].keys()
    validate_lists_are_same(output_params, handled_outputs, 'ERROR: ' + api_name +
                            ' : Output of API and schema definition differs')


def get_input_parameter(api_name, param):
    return API_SCHEMAS[api_name]['input'][param]


def get_output_parameter(api_name, param):
    return API_SCHEMAS[api_name]['output']['BODY'][param]


def _find_required_params_from_schema(api_name):
    keys = list(API_SCHEMAS.keys())
    keys.remove('endpoints')
    for key in keys:
        if API_SCHEMAS[key]['input']['api'] == api_name:
            return API_SCHEMAS[key]['input'].keys()


def check_event_confirms_to_schema_and_get_error(api_name, event):
    required_input_params = _find_required_params_from_schema(api_name)
    event_params = event[API_PARAMS].keys()
    if set(required_input_params).issubset(set(event_params)):
        return None
    missing_params = list(set(required_input_params).
                          difference(set(required_input_params).intersection(set(event_params))))
    print("ERROR: Some required params missing: ", json.dumps(missing_params))
    return "ERROR: Some required params missing: " + json.dumps(missing_params)


API_SCHEMAS = {
    "endpoints": {
        "dev": "https://api.openresearch.dev/dev/exec",
        "prod": "https://api.openresearch.dev/prod/exec"
    },
    "api_hello_world": {
        "HTTP_METHOD": "GET",
        "input": {
            "api": "hello_world",
            "name": "Your name to say hello"
        },
        "output": {
            "HTTP_RESPONSE_CODE": 200,
            "BODY": {
                "message": "hello world, <name>"
            }
        },
        "exceptions": [
            "401 access denied",
            "400 bad request"
        ]
    }
}
