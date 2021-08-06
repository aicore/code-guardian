import boto3
import os

dynamodb = None
root_table = None
PRIMARY_KEY = 'uid'
SORT_KEY = 'sort'


def get_single_table_name():
    return 'single-table-' + os.environ['stage']


def set_dynamodb():
    global dynamodb
    if dynamodb is None:
        if os.getenv('AWS_ACCESS_KEY_ID') is not None:
            dynamodb = boto3.resource('dynamodb', 'us-east-1',
                                      aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                                      aws_session_token=os.environ['AWS_SESSION_TOKEN']
                                      )
        else:
            dynamodb = boto3.resource('dynamodb', 'us-east-1')
    return dynamodb


def _get_single_table():
    global root_table, dynamodb
    set_dynamodb()
    if root_table is None:
        root_table = dynamodb.Table(get_single_table_name())
    return root_table


def get_primary_key_value(table_name, primary_key):
    return table_name + ':' + primary_key


def _get_key(table_name, primary_key, sort_key):
    return {
        PRIMARY_KEY: get_primary_key_value(table_name, primary_key),
        SORT_KEY: sort_key
    }


# will return item if present or None
def get_item(table_name, primary_key_str, sort_key_str):
    item_keys = _get_key(table_name, primary_key_str, sort_key_str)
    print("Getting item: ", item_keys)
    response = _get_single_table().get_item(
        Key=item_keys
    )
    return response.get('Item')


# will overwrite exiting data
def put_item(table_name, primary_key_str, sort_key_str, item={}):
    item_keys = _get_key(table_name, primary_key_str, sort_key_str)
    print("Putting item: ", item_keys)
    response = _get_single_table().put_item(
        # merge dict
        Item={**item, **item_keys}
    )
    return response


# idempotent. will delete and return success regardless of the item existed in the database.
def delete_item(table_name, primary_key_str, sort_key_str):
    item_keys = _get_key(table_name, primary_key_str, sort_key_str)
    print("Deleting item: ", item_keys)
    response = _get_single_table().delete_item(
        Key=item_keys
    )
    return response


def query_table_and_return_everything_filtered(key_condition_expression, filter_expression):
    table = _get_single_table()
    response = _get_single_table().query(
        KeyConditionExpression=key_condition_expression,
        FilterExpression=filter_expression
    )
    data = response['Items']

    # LastEvaluatedKey indicates that there are more results
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            FilterExpression=filter_expression,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        data.update(response['Items'])
    return data


def query_table_and_return_everything(key_condition_expression):
    table = _get_single_table()
    response = _get_single_table().query(
        KeyConditionExpression=key_condition_expression
    )
    data = response['Items']

    # LastEvaluatedKey indicates that there are more results
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        data.update(response['Items'])
    return data
