from boto3.dynamodb.conditions import Key
from database.table_operations import get_item, put_item, delete_item, \
    query_table_and_return_everything, PRIMARY_KEY, get_primary_key_value

# primary_key = login_with_github
# sort_key =  github_login
# other fields : [role]

# example table structure
# uid                             |  sort          | role            |
# allowed_users:login_with_github | github_login   | user/admin/etc. |


FIELD_ROLE = 'role'
FIELD_ADDED_BY = 'added_by'

SCOPE_LOGIN_WITH_GITHUB = 'login_with_github'


def _get_allowed_user_table_name():
    return 'allowed_user_table'


def get_user(username):
    return get_item(_get_allowed_user_table_name(), SCOPE_LOGIN_WITH_GITHUB, username)


def put_user(username, role, added_by_username):
    return put_item(_get_allowed_user_table_name(), SCOPE_LOGIN_WITH_GITHUB, username, {
        FIELD_ROLE: role,
        FIELD_ADDED_BY: added_by_username
    })


def delete_user(username):
    return delete_item(_get_allowed_user_table_name(), SCOPE_LOGIN_WITH_GITHUB, username)


def list_users():
    all_users = query_table_and_return_everything(
        Key(PRIMARY_KEY).eq(get_primary_key_value(_get_allowed_user_table_name(), SCOPE_LOGIN_WITH_GITHUB))
    )
    return all_users
