import datetime
import boto3
import pymysql
import json
from mysqlConnect import *


def lambda_handler(event, context):
    request_username = event['requestContext']['authorizer']['claims']['cognito:username']
    request_group = event['requestContext']['authorizer']['claims']['cognito:group']

    return {
        "statusCode": 200,
        "body": json.dumps({
            "username": request_username,
            "group": request_group
        })
    }
