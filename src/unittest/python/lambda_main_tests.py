import json
from moto import mock_dynamodb2
import os
import unittest
from setup_aws_test_mocks import setup_aws_infra

from api.api_schemas import PARAM_API
import lambda_handler
from test_utils import create_sample_event
from api.util import get_ist_date_string_now, get_ist_timestamp_string_now, STATUS_CODE, BODY
from api import api_hello_world, util


@mock_dynamodb2
class LambdaMainTests(unittest.TestCase):
    def setUp(self):
        event = create_sample_event()
        lambda_handler._setup(event)
        setup_aws_infra()

    # noinspection PyMethodMayBeStatic
    def test_ist_time(self):
        ist_time = get_ist_date_string_now()
        assert ist_time is not None
        timestamp = get_ist_timestamp_string_now()
        assert timestamp is not None

    # noinspection PyMethodMayBeStatic
    def test_should_lambda_handler_set_en_vars(self):
        event = create_sample_event()
        lambda_handler.lambda_handler(event, "context")

        assert os.environ['stage'] == event['requestContext']['stage']

    # noinspection PyMethodMayBeStatic
    def test_should_lambda_handler_retrun_200_on_options_verb(self):
        event = create_sample_event(http_verb='options')
        return_val = lambda_handler.lambda_handler(event, "context")

        assert return_val[STATUS_CODE] == 200

    # noinspection PyMethodMayBeStatic
    def test_should_retuen_400_on_unknown_api(self):
        event = create_sample_event({
            PARAM_API: 'api_that_doesnt_exist',
        }, {
        })
        return_val = lambda_handler.lambda_handler(event, "context")

        assert return_val[STATUS_CODE] == 400

    # noinspection PyMethodMayBeStatic
    def test_should_retuen_400_on_duplicate_query_params_and_body(self):
        event = create_sample_event({
            PARAM_API: 'apiname',
        }, {
            PARAM_API: 'apiname',
        })
        return_val = lambda_handler.lambda_handler(event, "context")

        assert return_val[STATUS_CODE] == 400

    # noinspection PyMethodMayBeStatic
    def test_should_allow_params_in_body_and_query_string(self):
        event = create_sample_event({
            PARAM_API: api_hello_world.API_NAME_HELLO_WORLD,
            api_hello_world.PARAM_NAME: "my name"
        })
        return_val = lambda_handler.lambda_handler(event, "context")

        assert return_val[STATUS_CODE] == 200
        assert json.loads(return_val[BODY]) == {
            api_hello_world.RESPONSE_MESSAGE: 'Hello World, my name'
        }

    # noinspection PyMethodMayBeStatic
    def test_should_fail_on_missing_required_params(self):
        event = create_sample_event({
            PARAM_API: api_hello_world.API_NAME_HELLO_WORLD
        })
        return_val = lambda_handler.lambda_handler(event, "context")

        assert return_val[STATUS_CODE] == 400

    # noinspection PyMethodMayBeStatic
    def test_should_validate_date(self):
        assert util.is_valid_date('2020-10-11') is True
        assert util.is_valid_date('2020-10-11-') is False
        assert util.is_valid_date('999-10-11') is False
        assert util.is_valid_date('10000-10-11') is False
        assert util.is_valid_date('2000-13-10') is False
        assert util.is_valid_date('2000-02-31') is False
        assert util.is_valid_date('2000-2-3') is False
