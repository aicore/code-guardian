from moto import mock_dynamodb2
import unittest
from setup_aws_test_mocks import setup_aws_infra

from api.api_schemas import validate_lists_are_same, get_output_parameter
from api import api_hello_world
import lambda_handler
from test_utils import create_sample_event


@mock_dynamodb2
class LambdaMainTests(unittest.TestCase):
    def setUp(self):
        event = create_sample_event()
        lambda_handler._setup(event)
        setup_aws_infra()

    # noinspection PyMethodMayBeStatic
    def test_should_validate_lists_are_same(self):
        validate_lists_are_same(['1', 2, 3], [2, 3, '1'], 'exception message if not same')
        self.assertRaises(Exception, validate_lists_are_same, [], [1], 'ece')

    # noinspection PyMethodMayBeStatic
    def test_should_get_output_params(self):
        output = get_output_parameter(api_hello_world.SCHEMA_DEFINITION_API_NAME, api_hello_world.RESPONSE_MESSAGE)
        assert output == 'hello world, <name>'
