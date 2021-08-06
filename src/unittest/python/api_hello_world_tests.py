import json
from moto import mock_dynamodb2
import unittest
from setup_aws_test_mocks import setup_aws_infra

from api.api_schemas import PARAM_API
import lambda_handler
from test_utils import create_sample_event
from api.util import STATUS_CODE, BODY
from api import api_hello_world


@mock_dynamodb2
class LambdaMainTests(unittest.TestCase):
    def setUp(self):
        event = create_sample_event()
        lambda_handler._setup(event)
        setup_aws_infra()

    # noinspection PyMethodMayBeStatic
    def test_should_print_hello(self):
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
    def test_should_return_400_on_invalid_name(self):
        event = create_sample_event({
            PARAM_API: api_hello_world.API_NAME_HELLO_WORLD,
            api_hello_world.PARAM_NAME: "name with number 1"
        })
        return_val = lambda_handler.lambda_handler(event, "context")

        assert return_val[STATUS_CODE] == 400
