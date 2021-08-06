import json
from moto import mock_dynamodb2
import os
import unittest
from setup_aws_test_mocks import setup_aws_infra

from api.api_schemas import PARAM_API
import lambda_handler
from test_utils import create_sample_worker_event
from api.util import STATUS_CODE, BODY
from scheduler.do_work import WORKER


@mock_dynamodb2
class LambdaMainTests(unittest.TestCase):
    def setUp(self):
        event = create_sample_worker_event()
        lambda_handler._setup(event)
        setup_aws_infra()

    # noinspection PyMethodMayBeStatic
    def test_should_lambda_handler_set_env_vars(self):
        event = create_sample_worker_event()
        lambda_handler.lambda_handler(event, "context")

        assert os.environ['stage'] == event['worker_info']['stage']

    # noinspection PyMethodMayBeStatic
    def test_should_exception_on_unknown_api(self):
        event = create_sample_worker_event({
            WORKER: 'invalid worker'
        })
        self.assertRaises(Exception, lambda_handler.lambda_handler, event, "context")

