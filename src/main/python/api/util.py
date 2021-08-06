import json
import os
from datetime import datetime, timedelta


API = 'api'
STAGE = 'stage'
API_PARAMS = 'apiParams'
ROLE = 'role'
STATUS_CODE = 'statusCode'
BODY = 'body'
HEADERS = 'headers'
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
    'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With'
}


def get_stage():
    return os.getenv('stage')


def utc_to_ist(utc_dt):
    return utc_dt + timedelta(minutes=330)


def get_ist_date_string_now():
    utc_now = datetime.utcnow()
    ist_now = utc_to_ist(utc_now)
    return ist_now.strftime("%Y-%m-%d")


def get_ist_timestamp_string_now():
    utc_now = datetime.utcnow()
    ist_now = utc_to_ist(utc_now)
    return ist_now.strftime("%Y-%m-%d_%H-%M-%S.%f")


def is_valid_date(date_str_YYYYMMDD):
    date = date_str_YYYYMMDD.split('-')
    if len(date) != 3:
        return False
    try:
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        datetime(int(year), int(month), int(day))
        if len(date[0]) != 4 or len(date[1]) != 2 or len(date[2]) != 2:
            return False
    except ValueError:
        return False
    return True


def http_200_ok(body):
    print("200 OK: ")
    print(body)
    return {
        STATUS_CODE: 200,
        BODY: body,
        HEADERS: CORS_HEADERS
    }


def http_200_ok_with_json_response(object):
    json_str = json.dumps(object)
    print("200 OK: ")
    print(json_str)
    return {
        STATUS_CODE: 200,
        BODY: json_str,
        HEADERS: CORS_HEADERS
    }


def http_400_bad_request(body='400: request cannot be completed'):
    print("400 bad request: ")
    print(body)
    return {
        STATUS_CODE: 400,
        BODY: body,
        HEADERS: CORS_HEADERS
    }


def http_401_unauthorized(body='401: You do not have permission to access this resource'):
    print("401 unauthorised: ")
    print(body)
    return {
        STATUS_CODE: 401,
        BODY: body,
        HEADERS: CORS_HEADERS
    }


def http_500_inernal_server_error(body='500: oops something went wrong.'):
    print("500 internal server error: ")
    print(body)
    return {
        STATUS_CODE: 500,
        BODY: body,
        HEADERS: CORS_HEADERS
    }
