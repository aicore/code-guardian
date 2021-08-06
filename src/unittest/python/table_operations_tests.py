import unittest
from setup_aws_test_mocks import setup_aws_infra
from boto3.dynamodb.conditions import Key, Attr

from moto import mock_dynamodb2
from database.table_operations import PRIMARY_KEY,SORT_KEY, get_item, get_primary_key_value,\
    put_item, delete_item, query_table_and_return_everything, query_table_and_return_everything_filtered
import lambda_handler
from test_utils import load_json_test_resource

TEST_TABLE_NAME = 'test_table'


@mock_dynamodb2
class TableOperationsTests(unittest.TestCase):
    def setUp(self):
        event = load_json_test_resource('sample_request.json')
        lambda_handler._setup(event)
        setup_aws_infra()

    # noinspection PyMethodMayBeStatic
    def test_should_put_and_get_item(self):
        resp = put_item(TEST_TABLE_NAME, 'jane', 'makeba')
        item = get_item(TEST_TABLE_NAME, 'jane', 'makeba')

        assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
        assert item.get('sort') == 'makeba'

    # noinspection PyMethodMayBeStatic
    def test_should_delete_item(self):
        put_item(TEST_TABLE_NAME, 'ola', 'amigos')
        item = get_item(TEST_TABLE_NAME, 'ola', 'amigos')
        assert item is not None

        delete_item(TEST_TABLE_NAME, 'ola', 'amigos')
        item = get_item(TEST_TABLE_NAME, 'ola', 'amigos')
        assert item is None

    # noinspection PyMethodMayBeStatic
    def test_should_delete_item_should_succeed_even_if_item_not_present_in_table(self):
        status = delete_item(TEST_TABLE_NAME, 'some non existant primary key', 'sorty')
        assert status['ResponseMetadata']['HTTPStatusCode'] == 200

    # noinspection PyMethodMayBeStatic
    def test_should_query_with_key_condition_expression(self):
        put_item('custom_table','jane', 'makeba')
        put_item('custom_table', 'jane', 'dynabeat')
        put_item('custom_table', 'yeshudas', 'all',{
            'language': 'malayalam'
        })

        responses = query_table_and_return_everything(
            Key(PRIMARY_KEY).eq(get_primary_key_value('custom_table', 'jane'))
        )
        assert len(responses) == 2

        responses = query_table_and_return_everything(
            # primary key should be eq.
            Key(PRIMARY_KEY).eq(get_primary_key_value('custom_table', 'yeshudas')) &
            # sort key operations can be eq, between etc..
            # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html#Query.KeyConditionExpressions
            Key(SORT_KEY).eq('all')
        )
        assert len(responses) == 1
        assert responses[0]['language'] == 'malayalam'

        responses = query_table_and_return_everything(
            Key(PRIMARY_KEY).eq(get_primary_key_value('custom_table', 'not_in_table'))
        )
        assert len(responses) == 0

    # noinspection PyMethodMayBeStatic
    def test_should_query_with_key_condition_expression_and_filter(self):
        put_item('custom_table','jane', 'makeba')
        put_item('custom_table', 'jane', 'dynabeat')
        put_item('custom_table', 'yeshudas', 'all',{
            'language': 'malayalam'
        })

        responses = query_table_and_return_everything(
            Key(PRIMARY_KEY).eq(get_primary_key_value('custom_table', 'jane'))
        )
        assert len(responses) == 2

        responses = query_table_and_return_everything(
            # primary key should be eq.
            Key(PRIMARY_KEY).eq(get_primary_key_value('custom_table', 'yeshudas')) &
            # sort key operations can be eq, between etc..
            # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html#Query.KeyConditionExpressions
            Key(SORT_KEY).eq('all')
        )
        assert len(responses) == 1
        assert responses[0]['language'] == 'malayalam'

        responses = query_table_and_return_everything_filtered(
            Key(PRIMARY_KEY).eq(get_primary_key_value('custom_table', 'yeshudas')),
            Attr('language').eq('malayalam')
        )
        assert len(responses) == 1
        assert responses[0]['language'] == 'malayalam'

        responses = query_table_and_return_everything(
            Key(PRIMARY_KEY).eq(get_primary_key_value('custom_table', 'not_in_table'))
        )
        assert len(responses) == 0
