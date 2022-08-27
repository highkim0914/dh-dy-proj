import datetime
import boto3
import pymysql
import json
from dbConnect import *


def lambda_handler(event, context):
    asset_id = event['pathParameters']['asset_id']
    uploading_hash = event['queryStringParameters']['hash']
    print(asset_id)
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(f'SELECT asset.file_hash FROM asset where asset.id = {asset_id}')
        query_results = cur.fetchall()
        existing_hash = query_results[0]['file_hash']
        if uploading_hash == existing_hash:
            return {
                "statusCode": 200,
                "body": "같은 파일입니다."
            }
        else:
            return {
                "statusCode": 200,
                "body": "다른 파일입니다."
            }

    except Exception as e:
        print("Database connection failed due to {}".format(e))
