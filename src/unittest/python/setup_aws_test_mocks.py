import os
import boto3
from moto import mock_dynamodb2
from database.table_operations import get_single_table_name, _get_key


infra_setup_complete = False
SAMPLE_TABLE_NAME = 'SAMPLE_TABLE_NAME'


def _set_aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


def _add_item(table, table_name, primary_key, sort_key, item={}):
    item_keys = _get_key(table_name, primary_key, sort_key)
    table.put_item(
        Item={**item, **item_keys}
    )


def _add_sample_items(table):
    _add_item(table, SAMPLE_TABLE_NAME, 'user', 'pass')


@mock_dynamodb2
def _setup_ddb():
    dynamodb = boto3.resource("dynamodb", "us-east-1")
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName=get_single_table_name(),
        KeySchema=[
            {"AttributeName": "uid", "KeyType": "HASH"},
            {"AttributeName": "sort", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "uid", "AttributeType": "S"},
            {"AttributeName": "sort", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    _add_sample_items(table)


def setup_aws_infra():
    _set_aws_credentials()
    global infra_setup_complete
    if not infra_setup_complete:
        _setup_ddb()
        infra_setup_complete = True
