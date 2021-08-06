import unittest
from setup_aws_test_mocks import setup_aws_infra

from moto import mock_dynamodb2
from database import allowed_users_table
import lambda_handler
from test_utils import load_json_test_resource


@mock_dynamodb2
class AllowedUsersTableTests(unittest.TestCase):
    def setUp(self):
        event = load_json_test_resource('sample_request.json')
        lambda_handler._setup(event)
        setup_aws_infra()

    # noinspection PyMethodMayBeStatic
    def test_should_put_and_get_user(self):
        allowed_users_table.put_user('user1', 'admin', 'added_by_1')
        user = allowed_users_table.get_user('user1')

        assert user[allowed_users_table.FIELD_ROLE] == 'admin'

    # noinspection PyMethodMayBeStatic
    def test_should_delete_user(self):
        allowed_users_table.put_user('user1', 'admin', 'added_by_1')
        allowed_users_table.delete_user('user1')
        user = allowed_users_table.get_user('user1')

        assert user is None

    # noinspection PyMethodMayBeStatic
    def test_should_list_all_users(self):
        allowed_users_table.put_user('user1', 'admin', 'added_by_1')
        allowed_users_table.put_user('user2', 'user', 'added_by_1')

        users = allowed_users_table.list_users()

        assert len(users) == 2
