import json
import pymysql
import boto3

from hello_world import Sample


def lambda_handler(event, context):

    client = boto3.client('rds')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world"
        }),
    }
