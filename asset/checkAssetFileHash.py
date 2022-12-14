import datetime
import boto3
import pymysql
import json
from dbConnect import *

try:
    conn = get_connection()
except Exception as e:
    print("Database connection failed due to {}".format(e))


def lambda_handler(event, context):
    asset_id = event['pathParameters']['asset_id']
    uploading_hash = event['queryStringParameters']['hash']
    print(asset_id)
    try:
        cur = get_dict_cursor(conn)
        cur.execute(f'SELECT asset.file_hash FROM asset where asset.id = {asset_id}')
        query_results = cur.fetchall()
        existing_hash = query_results[0]['file_hash']
        conn.commit()
        if uploading_hash == existing_hash:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "is_same": "true",
                    "message": "같은 파일입니다."
                })
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "is_same": "false",
                    "message": "다른 파일입니다."
                })
            }

    except Exception as e:
        print("Database connection failed due to {}".format(e))
